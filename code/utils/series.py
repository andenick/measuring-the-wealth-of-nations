"""Parametrized building blocks shared by per-series L##/P##/V## scripts.

Per the simplicity rule: each per-series script remains a thin, readable file
that declares its parameters and calls these helpers. The helpers don't hide
anything — they centralize the few mechanical steps that are identical across
every Ch5 series (read a wide CSV, project one column, validate against a
dict of benchmark years).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import pandas as pd

from .io import read_book_table, write_series_csv, write_validation_result


# ----- Tolerance classes (mirrors ST2 validation_config.json) -----

TOLERANCES = {
    "dollar_series": {"rel": 0.01,  "abs": 1.0},
    "rate_series":   {"rel": 0.001, "abs": 0.01},
    "share_series":  {"rel": 0.05,  "abs": 0.02},
    "level_series":  {"rel": 0.05,  "abs": 10.0},
}


# ----- Spec dataclasses -----

@dataclass(frozen=True)
class BookColumnLoader:
    """Load one column from a digitized book table CSV (wide format with `year` index).

    `unit_scale` divides raw values (e.g., 1000.0 converts millions→billions).
    Defaults to 1.0 (no conversion). The DPR documents the conversion when
    used so the provenance chain stays traceable.
    """

    series_id:    str            # e.g. "S502"
    subseries_id: str            # e.g. "S502-A"
    source_file:  Path           # e.g. BOOK_TABLES / "book_tableH1_1948_1989.csv"
    source_column: str           # e.g. "Mp"
    units:        str            # e.g. "billions_usd"
    unit_scale:   float = 1.0    # divisor applied to raw source values

    def load(self) -> pd.DataFrame:
        if not self.source_file.exists():
            raise FileNotFoundError(f"Source data missing: {self.source_file}")
        df = read_book_table(self.source_file)
        # Some digitized book tables leave the year column unnamed (`,col1,col2,...`
        # after the `#` comment row). Treat first column as `year` if it isn't already.
        if "year" not in df.columns:
            df = df.rename(columns={df.columns[0]: "year"})
        if self.source_column not in df.columns:
            raise KeyError(
                f"Column {self.source_column!r} not in {self.source_file.name}; "
                f"got {list(df.columns)[:8]}..."
            )
        out = df[["year", self.source_column]].rename(columns={self.source_column: "value"}).copy()
        out["series_id"] = self.subseries_id
        out["units"] = self.units
        out = out[["series_id", "year", "value", "units"]].reset_index(drop=True)
        out["year"] = out["year"].astype(int)
        out["value"] = out["value"].astype(float) / self.unit_scale
        return out


def standard_passthrough_processor(loader: BookColumnLoader, source_label: str) -> pd.DataFrame:
    """Standard book-period processor: pass-through with stage + provenance columns.

    Returns a frame ready to be written to intermediate/final. Use when the
    book series IS the canonical published value (no transformation needed for
    the book period; extension/splice stages add rows in later pipeline runs).
    """
    df = loader.load()
    df["stage"] = "book_period"
    df["provenance"] = source_label
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


# ----- Validator helpers -----

def _within_tol(actual: float, expected: float, *, rel_tol: float, abs_tol: float) -> tuple[bool, float, float]:
    abs_err = abs(actual - expected)
    rel_err = abs_err / max(abs(expected), 1e-12)
    return (abs_err <= abs_tol or rel_err <= rel_tol), abs_err, rel_err


@dataclass(frozen=True)
class BenchmarkValidator:
    """Validates a per-series final CSV against a dict of {year: book_value}."""

    series_id:        str
    tolerance_class:  str
    benchmarks:       dict[int, float]
    subseries_filter: str | None = None   # If set, validate book-period rows against this subseries_id
    # Extension-arm scoping (DIV-022): benchmark years AFTER `ext_year_after` are
    # validated against `ext_subseries_filter` (the -COMBINED/-EXT arm) instead of
    # `subseries_filter` (the -A book arm). This lets one registry reference_values
    # dict carry both book-period anchors and post-book extension anchors without
    # the extension anchors being reported MISSING by an -A-only filter.
    ext_subseries_filter: str | None = None
    ext_year_after:       int | None = None

    def run(self, final_csv: Path) -> dict:
        if not final_csv.exists():
            raise FileNotFoundError(f"{final_csv} missing — processor must run first")
        full = pd.read_csv(final_csv)
        if self.subseries_filter is not None:
            df = full[full["series_id"] == self.subseries_filter]
        else:
            df = full

        tol = TOLERANCES[self.tolerance_class]
        by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))

        # Extension-arm lookup (only built when configured).
        ext_by_year: dict[int, float] = {}
        if self.ext_subseries_filter is not None:
            ext_df = full[full["series_id"] == self.ext_subseries_filter]
            ext_by_year = dict(zip(ext_df["year"].astype(int), ext_df["value"].astype(float)))

        checks: list[dict] = []
        for yr, expected in self.benchmarks.items():
            if (self.ext_year_after is not None and yr > self.ext_year_after
                    and self.ext_subseries_filter is not None):
                actual = ext_by_year.get(yr)
            else:
                actual = by_year.get(yr)
            if actual is None:
                checks.append({"year": yr, "expected": expected, "actual": None, "status": "MISSING"})
                continue
            ok, abs_err, rel_err = _within_tol(actual, expected, rel_tol=tol["rel"], abs_tol=tol["abs"])
            checks.append({
                "year": yr, "expected": expected, "actual": round(actual, 6),
                "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
                "status": "PASS" if ok else "FAIL",
            })

        n_pass    = sum(1 for c in checks if c["status"] == "PASS")
        n_fail    = sum(1 for c in checks if c["status"] == "FAIL")
        n_missing = sum(1 for c in checks if c["status"] == "MISSING")
        status = "PASS" if (n_fail == 0 and n_missing == 0) else "FAIL"

        result = {
            "series_id": self.series_id,
            "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tolerance_class": self.tolerance_class,
            "rel_tol": tol["rel"], "abs_tol": tol["abs"],
            "status": status,
            "n_pass": n_pass, "n_fail": n_fail, "n_missing": n_missing,
            "benchmarks": {"checks": checks},
        }
        write_validation_result(self.series_id, result)
        return result


def cross_source_e2_check(
    series_id: str, h1_final_csv: Path, e2_file: Path, e2_column: str,
    subseries_filter: str, tolerance_class: str = "dollar_series",
) -> dict:
    """Duplicate-source consistency check: compare H.1-derived series to E.2 for overlap years.

    Used for S501-S510 (the revenue-account series): Table H.1 and Table E.2
    should report identical values for 1948-1961. Any divergence indicates a
    digitization error in one of the two tables.
    """
    if not e2_file.exists():
        return {"status": "SKIP", "reason": f"{e2_file.name} not present"}
    df = pd.read_csv(h1_final_csv)
    df = df[df["series_id"] == subseries_filter]
    e2 = read_book_table(e2_file)
    if e2_column not in e2.columns:
        return {"status": "SKIP", "reason": f"Column {e2_column} missing from E.2"}
    e2 = e2.rename(columns={e2.columns[0]: "year"})
    by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))
    tol = TOLERANCES[tolerance_class]
    mismatches: list[dict] = []
    compared = 0
    for _, row in e2.iterrows():
        try:
            yr = int(row["year"])
        except (ValueError, TypeError):
            continue
        if yr not in by_year:
            continue
        compared += 1
        expected = float(row[e2_column])
        ok, abs_err, rel_err = _within_tol(by_year[yr], expected, rel_tol=tol["rel"], abs_tol=tol["abs"])
        if not ok:
            mismatches.append({
                "year": yr, "H1": by_year[yr], "E2": expected,
                "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
            })
    return {
        "status": "PASS" if not mismatches else "FAIL",
        "compared_years": compared,
        "mismatches": mismatches,
    }


def run_pipeline_for_series(loader: BookColumnLoader, source_label: str) -> Path:
    """Standard run sequence: load -> process -> write intermediate + final CSV."""
    final = standard_passthrough_processor(loader, source_label)
    write_series_csv(final, loader.series_id, stage="intermediate")
    final_path = write_series_csv(final, loader.series_id, stage="final")
    return final_path

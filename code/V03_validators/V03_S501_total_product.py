"""V03_S501 — Validate Total Product (TP*) against book reference values.

Reference values from Appendix H.1 / E.2 (Shaikh & Tonak 1994). Tolerance class
is `dollar_series` (relative 0.01, absolute 1.0). Also performs a cross-source
duplicate check against the page-310 Table E.2 extraction for the 1948-1961
overlap, which catches any digitization error in either source.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import read_book_table, write_validation_result
from utils.paths import BOOK_TABLES, DATA_FINAL


SERIES_ID = "S501"
TOLERANCE_CLASS = "dollar_series"
REL_TOL = 0.01
ABS_TOL = 1.0

# Reference values from Appendix H.1 (S&T 1994), billions current $
BOOK_BENCHMARKS = {
    1948: 446.21,
    1958: 711.67,
    1961: 811.42,
}


def _within_tol(actual: float, expected: float) -> tuple[bool, float, float]:
    abs_err = abs(actual - expected)
    rel_err = abs_err / max(abs(expected), 1e-12)
    return (abs_err <= ABS_TOL or rel_err <= REL_TOL), abs_err, rel_err


def validate_benchmarks(series: pd.DataFrame) -> dict:
    """Check series values against published Appendix H.1 reference values."""
    checks: list[dict] = []
    series = series[series["series_id"].str.startswith(SERIES_ID)]
    by_year = dict(zip(series["year"].astype(int), series["value"].astype(float)))
    for yr, expected in BOOK_BENCHMARKS.items():
        actual = by_year.get(yr)
        if actual is None:
            checks.append({"year": yr, "expected": expected, "actual": None, "status": "MISSING"})
            continue
        ok, abs_err, rel_err = _within_tol(actual, expected)
        checks.append({
            "year": yr, "expected": expected, "actual": round(actual, 4),
            "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
            "status": "PASS" if ok else "FAIL",
        })
    return {"checks": checks, "n_pass": sum(1 for c in checks if c["status"] == "PASS"),
            "n_fail": sum(1 for c in checks if c["status"] == "FAIL"),
            "n_missing": sum(1 for c in checks if c["status"] == "MISSING")}


def cross_source_check(series: pd.DataFrame) -> dict:
    """Duplicate-source consistency check against Table E.2 (1948-1961 subset)."""
    e2_path = BOOK_TABLES / "TableE2_RevenueAccounts_1948_1961.csv"
    if not e2_path.exists():
        return {"status": "SKIP", "reason": f"{e2_path.name} not present"}
    e2 = read_book_table(e2_path)
    if "TP_star" not in e2.columns:
        return {"status": "SKIP", "reason": "TP_star column missing from E.2 file"}
    # E.2 has the year column unnamed (first column after the comment row)
    e2 = e2.rename(columns={e2.columns[0]: "year"})
    series_book = series[series["series_id"] == "S501-A"]
    series_by_year = dict(zip(series_book["year"].astype(int), series_book["value"].astype(float)))
    mismatches: list[dict] = []
    compared = 0
    for _, row in e2.iterrows():
        yr = int(row["year"])
        if yr not in series_by_year:
            continue
        compared += 1
        expected = float(row["TP_star"])
        actual = series_by_year[yr]
        ok, abs_err, rel_err = _within_tol(actual, expected)
        if not ok:
            mismatches.append({"year": yr, "H1": actual, "E2": expected,
                               "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6)})
    return {"status": "PASS" if not mismatches else "FAIL",
            "compared_years": compared,
            "mismatches": mismatches}


def run() -> dict:
    final_csv = DATA_FINAL / f"{SERIES_ID}.csv"
    if not final_csv.exists():
        raise FileNotFoundError(f"{final_csv} missing — run P02_{SERIES_ID} first")
    df = pd.read_csv(final_csv)

    benchmark_result = validate_benchmarks(df)
    cross_result = cross_source_check(df)

    n_fail = benchmark_result["n_fail"] + (1 if cross_result.get("status") == "FAIL" else 0)
    n_pass = benchmark_result["n_pass"] + (1 if cross_result.get("status") == "PASS" else 0)
    status = "PASS" if n_fail == 0 and benchmark_result["n_missing"] == 0 else "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": TOLERANCE_CLASS,
        "rel_tol": REL_TOL, "abs_tol": ABS_TOL,
        "status": status,
        "n_pass": n_pass, "n_fail": n_fail,
        "benchmarks": benchmark_result,
        "cross_source_E2_vs_H1": cross_result,
    }
    out_path = write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} benchmarks_pass={benchmark_result['n_pass']}/{len(BOOK_BENCHMARKS)}; "
          f"cross_check={cross_result.get('status')}; report={out_path.name}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

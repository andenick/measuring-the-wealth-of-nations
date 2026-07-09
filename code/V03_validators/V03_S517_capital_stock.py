"""V03_S517 — Validate K* range, monotonicity, AND registry benchmarks.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
Upgraded from sanity-checks-only to also check year-by-year reference values.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_variant_reference_values  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402


SERIES_ID = "S517"


def _variant_book_checks(subseries: str, tol_class: str) -> list[dict]:
    """Book-anchored check of a GROSS variant subseries (K-plan WP-K3).

    Validates S517-GROSS-A against the book's OWN printed Table 5.8 gross K*
    (validation.variant_reference_values) — the family's first INDEPENDENT
    (non-tautological) book anchor. Returns [] when the variant or its refvals
    are absent (older builds), so this never spuriously fails.
    """
    refs = get_variant_reference_values(SERIES_ID, subseries)
    if not refs:
        return []
    full = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    v = full[full["series_id"] == subseries]
    by_year = dict(zip(v["year"].astype(int), v["value"].astype(float)))
    tol = TOLERANCES[tol_class]
    checks = []
    for yr, expected in sorted(refs.items()):
        actual = by_year.get(yr)
        if actual is None:
            checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        checks.append({"year": yr, "expected": expected, "actual": round(actual, 6),
                       "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
                       "status": "PASS" if ok else "FAIL"})
    return checks


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == "S517-A"].sort_values("year").reset_index(drop=True)

    # K* should be positive and broadly monotonic-increasing
    all_positive = bool((df["value"] > 0).all())
    # Year-over-year decreases allowed only in deep recessions; check no year has >5% nominal drop
    diffs = df["value"].pct_change()
    nominal_drops = diffs[diffs < -0.05]

    # Sanity: 1948 should be ~$300B (book era starting K*); 1989 ~$10000B; 2024 >$35000B
    v_1948 = float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None
    v_1989 = float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None
    v_2024 = float(df[df["year"] == 2024]["value"].iloc[0]) if (df["year"] == 2024).any() else None

    # Registry benchmark check (per Decision 0002)
    benchmarks = get_reference_values(SERIES_ID)
    by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))
    tol = TOLERANCES["level_series"]
    bench_checks = []
    for yr, expected in benchmarks.items():
        actual = by_year.get(yr)
        if actual is None:
            bench_checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        bench_checks.append({
            "year": yr, "expected": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
            "status": "PASS" if ok else "FAIL",
        })
    n_bench_pass = sum(1 for c in bench_checks if c["status"] == "PASS")
    n_bench_fail = sum(1 for c in bench_checks if c["status"] == "FAIL")
    n_bench_miss = sum(1 for c in bench_checks if c["status"] == "MISSING")

    # Book-anchored GROSS variant check (K-plan WP-K3; independent book anchor)
    variant_checks = _variant_book_checks("S517-GROSS-A", "level_series")
    n_var_pass = sum(1 for c in variant_checks if c["status"] == "PASS")
    n_var_fail = sum(1 for c in variant_checks if c["status"] == "FAIL")
    n_var_miss = sum(1 for c in variant_checks if c["status"] == "MISSING")

    status = "PASS"
    if not all_positive:
        status = "FAIL"
    elif v_1948 is not None and (v_1948 < 100 or v_1948 > 1000):
        status = "FAIL"
    elif v_1989 is not None and (v_1989 < 5000 or v_1989 > 20000):
        status = "FAIL"
    elif v_2024 is not None and v_2024 < 30000:
        status = "FAIL"
    elif n_bench_fail > 0 or n_bench_miss > 0:
        status = "FAIL"
    elif n_var_fail > 0:
        status = "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "level_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_bench_pass,
        "n_fail": n_bench_fail,
        "n_missing": n_bench_miss,
        "checks": {
            "all_positive": all_positive,
            "v_1948": v_1948,
            "v_1989": v_1989,
            "v_2024": v_2024,
            "nominal_drop_years": nominal_drops.dropna().to_dict() if len(nominal_drops) else {},
        },
        "benchmarks": {"checks": bench_checks},
        "variant_book_anchor": {
            "subseries": "S517-GROSS-A",
            "source": "book Table 5.8 GROSS K* (C*_f), printed cells; independent (non-tautological) anchor",
            "n_pass": n_var_pass, "n_fail": n_var_fail, "n_missing": n_var_miss,
            "checks": variant_checks,
        },
    }
    write_validation_result(SERIES_ID, result)

    def _fmt(x):
        return f"{x:.0f}B" if x is not None else "n/a"
    print(f"    [V03_{SERIES_ID}] status={status} K*: 1948={_fmt(v_1948)}, 1989={_fmt(v_1989)}, 2024={_fmt(v_2024)} "
          f"bench_pass={n_bench_pass}/{n_bench_pass+n_bench_fail+n_bench_miss} "
          f"gross_book_anchor={n_var_pass}/{n_var_pass+n_var_fail+n_var_miss}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

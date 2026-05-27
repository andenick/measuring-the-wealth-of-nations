"""V03_S510 — Validate K/V* range AND registry benchmarks.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
Upgraded from skeleton (range-only) to a proper validator that also checks
year-by-year reference values from the registry.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S510.csv")
    df = df[df["series_id"] == "S510-A"]
    # K/V should be in [1, 30] for productive economy (book Table 5.10)
    in_range = bool(df["value"].between(1, 30).all())

    # Registry benchmark check (per Decision 0002)
    benchmarks = get_reference_values("S510")
    by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))
    tol = TOLERANCES["rate_series"]
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

    status = "PASS" if (in_range and len(df) > 0 and n_bench_fail == 0 and n_bench_miss == 0) else "FAIL"
    result = {
        "series_id": "S510",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_bench_pass,
        "n_fail": n_bench_fail,
        "n_missing": n_bench_miss,
        "range_check": {"expected": [1, 30], "actual_min": float(df["value"].min()), "actual_max": float(df["value"].max()), "in_range": in_range},
        "benchmarks": {"checks": bench_checks},
    }
    write_validation_result("S510", result)
    print(f"    [V03_S510] status={status} K/V*: range=[{df['value'].min():.2f}, {df['value'].max():.2f}] bench_pass={n_bench_pass}/{n_bench_pass+n_bench_fail+n_bench_miss}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_S513 — Validate Marxian profit rate (stock-form) range + secular trend + registry benchmarks.

v1.2 Iter 3 (2026-05-24): Validates S513-COMBINED (stock-form primary across full
1948-2024 span per VPR_S513_stock_vs_flow_DECISION_BRIEF). Prior version validated
only S513-A book period.

Reads benchmarks from registry (`validation.reference_values`) via
`utils.registry_validator.get_reference_values`. Benchmarks refreshed in v1.2
Iter 3 to stock-form endpoints at 1948, 1989, 2024.

The secondary S513-FLOW subseries is intentionally NOT validated by V03; it is
a reference variant whose published values are documented in the EPR/VPR but
are not the headline series.
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
    df_all = pd.read_csv(DATA_FINAL / "S513.csv")
    # Validate the COMBINED stock-form series across the full span.
    df = df_all[df_all["series_id"] == "S513-COMBINED"].sort_values("year").copy()

    # r* should be in [0.05, 1.0] over full 1948-2024 span (stock-form range)
    in_range = bool(df["value"].between(0.05, 1.0).all())

    # Secular trend: stock-form decline 1948 -> 2024 (book TRPF narrative)
    by_year = dict(zip(df["year"].astype(int), df["value"].astype(float)))
    v_1948 = by_year.get(1948)
    v_1989 = by_year.get(1989)
    v_2024 = by_year.get(2024)
    trend_1948_1989 = (v_1989 < v_1948) if (v_1948 and v_1989) else None
    trend_1948_2024 = (v_2024 < v_1948) if (v_1948 and v_2024) else None

    # Registry benchmark check (per Decision 0002)
    benchmarks = get_reference_values("S513")
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
        "series_id": "S513",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_bench_pass,
        "n_fail": n_bench_fail,
        "n_missing": n_bench_miss,
        "checks": {
            "validated_subseries": "S513-COMBINED",
            "form": "stock_primary (r* = S* / (K* + V*))",
            "in_range": in_range, "range_expected": [0.05, 1.0],
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": v_1948, "v_1989": v_1989, "v_2024": v_2024,
            "secular_decline_1948_to_1989": trend_1948_1989,
            "secular_decline_1948_to_2024": trend_1948_2024,
        },
        "benchmarks": {"checks": bench_checks},
    }
    write_validation_result("S513", result)
    print(
        f"    [V03_S513] status={status} stock-form r*: "
        f"1948={v_1948:.4f}, 1989={v_1989:.4f}, 2024={v_2024:.4f}; "
        f"decline_to_2024={trend_1948_2024}; bench_pass={n_bench_pass}/"
        f"{n_bench_pass + n_bench_fail + n_bench_miss}"
    )
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

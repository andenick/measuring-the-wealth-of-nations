"""V03_S701 — productive labor coefficient lambda_p (v1.1 Phase 5 polish).

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from the registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.

v1.1 Phase 5 update: per-sector consistent-procedure lambda_p (P02_S701 iter6)
is now defined on both the -A book-period subseries (1958, 1963, 1967, 1972,
1977 SIC benchmarks) and the -EXT subseries (1990-2024 annual). The validator
must look across both subseries so the 2024 EXT endpoint check (per Decision
0008) succeeds.

Dimensional check: lambda_p in hr/$ should be positive and finite. The
range is intentionally wide (0.001-100 hr/$) because sector coverage varies
with the benchmark year; the year-anchored reference-value check is the
load-bearing assertion.
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values
from utils.series import TOLERANCES


def _load_combined(sid: str) -> dict[int, float]:
    """Load year -> value lookup across -A, -EXT, -COMBINED subseries.

    Preference order: -COMBINED first (canonical full timeline), else union of
    -A and -EXT (older registries may not write -COMBINED).
    """
    df = pd.read_csv(DATA_FINAL / f"{sid}.csv")
    combined_id = f"{sid}-COMBINED"
    if (df["series_id"] == combined_id).any():
        sub = df[df["series_id"] == combined_id]
    else:
        sub = df[df["series_id"].isin([f"{sid}-A", f"{sid}-EXT"])]
    sub = sub.dropna(subset=["value"])
    return dict(zip(sub["year"].astype(int), sub["value"].astype(float)))


def run():
    by_year = _load_combined("S701")
    values = pd.Series(by_year)
    in_range = bool(values.between(0.001, 100).all()) if len(values) else False

    # Registry benchmark check (per Decision 0002)
    benchmarks = get_reference_values("S701")
    tol = TOLERANCES["rate_series"]
    bench_checks = []
    for yr, expected in benchmarks.items():
        actual = by_year.get(int(yr))
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

    status = "PASS" if (in_range and len(by_year) > 0 and n_bench_fail == 0 and n_bench_miss == 0) else "FAIL"
    result = {
        "series_id": "S701",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "rel_tol": tol["rel"], "abs_tol": tol["abs"],
        "status": status,
        "n_pass": n_bench_pass, "n_fail": n_bench_fail, "n_missing": n_bench_miss,
        "range_check": {
            "expected": [0.001, 100],
            "actual": [float(values.min()), float(values.max())] if len(values) else [None, None],
            "in_range": in_range,
        },
        "benchmarks": {"checks": bench_checks},
    }
    write_validation_result("S701", result)
    rng_lo = f"{values.min():.4f}" if len(values) else "NA"
    rng_hi = f"{values.max():.4f}" if len(values) else "NA"
    n_total = n_bench_pass + n_bench_fail + n_bench_miss
    print(f"    [V03_S701] status={status} range=[{rng_lo}, {rng_hi}] hr/$ bench_pass={n_bench_pass}/{n_total}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

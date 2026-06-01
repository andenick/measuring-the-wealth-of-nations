"""V03_S402 — B trace >= n check + registry benchmark check on b_frobenius_norm.

Refactored 2026-05-24 per Decision 0002 — augmented with registry-sourced
benchmark check (validation.reference_values stores b_frobenius_norm by year).
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values, get_tolerance_class
from utils.series import TOLERANCES

def run():
    df = pd.read_csv(DATA_FINAL / "S402.csv")
    trace_ok = bool((df["b_trace"] >= df["n_sectors"] - 0.01).all())

    bench_dict = get_reference_values("S402")
    tol_class = get_tolerance_class("S402", default="rate_series")
    tol = TOLERANCES[tol_class]
    by_year = dict(zip(df["year"].astype(int), df["b_frobenius_norm"].astype(float)))
    checks = []
    for yr, expected in bench_dict.items():
        actual = by_year.get(yr)
        if actual is None:
            checks.append({"year": yr, "expected": expected, "actual": None, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"] or rel_err <= tol["rel"])
        checks.append({"year": yr, "expected": expected, "actual": round(actual, 6),
                       "abs_err": round(abs_err, 6), "rel_err": round(rel_err, 6),
                       "status": "PASS" if ok else "FAIL"})
    n_bp = sum(1 for c in checks if c["status"] == "PASS")
    n_bf = sum(1 for c in checks if c["status"] == "FAIL")
    n_bm = sum(1 for c in checks if c["status"] == "MISSING")
    bench_pass = (n_bf == 0 and n_bm == 0)

    rule_pass = trace_ok and len(df) > 0
    status = "PASS" if (rule_pass and bench_pass) else "FAIL"
    result = {
        "series_id": "S402",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": tol_class,
        "status": status,
        "n_pass": n_bp + (1 if rule_pass else 0),
        "n_fail": n_bf + (0 if rule_pass else 1),
        "n_missing": n_bm,
        "checks": {
            "b_trace_ge_n": trace_ok,
            "n_benchmark_years": len(df),
            "frobenius_range": [float(df["b_frobenius_norm"].min()), float(df["b_frobenius_norm"].max())],
        },
        "benchmarks": {"target_column": "b_frobenius_norm", "checks": checks},
    }
    write_validation_result("S402", result)
    print(f"    [V03_S402] status={status} trace_ge_n={trace_ok}; bench={n_bp}/{n_bp+n_bf+n_bm}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

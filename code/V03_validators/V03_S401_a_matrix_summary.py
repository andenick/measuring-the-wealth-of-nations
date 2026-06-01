"""V03_S401 — Hawkins-Simon condition + registry benchmark check on max_eigenvalue.

Refactored 2026-05-24 per Decision 0002 — augmented with registry-sourced
benchmark check (validation.reference_values stores max_eigenvalue by year).
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import TOLERANCES  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S401.csv")
    # Hawkins-Simon: max eigenvalue must be < 1 for productive economy
    hs_ok = bool((df["max_eigenvalue"] < 1.0).all())
    # Sparsity in [0, 1]
    sp_ok = bool(df["sparsity"].between(0, 1).all())

    # Registry benchmark check (max_eigenvalue by year).
    bench_dict = get_reference_values("S401")
    tol_class = get_tolerance_class("S401", default="rate_series")
    tol = TOLERANCES[tol_class]
    by_year = dict(zip(df["year"].astype(int), df["max_eigenvalue"].astype(float)))
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

    rule_pass = hs_ok and sp_ok
    status = "PASS" if (rule_pass and bench_pass) else "FAIL"
    result = {
        "series_id": "S401",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": tol_class,
        "status": status,
        "n_pass": n_bp + (1 if rule_pass else 0),
        "n_fail": n_bf + (0 if rule_pass else 1),
        "n_missing": n_bm,
        "checks": {
            "hawkins_simon_all_lt_1": hs_ok,
            "max_eig_max": float(df["max_eigenvalue"].max()),
            "sparsity_in_unit_interval": sp_ok,
            "n_benchmark_years": len(df),
        },
        "benchmarks": {"target_column": "max_eigenvalue", "checks": checks},
    }
    write_validation_result("S401", result)
    print(f"    [V03_S401] status={status} HS_ok={hs_ok} max_eig_max={df['max_eigenvalue'].max():.6f}; bench={n_bp}/{n_bp+n_bf+n_bm}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

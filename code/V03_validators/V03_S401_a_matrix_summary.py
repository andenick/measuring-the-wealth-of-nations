"""V03_S401 -- rebuilt A-matrix summary (spectral radius) validator (workpackage C v2.0).

DE-TAUTOLOGIZED: the load-bearing assertions are matrix-internal invariants of
the REBUILT cache, not a copy of the series' own output:
  1. Hawkins-Simon viability: spectral radius of every rebuilt A < 1 with real
     margin (< 0.9) -- the defective cache sat at 0.95-0.98 by construction.
  2. Internal identity: stored L equals (I-A)^-1 (leontief_max_dev < 1e-6).
  3. Regression snapshot vs registry reference_values (pipeline snapshot).
S401 remains publish:false (a scalar summary of a matrix is not a series; the
matrix artifacts live in io_matrices_rebuilt/).
validator_class: matrix_internal__structural
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
    df = pd.read_csv(DATA_FINAL / "S401.csv")
    hs_ok = bool((df["max_eigenvalue"] < 0.9).all())
    ident_ok = bool((df["leontief_max_dev"].dropna() < 1e-6).all())
    sp_ok = bool(df["sparsity"].between(0, 1).all())

    tol = TOLERANCES["rate_series"]
    by_year = dict(zip(df["year"].astype(int), df["max_eigenvalue"].astype(float)))
    checks = []
    for yr, expected in get_reference_values("S401").items():
        actual = by_year.get(int(yr))
        if actual is None:
            checks.append({"year": yr, "expected": expected, "status": "MISSING"})
            continue
        abs_err = abs(actual - expected)
        rel_err = abs_err / max(abs(expected), 1e-12)
        ok = (abs_err <= tol["abs"]) or (rel_err <= tol["rel"])
        checks.append({"year": yr, "expected": expected, "actual": round(actual, 6),
                       "status": "PASS" if ok else "FAIL"})
    n_fail = sum(1 for c in checks if c["status"] != "PASS")

    status = "PASS" if (hs_ok and ident_ok and sp_ok and n_fail == 0) else "FAIL"
    result = {
        "series_id": "S401",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "validator_class": "matrix_internal__structural",
        "status": status,
        "hawkins_simon_lt_0p9": hs_ok,
        "internal_identity_lt_1e6": ident_ok,
        "sparsity_ok": sp_ok,
        "benchmarks": {"checks": checks, "n_fail": n_fail},
    }
    write_validation_result("S401", result)
    print(f"    [V03_S401] status={status} HS<0.9={hs_ok} identity={ident_ok} snapshot_fail={n_fail}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

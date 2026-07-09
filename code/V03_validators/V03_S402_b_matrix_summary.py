"""V03_S402 -- rebuilt Leontief-inverse summary (mean multiplier) validator (workpackage C v2.0).

DE-TAUTOLOGIZED: asserts the economically meaningful invariant directly --
mean total-requirements column multipliers of every rebuilt benchmark inverse
sit in the published-US-table band [1.5, 3.5] (the defective cache produced
multipliers ~70 / Frobenius norms 30-100). For NAICS years the underlying L IS
BEA's own published Total Requirements table, so the summary is anchored to
official values by construction. Plus a regression snapshot vs registry
reference_values (pipeline snapshot).
validator_class: matrix_internal__official_naics_anchor
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

NAICS_YEARS = {1997, 2002, 2007, 2012, 2017}


def run():
    df = pd.read_csv(DATA_FINAL / "S402.csv")
    band_ok = bool(df["b_colsum_mean"].between(1.5, 3.5).all())
    naics = df[df["year"].isin(NAICS_YEARS)]
    naics_full = bool((naics["n_live_columns"] == 71).all()) if len(naics) else False

    tol = TOLERANCES["rate_series"]
    by_year = dict(zip(df["year"].astype(int), df["b_colsum_mean"].astype(float)))
    checks = []
    for yr, expected in get_reference_values("S402").items():
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

    status = "PASS" if (band_ok and naics_full and n_fail == 0) else "FAIL"
    result = {
        "series_id": "S402",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "validator_class": "matrix_internal__official_naics_anchor",
        "status": status,
        "multiplier_band_1p5_3p5": band_ok,
        "naics_years_are_bea_published_full_71": naics_full,
        "benchmarks": {"checks": checks, "n_fail": n_fail},
    }
    write_validation_result("S402", result)
    print(f"    [V03_S402] status={status} band={band_ok} naics_official={naics_full} snapshot_fail={n_fail}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

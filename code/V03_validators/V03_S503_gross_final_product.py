"""V03_S503 — Validate GFP against book benchmark, identity, and cross-source E.2.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import BenchmarkValidator, cross_source_e2_check, TOLERANCES  # noqa: E402
from utils.io import write_validation_result  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S503",
    tolerance_class  = "dollar_series",
    benchmarks       = get_reference_values("S503"),
    subseries_filter = "S503-A",
)


def identity_check() -> dict:
    """Check identity: GFP = TP* - C*_m  (i.e., S503 = S501 - S502) year by year."""
    s501 = pd.read_csv(DATA_FINAL / "S501.csv")
    s502 = pd.read_csv(DATA_FINAL / "S502.csv")
    s503 = pd.read_csv(DATA_FINAL / "S503.csv")
    if not all(p.exists() for p in (DATA_FINAL/"S501.csv", DATA_FINAL/"S502.csv", DATA_FINAL/"S503.csv")):
        return {"status": "SKIP", "reason": "S501/S502 not yet built"}

    s501 = s501[s501["series_id"] == "S501-A"][["year", "value"]].rename(columns={"value": "TP_star"})
    s502 = s502[s502["series_id"] == "S502-A"][["year", "value"]].rename(columns={"value": "C_star_m"})
    s503 = s503[s503["series_id"] == "S503-A"][["year", "value"]].rename(columns={"value": "GFP_star"})
    merged = s501.merge(s502, on="year").merge(s503, on="year")
    merged["implied"] = merged["TP_star"] - merged["C_star_m"]
    merged["abs_err"] = (merged["implied"] - merged["GFP_star"]).abs()

    tol = TOLERANCES["dollar_series"]
    fails = merged[merged["abs_err"] > tol["abs"]]
    return {
        "status": "PASS" if len(fails) == 0 else "FAIL",
        "identity": "GFP = TP* - C*_m",
        "compared_years": len(merged),
        "max_abs_err": float(merged["abs_err"].max()) if len(merged) else None,
        "fail_years": fails["year"].tolist(),
    }


def run():
    result = VALIDATOR.run(DATA_FINAL / "S503.csv")
    result["identity_check"] = identity_check()
    result["cross_source_E2_vs_H1"] = cross_source_e2_check(
        series_id        = "S503",
        h1_final_csv     = DATA_FINAL / "S503.csv",
        e2_file          = BOOK_TABLES / "TableE2_RevenueAccounts_1948_1961.csv",
        e2_column        = "GFP",
        subseries_filter = "S503-A",
    )
    write_validation_result("S503", result)
    id_status = result["identity_check"]["status"]
    cs_status = result["cross_source_E2_vs_H1"]["status"]
    print(f"    [V03_S503] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}; "
          f"identity={id_status}; cross={cs_status}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

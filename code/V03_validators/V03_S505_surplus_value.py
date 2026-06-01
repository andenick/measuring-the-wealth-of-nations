"""V03_S505 — Validate Surplus Value (S*) against book benchmarks + identity check.

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
from utils.series import BenchmarkValidator, TOLERANCES  # noqa: E402
from utils.io import read_book_table, write_validation_result  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S505",
    tolerance_class  = "dollar_series",
    benchmarks       = get_reference_values("S505"),
    subseries_filter = "S505-A",
)


def identity_check() -> dict:
    """Check S* = VA* - V* using S505 final CSV and H.1 VA_star column."""
    h1 = read_book_table(BOOK_TABLES / "book_tableH1_1948_1989.csv")
    s505 = pd.read_csv(DATA_FINAL / "S505.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")

    va = h1[["year", "VA_star"]]
    s505 = s505[s505["series_id"] == "S505-A"][["year", "value"]].rename(columns={"value": "S_star"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    merged = va.merge(s504, on="year").merge(s505, on="year")
    merged["implied"] = merged["VA_star"] - merged["V_star"]
    merged["abs_err"] = (merged["implied"] - merged["S_star"]).abs()

    tol = TOLERANCES["dollar_series"]
    fails = merged[merged["abs_err"] > tol["abs"]]
    return {
        "status": "PASS" if len(fails) == 0 else "FAIL",
        "identity": "S* = VA* - V*",
        "compared_years": len(merged),
        "max_abs_err": float(merged["abs_err"].max()) if len(merged) else None,
        "fail_years": fails["year"].tolist(),
    }


def run():
    result = VALIDATOR.run(DATA_FINAL / "S505.csv")
    result["identity_check"] = identity_check()
    write_validation_result("S505", result)
    id_st = result["identity_check"]["status"]
    print(f"    [V03_S505] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}; identity={id_st}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_S607 — Validate NSW + V06 overlap + regime-change check.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
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
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S607",
    tolerance_class  = "dollar_series",
    benchmarks       = get_reference_values("S607"),
    subseries_filter = "S607-A",
)


def regime_change_check() -> dict:
    """Headline finding: NSW negative through ~1991, then turns positive."""
    df = pd.read_csv(DATA_FINAL / "S607.csv")
    combined = df[df["series_id"] == "S607-COMBINED"].sort_values("year")
    positive = combined[combined["value"] > 0]
    if len(positive) == 0:
        return {"status": "FAIL", "note": "no positive years — extension data missing?"}
    first_positive = int(positive["year"].min())
    last_negative = int(combined[combined["value"] < 0]["year"].max()) if (combined["value"] < 0).any() else None
    return {
        "status": "PASS" if 1989 < first_positive < 2000 else "WARN",
        "first_positive_year": first_positive,
        "last_negative_year":  last_negative,
        "interpretation":      f"NSW turns POSITIVE in {first_positive}, after being negative 1952-{last_negative}",
    }


def run():
    result = VALIDATOR.run(DATA_FINAL / "S607.csv")
    result["regime_change_check"] = regime_change_check()
    write_validation_result("S607", result)
    rc = result["regime_change_check"]
    print(f"    [V03_S607] status={result['status']} bench_pass={result['n_pass']}/"
          f"{result['n_pass']+result['n_fail']+result['n_missing']} "
          f"regime_change=first_positive_year={rc.get('first_positive_year')}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

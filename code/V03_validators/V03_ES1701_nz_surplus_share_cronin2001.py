"""V03_ES1701 — Validate NZ Surplus Share of Total Value (Cronin 2001).

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
Unit note: registry stores decimals (0.34); the final CSV reports percent (34).
Benchmarks are scaled by 100 here so PASS/FAIL is meaningful. Resolve at the
registry level by adding a `validation.units_scale` field (out of scope for
this refactor — Decision 0002 forbids registry edits from V03 scripts).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


_RAW = get_reference_values("ES1701")
# Compensate for registry-vs-CSV unit mismatch (decimal -> percent).
_BENCH = {y: v * 100 for y, v in _RAW.items()}

VALIDATOR = BenchmarkValidator(
    series_id        = "ES1701",
    tolerance_class  = get_tolerance_class("ES1701", default="share_series"),
    benchmarks       = _BENCH,
    subseries_filter = "ES1701-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1701.csv")
    print(f"    [V03_ES1701] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

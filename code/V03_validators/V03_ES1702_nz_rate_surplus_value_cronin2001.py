"""V03_ES1702 — Validate NZ Rate of Surplus Value (Cronin 2001).

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
Unit note: registry stores decimal-ratio (2.06); final CSV reports percent (206).
Benchmarks scaled by 100 here; registry units field needs reconciliation.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


_RAW = get_reference_values("ES1702")
_BENCH = {y: v * 100 for y, v in _RAW.items()}

VALIDATOR = BenchmarkValidator(
    series_id        = "ES1702",
    tolerance_class  = get_tolerance_class("ES1702", default="rate_series"),
    benchmarks       = _BENCH,
    subseries_filter = "ES1702-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1702.csv")
    print(f"    [V03_ES1702] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

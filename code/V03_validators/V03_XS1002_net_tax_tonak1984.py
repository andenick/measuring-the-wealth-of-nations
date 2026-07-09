"""V03_XS1002 — Validate Net Tax on Labor (Tonak 1984).

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from
`series_registry.json` validation.reference_values.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "XS1002",
    tolerance_class  = get_tolerance_class("XS1002", default="dollar_series"),
    benchmarks       = get_reference_values("XS1002"),
    subseries_filter = "XS1002-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1002.csv")
    print(f"    [V03_XS1002] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

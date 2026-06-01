"""V03_S515 — Validate Productive Employment (Lp) against book TableE3 row directly.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.

Note: ST2's validation_config T515 benchmark of 17331.95 was in DOLLARS (wage bill
Lp*w). Our S515 is COUNT in thousands; the registry stores the TableE3 Lp_total
counts (1948 = 29937, 1961 = 33615), which is the correct unit for this series.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S515",
    tolerance_class  = "level_series",
    benchmarks       = get_reference_values("S515"),
    subseries_filter = "S515-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S515.csv")
    print(f"    [V03_S515] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

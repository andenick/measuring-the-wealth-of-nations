"""V03_S515 — Validate Productive Employment (Lp) against book TableE3 row directly."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


# Note: validation_config T515 benchmark of 17331.95 is in DOLLARS (the wage bill
# Lp*w?). Our S515 is COUNT in thousands. Use TableE3 published Lp_total values
# directly as benchmarks for the 14 known years.
VALIDATOR = BenchmarkValidator(
    series_id        = "S515",
    tolerance_class  = "level_series",
    # TableE3 Lp_total row, 1948 = 29937, 1961 = 33615 (head/tail of the wide row)
    benchmarks       = {1948: 29937, 1961: 33615},
    subseries_filter = "S515-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S515.csv")
    print(f"    [V03_S515] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

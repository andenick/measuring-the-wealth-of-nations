"""V03_ES1704 — Validate NZ Total Value (Cronin 2001)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "ES1704",
    tolerance_class  = "dollar_series",
    benchmarks       = {1972: 10423},
    subseries_filter = "ES1704-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1704.csv")
    print(f"    [V03_ES1704] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

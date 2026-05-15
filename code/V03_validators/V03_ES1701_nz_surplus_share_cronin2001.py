"""V03_ES1701 — Validate NZ Surplus Share of Total Value (Cronin 2001)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "ES1701",
    tolerance_class  = "share_series",
    benchmarks       = {1972: 34},
    subseries_filter = "ES1701-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1701.csv")
    print(f"    [V03_ES1701] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

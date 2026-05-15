"""V03_ES1001 — Validate Labor Share of National Taxes (Tonak 1984)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "ES1001",
    tolerance_class  = "dollar_series",
    benchmarks       = {1952: 34.58, 1980: 456.39},
    subseries_filter = "ES1001-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1001.csv")
    print(f"    [V03_ES1001] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

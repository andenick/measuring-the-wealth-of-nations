"""V03_S605 — Validate Government Benefits to Workers (B_w) against book benchmark values."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S605",
    tolerance_class  = "dollar_series",
    benchmarks       = {1952: 10.994,  1989: 521.07},
    subseries_filter = "S605-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S605.csv")
    print(f"    [V03_S605] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

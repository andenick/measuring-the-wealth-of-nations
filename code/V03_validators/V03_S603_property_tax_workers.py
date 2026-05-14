"""V03_S603 — Validate Property Tax Workers against book benchmark values."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S603",
    tolerance_class  = "dollar_series",
    benchmarks       = {1952: 4.1925,  1989: 74.9315},
    subseries_filter = "S603-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S603.csv")
    print(f"    [V03_S603] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

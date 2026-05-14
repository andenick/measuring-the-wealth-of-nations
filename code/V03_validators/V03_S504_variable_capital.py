"""V03_S504 — Validate Variable Capital (V*) against book benchmarks."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S504",
    tolerance_class  = "dollar_series",
    benchmarks       = {1948: 88.41, 1972: 324.30, 1989: 1206.40},
    subseries_filter = "S504-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S504.csv")
    print(f"    [V03_S504] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_S511 — Validate Productive Labor Share (Lp/L) against book benchmarks."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S511",
    tolerance_class  = "share_series",
    benchmarks       = {1948: 0.57, 1958: 0.52, 1967: 0.51, 1977: 0.50, 1989: 0.36},
    subseries_filter = "S511-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S511.csv")
    print(f"    [V03_S511] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

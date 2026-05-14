"""V03_S516 — Validate Unproductive Employment Lu = L - Lp against E.3 row values."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


# 1948: L_total=66091, Lp_total=29937 -> Lu = 36154 thousand
# 1961: L_total=82827, Lp_total=33615 -> Lu = 49212 thousand
VALIDATOR = BenchmarkValidator(
    series_id        = "S516",
    tolerance_class  = "level_series",
    benchmarks       = {1948: 36154, 1961: 49212},
    subseries_filter = "S516-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S516.csv")
    print(f"    [V03_S516] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_ES1403 — Validate Variable Capital — Mohun Classification (Mohun 2005)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "ES1403",
    tolerance_class  = "rate_series",
    benchmarks       = {1948: 1112758.197},
    subseries_filter = "ES1403-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1403.csv")
    print(f"    [V03_ES1403] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

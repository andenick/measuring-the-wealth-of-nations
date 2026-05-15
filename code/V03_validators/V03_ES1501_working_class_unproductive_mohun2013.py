"""V03_ES1501 — Validate Working Class Unproductive Labor (Mohun 2013)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="ES1501", tolerance_class="level_series",
    benchmarks={1948: 6426.4746},
    subseries_filter="ES1501-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1501.csv")
    print(f"    [V03_ES1501] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_ES1502 — Validate Managerial Unproductive Labor (Mohun 2013)."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="ES1502", tolerance_class="level_series",
    benchmarks={1948: 7669.3547},
    subseries_filter="ES1502-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "ES1502.csv")
    print(f"    [V03_ES1502] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

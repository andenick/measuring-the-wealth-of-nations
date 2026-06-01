"""V03_S617 — Validate EC against H.1 row values.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="S617", tolerance_class="dollar_series",
    benchmarks=get_reference_values("S617"),
    subseries_filter="S617-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "S617.csv")
    print(f"    [V03_S617] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

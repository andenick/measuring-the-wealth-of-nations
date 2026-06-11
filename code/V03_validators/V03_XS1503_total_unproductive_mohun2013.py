"""V03_XS1503 — Validate Total Unproductive Labor (Mohun 2013).

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values, get_tolerance_class
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="XS1503",
    tolerance_class=get_tolerance_class("XS1503", default="level_series"),
    benchmarks=get_reference_values("XS1503"),
    subseries_filter="XS1503-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1503.csv")
    print(f"    [V03_XS1503] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

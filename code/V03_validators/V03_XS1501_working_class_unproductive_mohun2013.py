"""V03_XS1501 — Validate Mohun (2013) unproductive working-class employment share.

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
D4 REBUILD (2026-07-02): series is now a SHARE of total employment (Mohun Fig 2);
benchmarks 1964=0.251, 2007=0.300 are EXTERNAL Mohun anchors (non-tautological).
Default tolerance class -> share_series.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL
from utils.registry_validator import get_reference_values, get_tolerance_class
from utils.series import BenchmarkValidator

VALIDATOR = BenchmarkValidator(
    series_id="XS1501",
    tolerance_class=get_tolerance_class("XS1501", default="share_series"),
    benchmarks=get_reference_values("XS1501"),
    subseries_filter="XS1501-A",
)

def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1501.csv")
    print(f"    [V03_XS1501] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

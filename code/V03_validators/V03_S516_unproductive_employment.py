"""V03_S516 — Validate Unproductive Employment Lu = L - Lp against E.3 row values.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.

Reference values (registry): 1948: 36154, 1961: 49212 — derived as L - Lp from
TableE3 (1948: L_total=66091, Lp_total=29937; 1961: L_total=82827, Lp_total=33615).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S516",
    tolerance_class  = "level_series",
    benchmarks       = get_reference_values("S516"),
    subseries_filter = "S516-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S516.csv")
    print(f"    [V03_S516] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

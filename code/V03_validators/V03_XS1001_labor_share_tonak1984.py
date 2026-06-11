"""V03_XS1001 — Validate Labor Share of National Taxes (Tonak 1984).

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "XS1001",
    tolerance_class  = get_tolerance_class("XS1001", default="share_series"),
    benchmarks       = get_reference_values("XS1001"),
    subseries_filter = "XS1001-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1001.csv")
    print(f"    [V03_XS1001] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

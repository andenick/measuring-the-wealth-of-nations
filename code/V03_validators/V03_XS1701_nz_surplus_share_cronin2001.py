"""V03_XS1701 — Validate NZ Surplus Share of Total Value (Cronin 2001).

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
Units reconciled 2026-07-01 (workpackage E review, Group D): the registry
`validation.reference_values` now store PERCENT (34, 38, 38), matching the final
CSV (percent), the series `units:"percent"`, and Cronin (2001) Table 2 which
prints "34%", "38%". The former decimal-fraction refvals (0.34) and the *100
compensation hack applied here are RETIRED. Benchmarks are read from the registry
unchanged. NOTE: this V03 edit is paired with D_REGISTRY_PATCHES.json (decimal->
percent for XS1701); both must be applied together.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "XS1701",
    tolerance_class  = get_tolerance_class("XS1701", default="share_series"),
    benchmarks       = get_reference_values("XS1701"),
    subseries_filter = "XS1701-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1701.csv")
    print(f"    [V03_XS1701] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

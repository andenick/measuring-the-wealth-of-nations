"""V03_XS1703 — Validate NZ Value Composition of Capital (Cronin 2001).

Refactored 2026-05-24 per Decision 0002 — benchmarks sourced from registry.
Units reconciled 2026-07-01 (workpackage E review, Group D): registry
`validation.reference_values` now store PERCENT (293, 385, 397), matching the
final CSV (percent), `units:"percent"`, and Cronin (2001) Table 2 ("293%",
"397%"). The former decimal-ratio refvals (2.93) and the *100 compensation hack
are RETIRED; benchmarks are read from the registry unchanged. NOTE: paired with
D_REGISTRY_PATCHES.json (decimal->percent for XS1703) — apply both together.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values, get_tolerance_class  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "XS1703",
    tolerance_class  = get_tolerance_class("XS1703", default="rate_series"),
    benchmarks       = get_reference_values("XS1703"),
    subseries_filter = "XS1703-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "XS1703.csv")
    print(f"    [V03_XS1703] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

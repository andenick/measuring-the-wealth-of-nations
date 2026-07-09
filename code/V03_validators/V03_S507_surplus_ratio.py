"""V03_S507 — Validate Surplus Ratio against book benchmarks.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import BenchmarkValidator  # noqa: E402


# Book-faithful benchmarks: S*/Y = S*/(S*+V*) = e/(1+e).
#
# Derived directly from the book's published e (S506) values:
#   1948: e=1.70 -> S/Y = 1.70/2.70 = 0.6296
#   1989: e=2.44 -> S/Y = 2.44/3.44 = 0.7093
#
# predecessor-build's validation_config benchmark of 0.57/0.60 came from a NIPA-proxy
# source (`T509_surplus_ratio` in ExploitationComposition_1948_1989.csv),
# which is NOT the book's surplus ratio. Documented in
# Technical/MIGRATION/divergences_from_predecessor-build.md.
VALIDATOR = BenchmarkValidator(
    series_id        = "S507",
    tolerance_class  = "share_series",
    benchmarks       = get_reference_values("S507"),
    subseries_filter = "S507-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S507.csv")
    print(f"    [V03_S507] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

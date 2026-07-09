"""V03_S516 — Validate Unproductive Employment Lu = L - Lp against E.3 row values.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.

Reference values (registry, class=book): derived as L - Lp from TableE3
(= Table 5.5 = Appendix F Table F.1) over the full book period 1948-1989:
    1948 = 25307  (L 58301 - Lp 32994)
    1958 = 33416, 1967 = 42281, 1977 = 52318
    1989 = 72363  (L 113511 - Lp 41148)
Only the book arm S516-A is benchmark-validated (subseries_filter='S516-A'); the
extension S516-EXT = L - Lp (single book-anchored total-employment L incl. govt,
shared with S515; D2 rebuild) is validated by the independent-L identity + seam-
continuity tests in tests/test_identities.py, not by book benchmarks.
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

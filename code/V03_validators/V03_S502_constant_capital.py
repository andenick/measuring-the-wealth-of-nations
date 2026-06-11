"""V03_S502 — Validate Constant Capital (C*_m) against book benchmarks + cross-source E.2.

Refactored 2026-05-24 per Decision 0002 — reads benchmarks from registry
(`validation.reference_values`) via `utils.registry_validator.get_reference_values`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, DATA_FINAL  # noqa: E402
from utils.registry_validator import get_reference_values  # noqa: E402
from utils.series import BenchmarkValidator, cross_source_e2_check  # noqa: E402
from utils.io import write_validation_result  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id            = "S502",
    tolerance_class      = "dollar_series",
    benchmarks           = get_reference_values("S502"),
    subseries_filter     = "S502-A",
    # DIV-022: 1997/2010/2024 refvals belong to the extension arm; validate them
    # against S502-COMBINED (the book-year anchors 1948/1989 stay on S502-A).
    ext_subseries_filter = "S502-COMBINED",
    ext_year_after       = 1989,
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S502.csv")
    cross = cross_source_e2_check(
        series_id        = "S502",
        h1_final_csv     = DATA_FINAL / "S502.csv",
        e2_file          = BOOK_TABLES / "TableE2_RevenueAccounts_1948_1961.csv",
        e2_column        = "C_star_m",
        subseries_filter = "S502-A",
    )
    result["cross_source_E2_vs_H1"] = cross
    write_validation_result("S502", result)
    print(f"    [V03_S502] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}; "
          f"cross={cross['status']} ({cross.get('compared_years','-')} yrs)")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

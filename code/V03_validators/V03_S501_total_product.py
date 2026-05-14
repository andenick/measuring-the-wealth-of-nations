"""V03_S501 — Validate Total Product (TP*) against book benchmarks + cross-source E.2 check."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, DATA_FINAL  # noqa: E402
from utils.series import BenchmarkValidator, cross_source_e2_check  # noqa: E402


VALIDATOR = BenchmarkValidator(
    series_id        = "S501",
    tolerance_class  = "dollar_series",
    benchmarks       = {1948: 446.21, 1958: 711.67, 1961: 811.42},
    subseries_filter = "S501-A",
)


def run():
    result = VALIDATOR.run(DATA_FINAL / "S501.csv")
    cross = cross_source_e2_check(
        series_id        = "S501",
        h1_final_csv     = DATA_FINAL / "S501.csv",
        e2_file          = BOOK_TABLES / "TableE2_RevenueAccounts_1948_1961.csv",
        e2_column        = "TP_star",
        subseries_filter = "S501-A",
        tolerance_class  = "dollar_series",
    )
    result["cross_source_E2_vs_H1"] = cross
    # Re-write augmented result
    from utils.io import write_validation_result
    write_validation_result("S501", result)
    print(f"    [V03_S501] status={result['status']} bench_pass={result['n_pass']}/{result['n_pass']+result['n_fail']+result['n_missing']}; "
          f"cross={cross['status']} ({cross.get('compared_years','-')} yrs)")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

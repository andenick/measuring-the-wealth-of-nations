"""L01_S508 — Load Productive Consumption (CON*), 1948-1961.

Source: Appendix E.2, column `CON_star`. The book digitizes E.2 only for the
1948-1961 subset, so this series has limited coverage (14 years). Extension
to 1989 would require parsing the full E.2 from later book pages (not in
salvaged KB) or a methodological derivation from NIPA inputs.

Status: book_period_partial_1948_1961. Documented in DPR.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S508",
    subseries_id  = "S508-A",
    source_file   = BOOK_TABLES / "TableE2_RevenueAccounts_1948_1961.csv",
    source_column = "CON_star",
    units         = "billions_usd",
)


def run():
    df = LOADER.load()
    print(f"    [L01_{LOADER.series_id}] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.2f}, last={df.iloc[-1]['value']:.2f}")
    return df


if __name__ == "__main__":
    run()

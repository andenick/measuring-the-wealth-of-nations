"""L01_S509 — Load Productive Investment (IG*), 1948-1961.

Source: Appendix E.2, column `IG_star`. 14-year coverage. Extension to 1989
requires later-page E.2 data not in the salvaged KB; deferred.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S509",
    subseries_id  = "S509-A",
    source_file   = BOOK_TABLES / "TableE2_RevenueAccounts_1948_1961.csv",
    source_column = "IG_star",
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

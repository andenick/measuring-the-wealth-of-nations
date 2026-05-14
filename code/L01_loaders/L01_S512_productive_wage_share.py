"""L01_S512 — Load Productive Wage Share (V*/W) book-period series, 1948-1989.

Source: Book Table 5.7 (digitized as Table5_7_KeyRatios.csv), column `T512A`
(book values). V*/W is the share of total wage bill paid to productive labor.

The S511 (Lp/L) and S512 (V*/W) series are the two key ratios from Table 5.7
that drive most of the chapter's interpretive arguments and feed downstream
extension formulas (e.g., S506 extension uses e = 1.238/(V*/W) - 1).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S512",
    subseries_id  = "S512-A",
    source_file   = BOOK_TABLES / "Table5_7_KeyRatios.csv",
    source_column = "T512A",
    units         = "share",
)


def run():
    df = LOADER.load()
    print(f"    [L01_{LOADER.series_id}] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()

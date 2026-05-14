"""L01_S609 — Load NSW / National Income Share, book period (Ch6 NSW).

Source: Appendix Ch6 — `data/source/book_tables/Table6_3_NetSocialWage.csv`, column
`nsw_ni_share`. Source values already in share; no unit conversion.

Status: book_period (S607 has extension via Table6_3_Extended; others are
book-only).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S609",
    subseries_id  = "S609-A",
    source_file   = BOOK_TABLES / "Table6_3_NetSocialWage.csv",
    source_column = "nsw_ni_share",
    units         = "share",
    unit_scale    = 1.0,
)


def run():
    df = LOADER.load()
    print(f"    [L01_S609] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()

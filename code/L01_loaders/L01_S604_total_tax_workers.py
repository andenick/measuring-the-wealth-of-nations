"""L01_S604 — Load Total Tax Workers (T_w), book period (Ch6 NSW).

Source: Appendix Ch6 — `data/source/book_tables/Table6_1_TaxAccounts.csv`, column
`total_tax_workers`. Source values in MILLIONS; loader divides by 1000 for BILLIONS output, matching the registry's `units: billions_usd`.

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
    series_id     = "S604",
    subseries_id  = "S604-A",
    source_file   = BOOK_TABLES / "Table6_1_TaxAccounts.csv",
    source_column = "total_tax_workers",
    units         = "billions_usd",
    unit_scale    = 1000.0,
)


def run():
    df = LOADER.load()
    print(f"    [L01_S604] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()

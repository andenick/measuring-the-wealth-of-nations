"""L01_S505 — Load Surplus Value (S*) book-period series, 1948-1989.

Source: Appendix H.1, column `S_star`. Identity: S* = VA* - V* (also satisfied
by the H.1 columns VA_star and V_star, checked by V03_S505 identity_check).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S505",
    subseries_id  = "S505-A",
    source_file   = BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column = "S_star",
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

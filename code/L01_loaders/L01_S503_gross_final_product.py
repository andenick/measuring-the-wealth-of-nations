"""L01_S503 — Load Gross Final Product (GFP = TP* - C*_m), 1948-1989.

Source: Appendix H.1, column `GFP_star`. This is the published book series;
internally also satisfies the identity GFP = TP* - C*_m which V03 checks.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "S503",
    subseries_id  = "S503-A",
    source_file   = BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column = "GFP_star",
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

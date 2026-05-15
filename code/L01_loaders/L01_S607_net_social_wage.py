"""L01_S607 — Load Net Social Wage (NSW = B_w + G_w - T_w).

Loads both subseries:
- S607-A: book period 1952-1989 from `Table6_3_NetSocialWage.csv`
- S607-B: extension 1990-2024 from `Table6_3_Extended.csv` (same column,
   same methodology — extension is direct continuation, not a proxy)

Source values in MILLIONS; loader divides by 1000 for BILLIONS output.

Headline regime change preserved: NSW negative through 1989, turns POSITIVE
in the early 1990s as transfer programs expand faster than worker tax burden.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader


LOADER_A = BookColumnLoader(
    series_id     = "S607",
    subseries_id  = "S607-A",
    source_file   = BOOK_TABLES / "Table6_3_NetSocialWage.csv",
    source_column = "nsw",
    units         = "billions_usd",
    unit_scale    = 1000.0,
)

LOADER_B = BookColumnLoader(
    series_id     = "S607",
    subseries_id  = "S607-B",
    source_file   = BOOK_TABLES / "Table6_3_Extended.csv",
    source_column = "nsw",
    units         = "billions_usd",
    unit_scale    = 1000.0,
)

# Maintain `LOADER` as alias for backward compatibility with P02_S607.
LOADER = LOADER_A


def run():
    df_a = LOADER_A.load()
    df_b = LOADER_B.load()
    # Restrict B to 1990 onwards (overlap years 1952-1989 are in A)
    df_b = df_b[df_b["year"] >= 1990].copy()
    print(f"    [L01_S607-A] {len(df_a)} rows {df_a['year'].min()}-{df_a['year'].max()}; "
          f"first={df_a.iloc[0]['value']:.4f}, last={df_a.iloc[-1]['value']:.4f}")
    print(f"    [L01_S607-B] {len(df_b)} rows {df_b['year'].min()}-{df_b['year'].max()}; "
          f"first={df_b.iloc[0]['value']:.4f}, last={df_b.iloc[-1]['value']:.4f}")
    return df_a, df_b


if __name__ == "__main__":
    run()

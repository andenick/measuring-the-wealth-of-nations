"""L01_S607 — Load Net Social Wage (NSW = B_w + G_w - T_w).

Loads both subseries:
- S607-A:   book period 1952-1989 from `Table6_3_NetSocialWage.csv`
- S607-EXT: extension 1990-2025 from `Table6_3_Extended.csv` (same column,
            same methodology — extension is direct continuation, not a proxy)

Source values in MILLIONS; loader divides by 1000 for BILLIONS output.

Headline regime change preserved: NSW negative through 1989, turns POSITIVE
in the early 1990s as transfer programs expand faster than worker tax burden.

Naming note: legacy code emitted subseries `S607-B` for the extension. Per the
Decision 0003 cleanup + the project convention on extension subseries
use `-EXT` and `-COMBINED` suffixes (not `-B`). Renamed during 2026-05-23
Stage 5 cohort 2.
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

LOADER_EXT = BookColumnLoader(
    series_id     = "S607",
    subseries_id  = "S607-EXT",
    source_file   = BOOK_TABLES / "Table6_3_Extended.csv",
    source_column = "nsw",
    units         = "billions_usd",
    unit_scale    = 1000.0,
)

# Backward-compat aliases (do not use in new code).
LOADER = LOADER_A
LOADER_B = LOADER_EXT


def run():
    df_a   = LOADER_A.load()
    df_ext = LOADER_EXT.load()
    # Restrict EXT to 1990 onwards (overlap years 1952-1989 are in A)
    df_ext = df_ext[df_ext["year"] >= 1990].copy()
    print(f"    [L01_S607-A]   {len(df_a)} rows {df_a['year'].min()}-{df_a['year'].max()}; "
          f"first={df_a.iloc[0]['value']:.4f}, last={df_a.iloc[-1]['value']:.4f}")
    print(f"    [L01_S607-EXT] {len(df_ext)} rows {df_ext['year'].min()}-{df_ext['year'].max()}; "
          f"first={df_ext.iloc[0]['value']:.4f}, last={df_ext.iloc[-1]['value']:.4f}")
    return df_a, df_ext


if __name__ == "__main__":
    run()

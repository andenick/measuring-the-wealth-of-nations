"""L01_S515 — Load Productive Employment (Lp).

Book-period source: Appendix E.3 (digitized as TableE3_LaborStatistics.csv), row
`Lp_total`. Covers 1948-1961 in the salvaged KB digitization (NARROW
classification, Lp/L = 0.45 at 1948).

Extension source: BLS CES super-sector aggregation
(sum of mining/logging + construction + manufacturing production workers,
in thousands), 1948-2024.

The extension uses the 5-super-sector CES cache. The book's Appendix C uses
85 SIC sectors and also includes transportation/public utilities and
productive services — the super-sector cache cannot reproduce that finer
partition. This divergence is documented in S515_EPR.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES  # noqa: E402
from utils.io import read_book_table  # noqa: E402
from utils.bls_cache import productive_employment_annual  # noqa: E402


SERIES_ID = "S515"
SUBSERIES = "S515-A"
SOURCE_FILE = BOOK_TABLES / "TableE3_LaborStatistics.csv"
SOURCE_ROW_LABEL = "Lp_total"


def load() -> pd.DataFrame:
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source data missing: {SOURCE_FILE}")
    df = read_book_table(SOURCE_FILE)
    # E.3 first column is unnamed (`Unnamed: 0`), second is `Sector`.
    df = df.rename(columns={df.columns[0]: "row_idx"})
    if "Sector" not in df.columns:
        raise KeyError(f"Expected 'Sector' column in {SOURCE_FILE.name}; got {list(df.columns)[:5]}")
    row = df[df["Sector"] == SOURCE_ROW_LABEL]
    if row.empty:
        raise KeyError(f"Row '{SOURCE_ROW_LABEL}' not found in {SOURCE_FILE.name}")

    year_cols = [c for c in df.columns if c.isdigit() and 1900 <= int(c) <= 2100]
    out = pd.DataFrame({
        "year":      [int(c) for c in year_cols],
        "value":     [float(row.iloc[0][c]) for c in year_cols],
    })
    out["series_id"] = SUBSERIES
    out["units"]     = "thousands"
    return out[["series_id", "year", "value", "units"]].reset_index(drop=True)


def load_extension_raw() -> pd.DataFrame:
    """Load the raw (unspliced) BLS productive employment series, 1948-2024.

    Returns DataFrame [year, value] in thousands. value = sum of production
    workers across the goods-producing super-sectors (mining/logging +
    construction + manufacturing) per the BLS CES cache.

    This raw super-sector production-worker count is the honest, BLS-native
    constructible measure retained as the S515-EXT-CONSTRUCTIBLE arm in the
    D2 seam redesign (distinct measure, break-flagged) — NOT the published Lp.
    """
    return productive_employment_annual().reset_index(drop=True)


def load_book_L_total() -> pd.DataFrame:
    """Load the book total-employment L (TableE3 row `L_total`), 1948-1989.

    This is the book's L universe (total labor over all sectors incl.
    government, Table 5.5 / Appendix F Table F.1). Used as the 1989 anchor for
    the extension L re-anchoring in P02_S515/P02_S516. Returns [year, value].
    """
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source data missing: {SOURCE_FILE}")
    df = read_book_table(SOURCE_FILE)
    df = df.rename(columns={df.columns[0]: "row_idx"})
    row = df[df["Sector"] == "L_total"]
    if row.empty:
        raise KeyError(f"Row 'L_total' not found in {SOURCE_FILE.name}")
    year_cols = [c for c in df.columns if c.isdigit() and 1900 <= int(c) <= 2100]
    out = pd.DataFrame({
        "year":  [int(c) for c in year_cols],
        "value": [float(row.iloc[0][c]) for c in year_cols],
    })
    return out.sort_values("year").reset_index(drop=True)


def run():
    df = load()
    print(f"    [L01_{SERIES_ID}] book period: loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.0f}, last={df.iloc[-1]['value']:.0f}")
    ext = load_extension_raw()
    print(f"    [L01_{SERIES_ID}] extension raw: {len(ext)} rows; "
          f"period {ext['year'].min()}-{ext['year'].max()}; "
          f"1989_raw={float(ext.loc[ext['year']==1989, 'value'].iloc[0]):.0f}")
    return df


if __name__ == "__main__":
    run()

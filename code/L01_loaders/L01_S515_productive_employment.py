"""L01_S515 — Load Productive Employment (Lp), 1948-1961 (TableE3 narrow classification).

Source: Appendix E.3 (digitized as TableE3_LaborStatistics.csv), row
`Lp_total`. TableE3 is wide-by-year (years 1948-1961 are columns, sectors
are rows), so we transpose the row to a year-indexed series.

Note on classification: TableE3 uses the book's NARROW productive labor
classification (Lp/L ratio = 0.45 at 1948). This is different from the BROAD
classification in Table 5.7 (S511, Lp/L = 0.57). The book reports both;
they reflect different boundary choices for which sectors count as
productive. The DPR documents this distinction.

Status: book_period_partial_1948_1961.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES  # noqa: E402
from utils.io import read_book_table  # noqa: E402


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


def run():
    df = load()
    print(f"    [L01_{SERIES_ID}] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.0f}, last={df.iloc[-1]['value']:.0f}")
    return df


if __name__ == "__main__":
    run()

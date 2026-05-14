"""L01_S501 — Load Total Product (TP*) book-period series, 1948-1989.

Reads Appendix H.1 (digitized) and emits S501-A as an intermediate dataframe.
The extension component (S501-B) is the responsibility of a separate BEA loader
once API access is provisioned; see DPR for the splice contract.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import read_book_table
from utils.paths import BOOK_TABLES


SERIES_ID = "S501"
SUBSERIES = "S501-A"
SOURCE_FILE = BOOK_TABLES / "book_tableH1_1948_1989.csv"
SOURCE_COLUMN = "TP_star"


def load() -> pd.DataFrame:
    """Return a 2-column frame [year, value] for S501-A (book period TP*)."""
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source data missing: {SOURCE_FILE}")
    df = read_book_table(SOURCE_FILE)
    if SOURCE_COLUMN not in df.columns:
        raise KeyError(f"Column {SOURCE_COLUMN!r} not in {SOURCE_FILE.name}; got {list(df.columns)[:8]}")
    out = df[["year", SOURCE_COLUMN]].rename(columns={SOURCE_COLUMN: "value"}).copy()
    out["series_id"] = SUBSERIES
    out["units"] = "billions_usd"
    out = out[["series_id", "year", "value", "units"]].reset_index(drop=True)
    out["year"] = out["year"].astype(int)
    out["value"] = out["value"].astype(float)
    return out


def run() -> pd.DataFrame:
    df = load()
    print(f"    [L01_{SERIES_ID}] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.2f}, last={df.iloc[-1]['value']:.2f}")
    return df


if __name__ == "__main__":
    run()

"""L01_S501 — Load Total Product (TP*).

Two-part loader:
  - Book period (S501-A): book Table H.1 (TP_star column), 1948-1989, billions USD.
  - Extension period (S501-EXT raw): sum of BEA GDP-by-Industry gross-output
    for productive + trading top-level NAICS industries, 1997-2024, billions USD.
    Productive partition per Appendix C concordance (in EPR §5):
      11   Agriculture, forestry, fishing, hunting
      21   Mining
      22   Utilities
      23   Construction
      31G  Manufacturing (top-level rollup of 31ND + 33DG)
      42   Wholesale trade
      44RT Retail trade
      48TW Transportation and warehousing
    All eight are TOP-LEVEL aggregates in the BEA cache — summing them does
    not double-count with sub-industry codes (which appear separately in the
    same CSV).

The L01 returns BOTH series as a tuple. P02_S501 does the splice.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, ROOT  # noqa: E402
from utils.series import BookColumnLoader  # noqa: E402


# --- Book period loader (S501-A) ---

LOADER = BookColumnLoader(
    series_id    = "S501",
    subseries_id = "S501-A",
    source_file  = BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column = "TP_star",
    units        = "billions_usd",
)


# --- BEA extension loader (S501-EXT raw, pre-splice) ---

BEA_GO_CSV = ROOT / "data" / "raw" / "bea" / "gdp_by_industry_gross_output.csv"

PRODUCTIVE_TRADE_INDUSTRIES = [
    "11",     # Agriculture, forestry, fishing, hunting
    "21",     # Mining
    "22",     # Utilities
    "23",     # Construction
    "31G",    # Manufacturing (top-level rollup)
    "42",     # Wholesale trade
    "44RT",   # Retail trade
    "48TW",   # Transportation and warehousing
]


def load_bea_extension_raw() -> pd.DataFrame:
    """Load BEA GDP-by-Industry gross output, sum across productive+trade NAICS
    top-level industries, return DataFrame[year, value] (billions current USD)."""
    if not BEA_GO_CSV.exists():
        raise FileNotFoundError(f"BEA cache missing: {BEA_GO_CSV}")
    df = pd.read_csv(BEA_GO_CSV, dtype={"Industry": str})
    sel = df[df["Industry"].isin(PRODUCTIVE_TRADE_INDUSTRIES)].copy()
    if sel.empty:
        raise ValueError(
            f"No rows matched productive+trade industries {PRODUCTIVE_TRADE_INDUSTRIES} "
            f"in {BEA_GO_CSV.name}"
        )
    sel["Year"] = sel["Year"].astype(int)
    sel["DataValue"] = sel["DataValue"].astype(float)
    by_year = sel.groupby("Year", as_index=False)["DataValue"].sum()
    by_year = by_year.rename(columns={"Year": "year", "DataValue": "value"})
    by_year = by_year.sort_values("year").reset_index(drop=True)
    return by_year


def load() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return (book_df, bea_raw_df). Both have columns [series_id, year, value, units]
    for book_df; [year, value] for bea_raw_df. Splice/-EXT/-COMBINED is done in P02."""
    book = LOADER.load()
    bea_raw = load_bea_extension_raw()
    return book, bea_raw


def run():
    book, bea_raw = load()
    print(f"    [L01_S501] book {len(book)} rows, {book['year'].min()}-{book['year'].max()}; "
          f"book_first={book.iloc[0]['value']:.2f}, book_last={book.iloc[-1]['value']:.2f}")
    print(f"    [L01_S501] bea  {len(bea_raw)} rows, {bea_raw['year'].min()}-{bea_raw['year'].max()}; "
          f"bea_first(1997)={bea_raw.iloc[0]['value']:.2f}, bea_last={bea_raw.iloc[-1]['value']:.2f}")
    return book, bea_raw


if __name__ == "__main__":
    run()

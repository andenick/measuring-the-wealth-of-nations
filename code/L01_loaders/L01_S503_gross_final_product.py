"""L01_S503 — Load Gross Final Product (GFP = TP* - C*_m) book-period + BEA extension.

Two-part loader (mirrors S501/S502 pattern):
  - Book period (S503-A): Appendix H.1, column `GFP_star`. Published book series;
    also satisfies the identity GFP = TP* - C*_m which V03 checks. 1948-1989,
    billions current USD.
  - Extension period (S503-EXT raw): BEA Value Added (VA) for productive +
    trading top-level NAICS industries, 1997-2024. Productive partition uses
    the same 8 top-level NAICS aggregates as S501 EPR Appendix C concordance:
      11, 21, 22, 23, 31G, 42, 44RT, 48TW
    BEA VA = Gross Output - Intermediate Inputs is exactly the productive-sector
    value added of the book's GFP construct (GFP = TP* - M'_p = value added at
    factor cost by productive industries).

The L01 returns BOTH series as a tuple. P02_S503 does the splice.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, ROOT  # noqa: E402
from utils.series import BookColumnLoader  # noqa: E402


# --- Book period loader (S503-A) ---

LOADER = BookColumnLoader(
    series_id     = "S503",
    subseries_id  = "S503-A",
    source_file   = BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column = "GFP_star",
    units         = "billions_usd",
)


# --- BEA extension loader (S503-EXT raw, pre-splice) ---

BEA_VA_CSV = ROOT / "data" / "raw" / "bea" / "gdp_by_industry_value_added.csv"

PRODUCTIVE_TRADE_INDUSTRIES = [
    "11", "21", "22", "23", "31G", "42", "44RT", "48TW",
]


def load_bea_extension_raw() -> pd.DataFrame:
    """Load BEA GDP-by-Industry value added, sum across productive+trade NAICS
    top-level industries, return DataFrame[year, value] (billions current USD)."""
    if not BEA_VA_CSV.exists():
        raise FileNotFoundError(f"BEA cache missing: {BEA_VA_CSV}")
    df = pd.read_csv(BEA_VA_CSV, dtype={"Industry": str})
    sel = df[df["Industry"].isin(PRODUCTIVE_TRADE_INDUSTRIES)].copy()
    if sel.empty:
        raise ValueError(
            f"No rows matched productive+trade industries in {BEA_VA_CSV.name}"
        )
    sel["Year"] = sel["Year"].astype(int)
    sel["DataValue"] = sel["DataValue"].astype(float)
    by_year = sel.groupby("Year", as_index=False)["DataValue"].sum()
    by_year = by_year.rename(columns={"Year": "year", "DataValue": "value"})
    return by_year.sort_values("year").reset_index(drop=True)


def load() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return (book_df, bea_raw_df). Splice/-EXT/-COMBINED is done in P02."""
    book = LOADER.load()
    bea_raw = load_bea_extension_raw()
    return book, bea_raw


def run():
    book, bea_raw = load()
    print(f"    [L01_S503] book {len(book)} rows, {book['year'].min()}-{book['year'].max()}; "
          f"book_first={book.iloc[0]['value']:.2f}, book_last={book.iloc[-1]['value']:.2f}")
    print(f"    [L01_S503] bea  {len(bea_raw)} rows, {bea_raw['year'].min()}-{bea_raw['year'].max()}; "
          f"bea_first(1997)={bea_raw.iloc[0]['value']:.2f}, bea_last={bea_raw.iloc[-1]['value']:.2f}")
    return book, bea_raw


if __name__ == "__main__":
    run()

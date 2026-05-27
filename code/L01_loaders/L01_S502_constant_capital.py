"""L01_S502 — Load Constant Capital (C*_m = M'_p) book-period series + BEA extension.

Two-part loader (mirrors S501 pattern):
  - Book period (S502-A): Appendix H.1 (digitized), column `Mp` = constant capital
    consumed in production (= materials-only identity per p.95). 1948-1989,
    billions current USD.
  - Extension period (S502-EXT raw): BEA Intermediate Inputs (II) for productive +
    trading top-level NAICS industries, 1997-2024. Computed as II = Gross Output
    - Value Added, which is the BEA-published identity for industry accounts.
    Productive partition uses the same 8 top-level NAICS aggregates as S501 EPR
    Appendix C concordance:
      11   Agriculture, forestry, fishing, hunting
      21   Mining
      22   Utilities
      23   Construction
      31G  Manufacturing (top-level rollup of 31ND + 33DG)
      42   Wholesale trade
      44RT Retail trade
      48TW Transportation and warehousing

Marxian rationale: in the book's notation, C*_m = M'_p is the materials-only
component of productive-sector constant capital consumption. The BEA "Intermediate
Inputs" purchased by productive industries is the closest modern accounting
equivalent — it is the value of non-labor produced inputs consumed in production.
This excludes depreciation of fixed capital (which is handled separately by
S517 capital stock); the book's C*_m / M'_p notation is likewise the materials
flow, distinct from depreciation D_p.

The L01 returns BOTH series as a tuple. P02_S502 does the splice.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, ROOT  # noqa: E402
from utils.series import BookColumnLoader  # noqa: E402


# --- Book period loader (S502-A) ---

LOADER = BookColumnLoader(
    series_id     = "S502",
    subseries_id  = "S502-A",
    source_file   = BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column = "Mp",
    units         = "billions_usd",
)


# --- BEA extension loader (S502-EXT raw, pre-splice) ---

BEA_GO_CSV = ROOT / "data" / "raw" / "bea" / "gdp_by_industry_gross_output.csv"
BEA_VA_CSV = ROOT / "data" / "raw" / "bea" / "gdp_by_industry_value_added.csv"

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


def _sum_productive(csv_path: Path) -> pd.DataFrame:
    """Load BEA industry CSV, filter productive+trade industries, sum by year."""
    if not csv_path.exists():
        raise FileNotFoundError(f"BEA cache missing: {csv_path}")
    df = pd.read_csv(csv_path, dtype={"Industry": str})
    sel = df[df["Industry"].isin(PRODUCTIVE_TRADE_INDUSTRIES)].copy()
    if sel.empty:
        raise ValueError(
            f"No rows matched productive+trade industries in {csv_path.name}"
        )
    sel["Year"] = sel["Year"].astype(int)
    sel["DataValue"] = sel["DataValue"].astype(float)
    by_year = sel.groupby("Year", as_index=False)["DataValue"].sum()
    by_year = by_year.rename(columns={"Year": "year", "DataValue": "value"})
    return by_year.sort_values("year").reset_index(drop=True)


def load_bea_extension_raw() -> pd.DataFrame:
    """Return DataFrame[year, value] for BEA II = GO - VA, productive+trade NAICS,
    billions current USD."""
    go = _sum_productive(BEA_GO_CSV).rename(columns={"value": "go"})
    va = _sum_productive(BEA_VA_CSV).rename(columns={"value": "va"})
    merged = go.merge(va, on="year", how="inner")
    merged["value"] = merged["go"] - merged["va"]
    return merged[["year", "value"]].copy()


def load() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return (book_df, bea_raw_df). Splice/-EXT/-COMBINED is done in P02."""
    book = LOADER.load()
    bea_raw = load_bea_extension_raw()
    return book, bea_raw


def run():
    book, bea_raw = load()
    print(f"    [L01_S502] book {len(book)} rows, {book['year'].min()}-{book['year'].max()}; "
          f"book_first={book.iloc[0]['value']:.2f}, book_last={book.iloc[-1]['value']:.2f}")
    print(f"    [L01_S502] bea  {len(bea_raw)} rows, {bea_raw['year'].min()}-{bea_raw['year'].max()}; "
          f"bea_first(1997)={bea_raw.iloc[0]['value']:.2f}, bea_last={bea_raw.iloc[-1]['value']:.2f}")
    return book, bea_raw


if __name__ == "__main__":
    run()

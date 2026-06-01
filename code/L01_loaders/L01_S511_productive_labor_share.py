"""L01_S511 — Load Productive Labor Share (Lp/L) book-period series, 1948-1989.

Book-period source: Book Table 5.7 (digitized as Table5_7_KeyRatios.csv), column
`T511A` (book values, authoritative published Lp/L).

Extension source: BLS CES super-sector aggregation
(productive production workers ÷ total private all-employees).

The extension uses the 5-super-sector CES cache and aggregates the productive
goods-producing super-sectors. The book's Appendix C uses 85 SIC sectors;
this divergence is documented in S511_EPR.md and the registry's vintage_note.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES  # noqa: E402
from utils.series import BookColumnLoader  # noqa: E402
from utils.bls_cache import productive_employment_annual, total_employment_annual  # noqa: E402


LOADER = BookColumnLoader(
    series_id     = "S511",
    subseries_id  = "S511-A",
    source_file   = BOOK_TABLES / "Table5_7_KeyRatios.csv",
    source_column = "T511A",
    units         = "share",
)


def load_extension_raw() -> pd.DataFrame:
    """Load the raw (unspliced) BLS-derived Lp/L share, 1948-2024.

    Returns DataFrame [year, share] where share = productive production workers
    / total private all-employees. Both numerator and denominator come from the
    BLS CES super-sector cache.
    """
    lp = productive_employment_annual().rename(columns={"value": "Lp"})
    L  = total_employment_annual().rename(columns={"value": "L"})
    df = lp.merge(L, on="year", how="inner")
    df["share"] = df["Lp"] / df["L"]
    return df[["year", "share"]].reset_index(drop=True)


def run():
    df = LOADER.load()
    print(f"    [L01_{LOADER.series_id}] book period: loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    ext = load_extension_raw()
    print(f"    [L01_{LOADER.series_id}] extension raw: {len(ext)} rows; "
          f"period {ext['year'].min()}-{ext['year'].max()}; "
          f"1989_raw={float(ext.loc[ext['year']==1989, 'share'].iloc[0]):.4f}")
    return df


if __name__ == "__main__":
    run()

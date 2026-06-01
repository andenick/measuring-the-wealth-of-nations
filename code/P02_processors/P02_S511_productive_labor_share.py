"""P02_S511 — Process Productive Labor Share (Lp/L).

Stages:
  1. Load book series 1948-1989 (S511-A) from Table 5.7 column T511A.
  2. Load raw BLS-derived Lp/L share 1948-2024 (productive production workers
     ÷ total private all-employees, super-sector aggregation).
  3. Apply level splice at 1989: shift the raw extension so that
     extension(1989) == book(1989). Then take 1990-2024 as S511-EXT.
  4. S511-COMBINED = S511-A for 1948-1989 + S511-EXT for 1990-2024.
  5. Write all three subseries (long format) to data/final/S511.csv.

Caveat: BLS CES super-sector aggregation covers only the goods-producing
productive partition (mining/logging + construction + manufacturing). The
book's Appendix C uses 85 SIC sectors with additional productive services
and transportation/public utilities. Divergence documented in S511_EPR.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S511_productive_labor_share import LOADER, load_extension_raw  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID    = "S511"
SUB_A        = "S511-A"
SUB_EXT      = "S511-EXT"
SUB_COMBINED = "S511-COMBINED"
SPLICE_YEAR  = 1989
EXT_START    = 1990
EXT_END      = 2024


def _book_period_df() -> pd.DataFrame:
    df = LOADER.load()  # series_id=S511-A, year, value, units
    df["stage"]      = "book_period"
    df["provenance"] = "Table5_7_KeyRatios.csv:T511A"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def _ext_period_df(book_anchor: float) -> pd.DataFrame:
    """Build the spliced EXT subseries for EXT_START..EXT_END."""
    raw = load_extension_raw()  # year, share (raw BLS Lp/L)
    if SPLICE_YEAR not in raw["year"].values:
        raise ValueError(
            f"Cannot splice S511: BLS raw extension missing year {SPLICE_YEAR}"
        )
    raw_anchor = float(raw.loc[raw["year"] == SPLICE_YEAR, "share"].iloc[0])
    shift = book_anchor - raw_anchor  # level splice (additive)
    ext = raw[(raw["year"] >= EXT_START) & (raw["year"] <= EXT_END)].copy()
    ext["value"]      = ext["share"] + shift
    ext["series_id"]  = SUB_EXT
    ext["units"]      = "share"
    ext["stage"]      = "extension"
    ext["provenance"] = (
        f"BLS CES super-sector Lp/L (productive production workers / total private "
        f"all-employees), level-spliced at {SPLICE_YEAR} "
        f"(raw={raw_anchor:.4f} -> book={book_anchor:.4f}, shift={shift:+.4f}). "
        f"CAVEAT: super-sector aggregation; book uses 85 SIC sectors per Appendix C."
    )
    return ext[["series_id", "year", "value", "units", "stage", "provenance"]]


def _combined_df(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    book_part = book_df[book_df["year"] <= SPLICE_YEAR].copy()
    book_part["series_id"]  = SUB_COMBINED
    book_part["stage"]      = "combined_book"
    book_part["provenance"] = "S511-A (Table 5.7 T511A)"
    ext_part = ext_df.copy()
    ext_part["series_id"]   = SUB_COMBINED
    ext_part["stage"]       = "combined_extension"
    ext_part["provenance"]  = "S511-EXT (BLS CES super-sector, level-spliced at 1989)"
    out = pd.concat([book_part, ext_part], ignore_index=True)
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    book_df = _book_period_df()
    book_anchor = float(book_df.loc[book_df["year"] == SPLICE_YEAR, "value"].iloc[0])
    ext_df      = _ext_period_df(book_anchor)
    combined_df = _combined_df(book_df, ext_df)
    final = pd.concat([book_df, ext_df, combined_df], ignore_index=True)
    write_series_csv(final, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(final, SERIES_ID, stage="final")
    print(
        f"    [P02_{SERIES_ID}] wrote {final_path.name}: "
        f"A={len(book_df)} rows, EXT={len(ext_df)} rows, COMBINED={len(combined_df)} rows; "
        f"EXT[1995]={float(ext_df.loc[ext_df['year']==1995,'value'].iloc[0]):.4f}, "
        f"EXT[2010]={float(ext_df.loc[ext_df['year']==2010,'value'].iloc[0]):.4f}, "
        f"EXT[2024]={float(ext_df.loc[ext_df['year']==2024,'value'].iloc[0]):.4f}"
    )
    return final


if __name__ == "__main__":
    run()

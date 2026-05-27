"""P02_S515 — Process Productive Employment (Lp).

Stages:
  1. Load book series (S515-A) 1948-1961 from Appendix E.3 row `Lp_total`.
  2. Load raw BLS productive employment 1948-2024 (sum of goods-producing
     super-sector production workers, thousands).
  3. Apply level splice anchored at the LATEST AVAILABLE book endpoint.
     Book digitization currently covers 1948-1961, so the splice anchor is
     1961 (book_value=33615, extension begins at 1962). When the book-period
     KB digitization is extended to cover 1989, change SPLICE_YEAR to 1989.
  4. S515-EXT covers the post-anchor years through 2024.
  5. S515-COMBINED = S515-A for book years + S515-EXT for extension years.
  6. Write all three subseries (long format) to data/final/S515.csv.

Caveat: BLS CES super-sector aggregation covers only goods-producing
productive workers (mining/logging + construction + manufacturing). The
book's Appendix C uses 85 SIC sectors and also includes transportation/
public utilities and productive services. Levels here are therefore lower
than the book concept after the level splice corrects only the base. The
trajectory may also diverge from a 85-SIC reconstruction. Divergence is
documented in S515_EPR.md and the registry vintage_note.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S515_productive_employment import (  # noqa: E402
    load as load_S515,
    load_extension_raw,
)
from utils.io import write_series_csv  # noqa: E402


SERIES_ID    = "S515"
SUB_A        = "S515-A"
SUB_EXT      = "S515-EXT"
SUB_COMBINED = "S515-COMBINED"

# Book digitization covers 1948-1961 (NARROW classification, Appendix E.3).
# Splice at the latest available book endpoint.
SPLICE_YEAR  = 1961
EXT_START    = SPLICE_YEAR + 1  # 1962
EXT_END      = 2024


def _book_period_df() -> pd.DataFrame:
    df = load_S515()
    df["stage"]      = "book_period"
    df["provenance"] = "TableE3_LaborStatistics.csv:Lp_total"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def _ext_period_df(book_anchor: float) -> pd.DataFrame:
    raw = load_extension_raw()  # year, value (thousands)
    if SPLICE_YEAR not in raw["year"].values:
        raise ValueError(
            f"Cannot splice S515: BLS raw extension missing splice year {SPLICE_YEAR}"
        )
    raw_anchor = float(raw.loc[raw["year"] == SPLICE_YEAR, "value"].iloc[0])
    if raw_anchor <= 0:
        raise ValueError(f"BLS raw anchor at {SPLICE_YEAR} is non-positive: {raw_anchor}")
    # Level splice using a multiplicative scale: preserve growth trajectory of
    # raw BLS but rebase the level so extension(SPLICE_YEAR) == book(SPLICE_YEAR).
    # This is the canonical level-splice for a positive level series.
    scale = book_anchor / raw_anchor
    ext = raw[(raw["year"] >= EXT_START) & (raw["year"] <= EXT_END)].copy()
    ext["value"]      = ext["value"] * scale
    ext["series_id"]  = SUB_EXT
    ext["units"]      = "thousands"
    ext["stage"]      = "extension"
    ext["provenance"] = (
        f"BLS CES super-sector productive production workers "
        f"(mining/logging + construction + manufacturing), "
        f"level-spliced at {SPLICE_YEAR} via multiplicative scale "
        f"(raw={raw_anchor:.0f} -> book={book_anchor:.0f}, scale={scale:.4f}). "
        f"CAVEAT: super-sector aggregation; book uses 85 SIC sectors per Appendix C "
        f"(includes transportation/public utilities and productive services not "
        f"represented in the 5-super-sector cache)."
    )
    return ext[["series_id", "year", "value", "units", "stage", "provenance"]]


def _combined_df(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    book_part = book_df[book_df["year"] <= SPLICE_YEAR].copy()
    book_part["series_id"]  = SUB_COMBINED
    book_part["stage"]      = "combined_book"
    book_part["provenance"] = "S515-A (Appendix E.3 Lp_total)"
    ext_part = ext_df.copy()
    ext_part["series_id"]   = SUB_COMBINED
    ext_part["stage"]       = "combined_extension"
    ext_part["provenance"]  = f"S515-EXT (BLS CES super-sector, level-spliced at {SPLICE_YEAR})"
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
        f"EXT[1995]={float(ext_df.loc[ext_df['year']==1995,'value'].iloc[0]):.0f}, "
        f"EXT[2010]={float(ext_df.loc[ext_df['year']==2010,'value'].iloc[0]):.0f}, "
        f"EXT[2024]={float(ext_df.loc[ext_df['year']==2024,'value'].iloc[0]):.0f}"
    )
    return final


if __name__ == "__main__":
    run()

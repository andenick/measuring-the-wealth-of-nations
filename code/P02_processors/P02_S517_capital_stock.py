"""P02_S517 — Process K* (Productive Capital Stock) book + extension.

Three subseries emitted:
  S517-A        : Book period 1948-1989. Per the iteration 8 sourcing decision,
                  the book's Appendix H/K K* values are not extracted in the
                  current KB build (Appendix H is text-only per RMWND CLAUDE.md);
                  the BEA Fixed Assets Table 4.1 Line 1 (Private nonresidential,
                  Current-Cost Net Stock) series is therefore used as the
                  operational book reference, restricted to 1948-1989. This is
                  consistent with the reference_values populated by the Stage 3
                  v2 patch (1925, 1948, 1958, 1967, 1980, 1989 endpoints).

  S517-EXT      : Extension period 1990-2024 from the same BEA Fixed Assets
                  Table 4.1 Line 1 series. Splice at 1989 with method=level
                  and rescale factor = 1.0 (no transformation): book and
                  extension share the same underlying BEA series, so the
                  level-splice is trivially exact at the seam (1989 -> 1990
                  growth is BEA's own).

  S517-COMBINED : Concatenation of S517-A (1948-1989) and S517-EXT (1990-2024)
                  into a single continuous 1948-2024 panel. Pre-1948 BEA values
                  (1925-1947) are available in the raw cache but are not
                  included in -A or -COMBINED to keep alignment with the book's
                  1948-1989 reporting window.

Caveats (carried over from S517_research.json known_issues, the iteration 8
sourcing patch, and S517_DPR):
  1) BEA Fixed Assets Table 4.1 is the AGGREGATE current-cost net stock of
     private nonresidential fixed assets. It is NOT yet filtered through the
     85-IO productive-sector concordance (agriculture, mining, construction,
     manufacturing, transportation, communications, utilities, trade). A
     concordance-based refinement would subtract the financial-sector
     component (~5-10%) and re-aggregate productive industries; that is a
     future Stage 5 refinement (see IMPLEMENTATION_PLAN.md Phase 2.A).
  2) Book Table 5.8 specifies K* = GROSS stock; this implementation uses NET
     stock per Table 4.1 (current-cost). For strict gross-stock replication
     BEA Table 4.2 would be the alternative source (not yet cached).
  3) Pre-1948 values (1925-1947) are emitted only in intermediate output for
     completeness; the canonical S517-A subseries is the 1948-1989 window.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S517_capital_stock import load as load_S517  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S517"
BOOK_FIRST_YEAR = 1948
BOOK_LAST_YEAR = 1989
EXT_FIRST_YEAR = 1990
EXT_LAST_YEAR = 2024


def run():
    raw = load_S517()  # series_id=S517-A, 1925-2024 from BEA Fixed Assets 4.1 Line 1

    # ---- S517-A : book pass-through, 1948-1989 ----
    book = raw[(raw["year"] >= BOOK_FIRST_YEAR) & (raw["year"] <= BOOK_LAST_YEAR)].copy()
    book["series_id"]  = "S517-A"
    book["units"]      = "billions_usd"
    book["stage"]      = "book_period"
    book["provenance"] = (
        "BEA Fixed Assets Table 4.1 Line 1 (Private nonresidential fixed assets), "
        "Current-Cost Net Stock; operational book reference for K* in lieu of "
        "Appendix H extraction (Appendix H is text-only)"
    )
    book_out = book[["series_id", "year", "value", "units", "stage", "provenance"]]

    # ---- S517-EXT : extension 1990-2024, level splice at 1989 (factor=1.0) ----
    book_1989 = float(raw.loc[raw["year"] == BOOK_LAST_YEAR, "value"].iloc[0])
    bea_1990 = float(raw.loc[raw["year"] == EXT_FIRST_YEAR, "value"].iloc[0])
    rescale_factor = 1.0  # same underlying BEA series -> trivial level splice

    ext = raw[(raw["year"] >= EXT_FIRST_YEAR) & (raw["year"] <= EXT_LAST_YEAR)].copy()
    ext["value"]      = ext["value"] * rescale_factor
    ext["series_id"]  = "S517-EXT"
    ext["units"]      = "billions_usd"
    ext["stage"]      = "extension"
    ext["provenance"] = (
        "BEA Fixed Assets Table 4.1 Line 1 (Private nonresidential fixed assets), "
        "Current-Cost Net Stock; level splice at 1989 with rescale_factor=1.0 "
        "(book and extension share the same underlying BEA series)"
    )
    ext_out = ext[["series_id", "year", "value", "units", "stage", "provenance"]]

    # ---- S517-COMBINED : book (1948-1989) + extension (1990-2024) ----
    combined_book = book.copy()
    combined_book["series_id"]  = "S517-COMBINED"
    combined_book["stage"]      = "book_period"
    combined_book["provenance"] = (
        "BEA Fixed Assets 4.1 Line 1 (book arm of combined series)"
    )

    combined_ext = ext.copy()
    combined_ext["series_id"]  = "S517-COMBINED"
    combined_ext["stage"]      = "extension"
    combined_ext["provenance"] = (
        "BEA Fixed Assets 4.1 Line 1 (extension arm of combined series, level splice)"
    )

    combined_out = pd.concat([
        combined_book[["series_id", "year", "value", "units", "stage", "provenance"]],
        combined_ext[["series_id", "year", "value", "units", "stage", "provenance"]],
    ], ignore_index=True).sort_values("year").reset_index(drop=True)

    # ---- Stack and write ----
    out = pd.concat([book_out, ext_out, combined_out], ignore_index=True)
    write_series_csv(out, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(out, SERIES_ID, stage="final")

    print(f"    [P02_S517] wrote {final_path.name}  ({len(out)} rows: "
          f"{(out['series_id']=='S517-A').sum()} A, "
          f"{(out['series_id']=='S517-EXT').sum()} EXT, "
          f"{(out['series_id']=='S517-COMBINED').sum()} COMBINED)")
    print(f"    [P02_S517] book_endpoint(1989)={book_1989:.2f}; "
          f"ext_start(1990)={bea_1990:.2f}; "
          f"rescale_factor={rescale_factor:.4f}; "
          f"EXT_2024={float(ext_out.loc[ext_out['year']==EXT_LAST_YEAR, 'value'].iloc[0]):.2f}")
    return out


if __name__ == "__main__":
    run()

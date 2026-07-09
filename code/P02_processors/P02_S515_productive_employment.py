"""P02_S515 — Process Productive Employment (Lp), share-primitive rebuild.

REVIEW_2026-07 item D2 (candidate (d) of internal-review-notes_2026-07/
S515_S516_SEAM_REDESIGN.md, user-ratified). This replaces the pre-review
direct super-sector level-splice (anchored, incorrectly, at 1961) with the
book's OWN construction (FULL_TEXT.md L449, verbatim):

    Lj = PEP = FEE + SEP;  L = ΣLj;  (Lp/L)j;  (Lp)j = (Lp/L)j·(Lj);
    Lp = Σ(Lp)j;  and  Lu = L − Lp.

i.e. the productive SHARE Lp/L is the estimated primitive; Lp = share × total L;
Lu (S516) is the residual L − Lp. The clean S511 series already provides that
share (workpackage A-certified, real BLS CES, additive level-splice @1989, continuous
seam). The total L is a book-anchored total-employment series incl. government
(CES0000000001), re-anchored to the book L at 1989.

Two published arms (both anchored at 1989):
  * S515-A            — book Lp (TableE3 `Lp_total`), 1948-1989 (unchanged).
  * S515-EXT          — Lp = S511_share × L_reanchored, 1990-2024.
  * S515-COMBINED     — S515-A (≤1989) spliced to S515-EXT (≥1990).

Honest constructible / transparency arms (distinct measures, break-flagged):
  * S515-EXT-CONSTRUCTIBLE   — raw 3-super-sector production-worker count
        (mining/logging + construction + manufacturing), unspliced. This is the
        honest BLS-native measure (Lp/L ≈ 0.195 @1989, ~half the book's 0.363
        productive perimeter). It is NOT the published Lp — retained per the
        S506/S512 two-arm pattern so the constructible measure is visible
        alongside the reconstructed one.
  * S515-EXT-OLD-DEPRECATED  — the frozen pre-review arm (raw super-sector count
        level-spliced @1961), retained for transparency only. DEPRECATED.

The old splice discarded 28 years of genuine book data (1962-1989); the new
build keeps every book year in S515-A/COMBINED and continues from a matched
level at the true 1989 overlap. Residual concept gaps (L universe;
productive-perimeter narrowing on the share) are registered as DIVs.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S515_productive_employment import (  # noqa: E402
    load as load_S515,
    load_extension_raw,
    load_book_L_total,
)
from utils.bls_cache import reanchored_total_employment  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID        = "S515"
SUB_A            = "S515-A"
SUB_EXT          = "S515-EXT"
SUB_COMBINED     = "S515-COMBINED"
SUB_CONSTRUCT    = "S515-EXT-CONSTRUCTIBLE"
SUB_OLD          = "S515-EXT-OLD-DEPRECATED"

# Single anchor year for the whole S515/S516 boundary (matches registry
# declaration splice_year=1989 and S511/S516). TableE3 covers 1948-1989.
SPLICE_YEAR = 1989
EXT_START   = SPLICE_YEAR + 1   # 1990
EXT_END     = 2024

# Frozen pre-review arm used 1961 as its anchor.
OLD_SPLICE_YEAR = 1961


def _book_period_df() -> pd.DataFrame:
    df = load_S515()  # S515-A, book Lp_total, 1948-1989
    df["stage"]      = "book_period"
    df["provenance"] = "TableE3_LaborStatistics.csv:Lp_total (book Lp, Table 5.5 / Appendix F)"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def _load_s511_share() -> pd.Series:
    """Return the clean continuous Lp/L share (S511) indexed by year.

    S511-COMBINED = S511-A (book Table 5.7 T511A, ≤1989) + S511-EXT (BLS CES
    super-sector Lp/L, additively level-spliced @1989, ≥1990). This is the
    workpackage A-certified CLEAN share the book method multiplies by total L.
    """
    s511_path = DATA_FINAL / "S511.csv"
    if not s511_path.exists():
        raise FileNotFoundError(
            f"S511 not built: {s511_path} missing. Run P02_S511 before P02_S515."
        )
    df = pd.read_csv(s511_path)
    comb = df[df["series_id"] == "S511-COMBINED"]
    if comb.empty:
        raise ValueError("S511-COMBINED subseries absent from data/final/S511.csv")
    return comb.set_index("year")["value"].astype(float)


def _reanchored_L() -> pd.Series:
    """Book-anchored total-employment L (incl. govt), indexed by year."""
    book_L = load_book_L_total().set_index("year")["value"]
    if SPLICE_YEAR not in book_L.index:
        raise ValueError(f"Book L_total missing anchor year {SPLICE_YEAR}")
    anchor_value = float(book_L.loc[SPLICE_YEAR])   # 113511 @1989
    Lre = reanchored_total_employment(SPLICE_YEAR, anchor_value)
    return Lre.set_index("year")["value"].astype(float)


def _ext_period_df() -> pd.DataFrame:
    """S515-EXT = S511_share × L_reanchored, EXT_START..EXT_END (book method)."""
    share = _load_s511_share()
    Lre = _reanchored_L()
    years = [y for y in range(EXT_START, EXT_END + 1) if y in share.index and y in Lre.index]
    Lp = pd.Series({y: float(share.loc[y]) * float(Lre.loc[y]) for y in years})
    ext = pd.DataFrame({"year": list(Lp.index), "value": list(Lp.values)})
    ext["series_id"]  = SUB_EXT
    ext["units"]      = "thousands"
    ext["stage"]      = "extension"
    anchor_L = float(Lre.loc[SPLICE_YEAR])
    ext["provenance"] = (
        f"Lp = (Lp/L)·L per book method (FULL_TEXT L449): S511 productive share × "
        f"book-anchored total employment L. Share = S511-COMBINED (BLS CES super-sector "
        f"Lp/L, additive level-splice @1989). L = CES0000000001 (total nonfarm incl. govt) "
        f"multiplicatively re-anchored to book L @{SPLICE_YEAR} (={anchor_L:.0f}). "
        f"Residual L concept gap (self-employed/agriculture; productive-perimeter narrowing "
        f"on the share) registered as DIVs."
    )
    return ext[["series_id", "year", "value", "units", "stage", "provenance"]]


def _combined_df(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    book_part = book_df[book_df["year"] <= SPLICE_YEAR].copy()
    book_part["series_id"]  = SUB_COMBINED
    book_part["stage"]      = "combined_book"
    book_part["provenance"] = "S515-A (TableE3 Lp_total, 1948-1989 book values retained)"
    ext_part = ext_df.copy()
    ext_part["series_id"]   = SUB_COMBINED
    ext_part["stage"]       = "combined_extension"
    ext_part["provenance"]  = f"S515-EXT (S511 share × book-anchored L, @{SPLICE_YEAR})"
    out = pd.concat([book_part, ext_part], ignore_index=True)
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def _constructible_df() -> pd.DataFrame:
    """S515-EXT-CONSTRUCTIBLE — raw 3-super-sector production-worker count.

    Honest BLS-native distinct measure (NOT the published Lp), unspliced,
    break-flagged. Full available span 1948-2024.
    """
    raw = load_extension_raw().copy()   # year, value (thousands)
    raw = raw.dropna(subset=["value"])
    raw["series_id"]  = SUB_CONSTRUCT
    raw["units"]      = "thousands"
    raw["stage"]      = "constructible_distinct_measure"
    raw["provenance"] = (
        "DISTINCT MEASURE (break-flagged): raw sum of BLS CES production workers over the "
        "3 goods-producing super-sectors (mining/logging CES1000000006 + construction "
        "CES2000000006 + manufacturing CES3000000006), UNSPLICED. Captures ~half the book's "
        "productive perimeter (super-sector Lp/L ≈ 0.195 vs book 0.363); it is the honest "
        "constructible count, NOT the published Lp. Retained per the S506/S512 two-arm pattern."
    )
    return raw[["series_id", "year", "value", "units", "stage", "provenance"]]


def _old_deprecated_df() -> pd.DataFrame:
    """S515-EXT-OLD-DEPRECATED — frozen pre-review arm (raw super-sector count
    level-spliced @1961). Retained for transparency only. DEPRECATED."""
    raw = load_extension_raw().copy()
    raw = raw.dropna(subset=["value"])
    anchor = raw.loc[raw["year"] == OLD_SPLICE_YEAR, "value"]
    if anchor.empty:
        raise ValueError(f"OLD arm: raw missing {OLD_SPLICE_YEAR}")
    # Book Lp @1961 = 29363 (TableE3).
    book_lp = load_S515().set_index("year")["value"]
    scale = float(book_lp.loc[OLD_SPLICE_YEAR]) / float(anchor.iloc[0])
    old = raw[(raw["year"] > OLD_SPLICE_YEAR) & (raw["year"] <= EXT_END)].copy()
    old["value"]      = old["value"] * scale
    old["series_id"]  = SUB_OLD
    old["units"]      = "thousands"
    old["stage"]      = "frozen_deprecated"
    old["provenance"] = (
        f"FROZEN / DEPRECATED (pre-review): raw super-sector production-worker count "
        f"level-spliced @{OLD_SPLICE_YEAR} (scale={scale:.4f}). Retained for transparency; "
        f"superseded by the share×L rebuild. Discarded book data 1962-1989 — do not consume."
    )
    return old[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    book_df    = _book_period_df()
    ext_df     = _ext_period_df()
    combined_df = _combined_df(book_df, ext_df)
    construct_df = _constructible_df()
    old_df       = _old_deprecated_df()
    final = pd.concat(
        [book_df, ext_df, combined_df, construct_df, old_df], ignore_index=True
    )
    write_series_csv(final, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(final, SERIES_ID, stage="final")

    def _v(df, sub_or_year, year=None):
        if year is None:
            year = sub_or_year
            d = ext_df
        else:
            d = df
        r = d.loc[d["year"] == year, "value"]
        return float(r.iloc[0]) if len(r) else float("nan")

    book_1989 = float(book_df.loc[book_df["year"] == 1989, "value"].iloc[0])
    ext_1990  = float(ext_df.loc[ext_df["year"] == 1990, "value"].iloc[0])
    print(
        f"    [P02_{SERIES_ID}] wrote {final_path.name}: A={len(book_df)} EXT={len(ext_df)} "
        f"COMBINED={len(combined_df)} CONSTRUCTIBLE={len(construct_df)} OLD-DEP={len(old_df)} rows; "
        f"book Lp[1989]={book_1989:.1f} -> EXT[1990]={ext_1990:.1f} "
        f"(seam break {100*(ext_1990-book_1989)/book_1989:+.1f}%); "
        f"EXT[2024]={float(ext_df.loc[ext_df['year']==2024,'value'].iloc[0]):.1f}"
    )
    return final


if __name__ == "__main__":
    run()

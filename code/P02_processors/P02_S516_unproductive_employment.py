"""P02_S516 — Unproductive Employment (Lu = L − Lp), single-L rebuild.

REVIEW_2026-07 item D2 (candidate (d), user-ratified). The book's method
(FULL_TEXT.md L449): Lu = L − Lp, where L is TOTAL labor over all sectors incl.
government and Lp = (Lp/L)·L. This processor uses the SAME single, book-anchored
total-employment L as P02_S515 and subtracts the published S515 Lp, so the
identity L = Lp + Lu holds at EVERY year including the 1989/1990 seam with one
consistent basis and anchor year.

Book period (1948-1989): S516-A = L_total − Lp_total from Appendix E.3
(TableE3_LaborStatistics.csv). Unchanged.

Extension (1990-2024): S516-EXT = L_reanchored − S515-EXT
  * L_reanchored = CES0000000001 (total nonfarm incl. govt), multiplicatively
    re-anchored to the book L @1989 (= the same L basis P02_S515 uses).
  * S515-EXT     = the published productive employment Lp (share × L).
This retires the pre-review bug where S516-EXT used total PRIVATE employment
(CES0500000001), which dropped government and drove the −22% Lu seam break.

COMBINED (1948-2024): S516-A authoritative through 1989, S516-EXT from 1990.
Both arms now share one L basis and one anchor year (1989), so there is no
seam discontinuity and no 1962-1989 gap.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, DATA_FINAL  # noqa: E402
from utils.io import read_book_table, write_series_csv  # noqa: E402
from utils.bls_cache import reanchored_total_employment  # noqa: E402


SERIES_ID = "S516"
SUBSERIES_A = "S516-A"
SUBSERIES_EXT = "S516-EXT"
SUBSERIES_COMBINED = "S516-COMBINED"
SOURCE_FILE = BOOK_TABLES / "TableE3_LaborStatistics.csv"
SPLICE_YEAR = 1989
EXT_START = SPLICE_YEAR + 1  # 1990
EXT_END = 2024


def compute_book_period() -> pd.DataFrame:
    """Lu = L − Lp from TableE3, 1948-1989 (S516-A)."""
    df = read_book_table(SOURCE_FILE)
    df = df.rename(columns={df.columns[0]: "row_idx"})
    L_total = df[df["Sector"] == "L_total"]
    Lp_total = df[df["Sector"] == "Lp_total"]
    if L_total.empty or Lp_total.empty:
        raise KeyError(f"L_total or Lp_total not found in {SOURCE_FILE.name}")

    year_cols = [c for c in df.columns if c.isdigit() and 1900 <= int(c) <= 2100]
    out = pd.DataFrame({
        "year":  [int(c) for c in year_cols],
        "L":     [float(L_total.iloc[0][c]) for c in year_cols],
        "Lp":    [float(Lp_total.iloc[0][c]) for c in year_cols],
    })
    out["value"]      = out["L"] - out["Lp"]
    out["series_id"]  = SUBSERIES_A
    out["units"]      = "thousands"
    out["stage"]      = "book_period"
    out["provenance"] = "TableE3_LaborStatistics.csv: L_total − Lp_total (book Lu, Table 5.5)"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def _book_L_anchor() -> float:
    """Book L_total at the splice year (113511 @1989)."""
    df = read_book_table(SOURCE_FILE)
    df = df.rename(columns={df.columns[0]: "row_idx"})
    L_total = df[df["Sector"] == "L_total"]
    if L_total.empty or str(SPLICE_YEAR) not in df.columns:
        raise KeyError(f"L_total / column {SPLICE_YEAR} not found in {SOURCE_FILE.name}")
    return float(L_total.iloc[0][str(SPLICE_YEAR)])


def load_s515_ext() -> pd.DataFrame:
    """Return [year, Lp] for the published S515-EXT (productive Lp), or raise."""
    s515_path = DATA_FINAL / "S515.csv"
    if not s515_path.exists():
        raise FileNotFoundError(
            f"S515 not built: {s515_path} missing. Run P02_S515 before P02_S516."
        )
    df = pd.read_csv(s515_path)
    ext = df[df["series_id"] == "S515-EXT"].copy()
    if ext.empty:
        raise ValueError("S515-EXT absent from data/final/S515.csv — run P02_S515 first.")
    return ext[["year", "value"]].rename(columns={"value": "Lp"}).reset_index(drop=True)


def compute_extension(s515_ext: pd.DataFrame) -> pd.DataFrame:
    """S516-EXT = L_reanchored − S515-EXT, 1990-2024 (book Lu = L − Lp)."""
    anchor_value = _book_L_anchor()   # 113511 @1989
    Lre = reanchored_total_employment(SPLICE_YEAR, anchor_value).rename(columns={"value": "L"})
    df = Lre.merge(s515_ext, on="year", how="inner")
    df = df[(df["year"] >= EXT_START) & (df["year"] <= EXT_END)].copy()
    df["value"]      = df["L"] - df["Lp"]
    df["series_id"]  = SUBSERIES_EXT
    df["units"]      = "thousands"
    df["stage"]      = "extension"
    df["provenance"] = (
        f"Lu = L − Lp (book method, FULL_TEXT L449): L = CES0000000001 (total nonfarm incl. "
        f"govt) re-anchored to book L @{SPLICE_YEAR} (={anchor_value:.0f}) − published S515-EXT "
        f"(productive Lp). Single consistent L basis shared with S515; identity holds at seam."
    )
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def splice_combined(df_a: pd.DataFrame, df_ext: pd.DataFrame) -> pd.DataFrame:
    """S516-COMBINED: A authoritative through SPLICE_YEAR, EXT from SPLICE_YEAR+1."""
    a_part = df_a[df_a["year"] <= SPLICE_YEAR].copy()
    ext_part = df_ext[df_ext["year"] > SPLICE_YEAR].copy()
    combined = pd.concat([a_part, ext_part], ignore_index=True).sort_values("year").reset_index(drop=True)
    combined["series_id"]  = SUBSERIES_COMBINED
    combined["provenance"] = (
        f"splice(S516-A book Lu through {SPLICE_YEAR}, S516-EXT = L − Lp from {EXT_START}); "
        f"single book-anchored L basis — continuous at the seam (no 1962-1989 gap)."
    )
    combined["stage"] = combined.apply(
        lambda r: "book_period" if r["year"] <= SPLICE_YEAR else "extension", axis=1
    )
    return combined[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df_a = compute_book_period()
    s515_ext = load_s515_ext()
    df_ext = compute_extension(s515_ext)
    df_combined = splice_combined(df_a, df_ext)
    final = pd.concat([df_a, df_ext, df_combined], ignore_index=True)
    write_series_csv(final, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(final, SERIES_ID, stage="final")

    book_1989 = float(df_a.loc[df_a["year"] == 1989, "value"].iloc[0])
    ext_1990  = float(df_ext.loc[df_ext["year"] == 1990, "value"].iloc[0])
    print(
        f"    [P02_{SERIES_ID}] {len(final)} rows "
        f"({len(df_a)} A + {len(df_ext)} EXT + {len(df_combined)} COMBINED); "
        f"book Lu[1989]={book_1989:.1f} -> EXT[1990]={ext_1990:.1f} "
        f"(seam break {100*(ext_1990-book_1989)/book_1989:+.1f}%); "
        f"EXT[2024]={float(df_ext.loc[df_ext['year']==2024,'value'].iloc[0]):.1f}; "
        f"wrote {final_path.name}"
    )
    return final


if __name__ == "__main__":
    run()

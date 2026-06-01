"""P02_S516 — Compute Unproductive Employment (Lu = L_total - Lp_total).

Book period (1948-1961): Appendix E.3 (TableE3_LaborStatistics.csv), rows
`L_total` and `Lp_total`. Computed as the residual.

Extension (1990-2024): derived identity Lu = L - Lp, where
  - L  = total private all-employees from BLS CES (`total_employment_annual`)
  - Lp = S515-EXT from `data/final/S515.csv` (parallel agent output)
If S515-EXT is not yet present in data/final/S515.csv, the EXT subseries is
skipped (logged as TODO) and only the book-period S516-A is written. This
processor should be re-run after S515-EXT becomes available.

COMBINED (1948-2024 when EXT available; else 1948-1961): direct splice with
S516-A authoritative through 1989, then S516-EXT from 1990 onward. There is
no overlap region to verify because S516-A ends 1961 and S516-EXT starts 1990
— the 1962-1989 gap is a documented coverage gap inherited from S515.

Status: book_period_partial_1948_1961 (book), extension dependent on S515.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES, DATA_FINAL  # noqa: E402
from utils.io import read_book_table, write_series_csv  # noqa: E402
from utils.bls_cache import total_employment_annual  # noqa: E402


SERIES_ID = "S516"
SUBSERIES_A = "S516-A"
SUBSERIES_EXT = "S516-EXT"
SUBSERIES_COMBINED = "S516-COMBINED"
SOURCE_FILE = BOOK_TABLES / "TableE3_LaborStatistics.csv"
SPLICE_YEAR = 1989


def compute_book_period() -> pd.DataFrame:
    """Lu = L - Lp from TableE3, 1948-1961 (S516-A)."""
    df = read_book_table(SOURCE_FILE)
    df = df.rename(columns={df.columns[0]: "row_idx"})
    L_total = df[df["Sector"] == "L_total"]
    Lp_total = df[df["Sector"] == "Lp_total"]
    if L_total.empty or Lp_total.empty:
        raise KeyError(f"L_total or Lp_total not found in {SOURCE_FILE.name}")

    year_cols = [c for c in df.columns if c.isdigit() and 1900 <= int(c) <= 2100]
    out = pd.DataFrame({
        "year":  [int(c) for c in year_cols],
        "L":     [float(L_total.iloc[0][c])  for c in year_cols],
        "Lp":    [float(Lp_total.iloc[0][c]) for c in year_cols],
    })
    out["value"]      = out["L"] - out["Lp"]
    out["series_id"]  = SUBSERIES_A
    out["units"]      = "thousands"
    out["stage"]      = "book_period"
    out["provenance"] = "TableE3_LaborStatistics.csv:L_total - Lp_total"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def load_s515_ext() -> pd.DataFrame | None:
    """Return DataFrame [year, value] for S515-EXT if present in data/final/S515.csv.

    Returns None if S515-EXT rows are absent — extension cannot be computed yet.
    """
    s515_path = DATA_FINAL / "S515.csv"
    if not s515_path.exists():
        return None
    df = pd.read_csv(s515_path)
    ext = df[df["series_id"] == "S515-EXT"].copy()
    if ext.empty:
        return None
    return ext[["year", "value"]].rename(columns={"value": "Lp"}).reset_index(drop=True)


def compute_extension(s515_ext: pd.DataFrame) -> pd.DataFrame:
    """Lu = L - Lp using BLS CES total employment and S515-EXT, 1990-2024 (S516-EXT)."""
    L = total_employment_annual().rename(columns={"value": "L"})
    df = L.merge(s515_ext, on="year", how="inner")
    df = df[df["year"] >= 1990].copy()
    df["value"]      = df["L"] - df["Lp"]
    df["series_id"]  = SUBSERIES_EXT
    df["units"]      = "thousands"
    df["stage"]      = "extension"
    df["provenance"] = (
        "BLS CES total_private_all_employees (CES0500000001) - S515-EXT "
        "[derived Lu = L - Lp]"
    )
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def splice_combined(df_a: pd.DataFrame, df_ext: pd.DataFrame) -> pd.DataFrame:
    """Build S516-COMBINED: A authoritative through SPLICE_YEAR, EXT from SPLICE_YEAR+1."""
    a_part = df_a[df_a["year"] <= SPLICE_YEAR].copy()
    ext_part = df_ext[df_ext["year"] > SPLICE_YEAR].copy()
    combined = pd.concat([a_part, ext_part], ignore_index=True).sort_values("year").reset_index(drop=True)
    combined["series_id"]  = SUBSERIES_COMBINED
    combined["provenance"] = (
        "splice(S516-A through 1989, S516-EXT from 1990) — gap 1962-1989 inherited from S515"
    )
    combined["stage"] = combined.apply(
        lambda r: "book_period" if r["year"] <= SPLICE_YEAR else "extension", axis=1
    )
    return combined[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df_a = compute_book_period()
    s515_ext = load_s515_ext()

    if s515_ext is None:
        # Extension not yet possible — emit only A. Re-run after S515-EXT lands.
        final = df_a
        write_series_csv(final, SERIES_ID, stage="intermediate")
        final_path = write_series_csv(final, SERIES_ID, stage="final")
        print(
            f"    [P02_{SERIES_ID}] book period only ({len(df_a)} rows); "
            f"first={df_a.iloc[0]['value']:.0f}; "
            f"S515-EXT not yet in data/final/S515.csv — TODO: re-run after S515 extension. "
            f"wrote {final_path.name}"
        )
        return final

    df_ext = compute_extension(s515_ext)
    df_combined = splice_combined(df_a, df_ext)
    final = pd.concat([df_a, df_ext, df_combined], ignore_index=True)
    write_series_csv(final, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(final, SERIES_ID, stage="final")
    print(
        f"    [P02_{SERIES_ID}] {len(final)} rows "
        f"({len(df_a)} A + {len(df_ext)} EXT + {len(df_combined)} COMBINED); "
        f"A first={df_a.iloc[0]['value']:.0f}; "
        f"EXT span {int(df_ext['year'].min())}-{int(df_ext['year'].max())}; "
        f"EXT last={df_ext.iloc[-1]['value']:.0f}; "
        f"wrote {final_path.name}"
    )
    return final


if __name__ == "__main__":
    run()

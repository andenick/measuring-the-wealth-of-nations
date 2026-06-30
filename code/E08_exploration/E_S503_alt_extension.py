"""E_S503_alt_extension — Explore alternative NAICS partitions for S503 GFP extension.

Problem
-------
The S503 (Gross Final Product, GFP = TP* - C*_m) extension currently uses a
narrow productive+trade NAICS partition:
    A = [11, 21, 22, 23, 31G, 42, 44RT, 48TW]
This yields a 1997 BEA endpoint of ~3462 Bn vs the book 1989 endpoint of ~4364 Bn,
a downward 26% discontinuity at the SIC->NAICS junction. The narrow partition
may understate value added because some borderline-productive activities
(information, professional services, real-estate-leasing-of-productive-assets)
are excluded.

This exploration tests broader partitions:
    B = A + [51 Information, 54 Professional/Scientific/Technical]
    C = A + [51, 54, 53 Real Estate / Rental / Leasing]
and reports the level discontinuity vs the book 1989 endpoint for each.

Inputs
------
- BEA GDP-by-Industry Value Added cache:
    data/raw/bea/gdp_by_industry_value_added.csv
- Book Table H.1 (column GFP_star):
    Technical/data/source/book_tables/book_tableH1_1948_1989.csv

Outputs
-------
- Technical/data/scratch/S503_alt_extension.csv (1948..2024 wide)
- Console comparison table

Notes
-----
This is a pure exploration script. It does NOT touch series_registry.json,
PIPELINE_STATE, LEDGER, MANIFEST, or SUBSERIES_PLAN. Results are evidence
for VPR_S503_alt_extension.md.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# --- Paths (absolute, project-anchored) ------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]  # .../RMWND
TECH_ROOT = PROJECT_ROOT / "Technical"

BEA_VA_CSV = (
    PROJECT_ROOT / "data" / "raw" / "bea"
    / "gdp_by_industry_value_added.csv"
)
BOOK_H1_CSV = TECH_ROOT / "data" / "source" / "book_tables" / "book_tableH1_1948_1989.csv"
SCRATCH_CSV = TECH_ROOT / "data" / "scratch" / "S503_alt_extension.csv"

# --- Partitions ------------------------------------------------------------

PARTITION_A = ["11", "21", "22", "23", "31G", "42", "44RT", "48TW"]
PARTITION_B = PARTITION_A + ["51", "54"]
PARTITION_C = PARTITION_B + ["53"]

BOOK_LAST_YEAR = 1989
EXT_FIRST_YEAR = 1997
EXT_LAST_YEAR = 2024


def load_bea_va_sum(industries: list[str]) -> pd.DataFrame:
    """Load BEA GDP-by-Industry value added, sum across the given NAICS top-level
    industries, return DataFrame[year, value] (billions current USD)."""
    if not BEA_VA_CSV.exists():
        raise FileNotFoundError(f"BEA cache missing: {BEA_VA_CSV}")
    df = pd.read_csv(BEA_VA_CSV, dtype={"Industry": str})
    sel = df[df["Industry"].isin(industries)].copy()
    if sel.empty:
        raise ValueError(f"No rows matched industries {industries}")
    sel["Year"] = sel["Year"].astype(int)
    sel["DataValue"] = sel["DataValue"].astype(float)
    # Annual rows only (Frequency == 'A')
    if "Frequency" in sel.columns:
        sel = sel[sel["Frequency"] == "A"]
    by_year = sel.groupby("Year", as_index=False)["DataValue"].sum()
    by_year = by_year.rename(columns={"Year": "year", "DataValue": "value"})
    return by_year.sort_values("year").reset_index(drop=True)


def load_book_gfp() -> pd.DataFrame:
    """Load book Table H.1 GFP_star, 1948-1989."""
    if not BOOK_H1_CSV.exists():
        raise FileNotFoundError(f"Book H.1 missing: {BOOK_H1_CSV}")
    df = pd.read_csv(BOOK_H1_CSV, comment="#")
    return df[["year", "GFP_star"]].rename(columns={"GFP_star": "value"}).copy()


def log_linear_bridge(book_endpoint: float, ext_endpoint: float,
                      y0: int, y1: int) -> pd.DataFrame:
    """Log-linear interpolation rows for the open interval (y0, y1)."""
    n = y1 - y0
    log0, log1 = np.log(book_endpoint), np.log(ext_endpoint)
    rows = [
        {"year": y0 + k, "value": float(np.exp(log0 + (k / n) * (log1 - log0)))}
        for k in range(1, n)
    ]
    return pd.DataFrame(rows)


def build_combined(book_df: pd.DataFrame, ext_df: pd.DataFrame) -> pd.DataFrame:
    """Build the full 1948..EXT_LAST_YEAR combined series with log-linear bridge."""
    book_1989 = float(book_df.loc[book_df["year"] == BOOK_LAST_YEAR, "value"].iloc[0])
    ext_1997 = float(ext_df.loc[ext_df["year"] == EXT_FIRST_YEAR, "value"].iloc[0])
    bridge = log_linear_bridge(book_1989, ext_1997, BOOK_LAST_YEAR, EXT_FIRST_YEAR)

    parts = [
        book_df[["year", "value"]],
        bridge,
        ext_df[(ext_df["year"] >= EXT_FIRST_YEAR) & (ext_df["year"] <= EXT_LAST_YEAR)][["year", "value"]],
    ]
    return pd.concat(parts, ignore_index=True).sort_values("year").reset_index(drop=True)


def main() -> None:
    book = load_book_gfp()
    book_1989 = float(book.loc[book["year"] == BOOK_LAST_YEAR, "value"].iloc[0])

    ext_a = load_bea_va_sum(PARTITION_A)
    ext_b = load_bea_va_sum(PARTITION_B)
    ext_c = load_bea_va_sum(PARTITION_C)

    # 1997 endpoints
    end_a = float(ext_a.loc[ext_a["year"] == EXT_FIRST_YEAR, "value"].iloc[0])
    end_b = float(ext_b.loc[ext_b["year"] == EXT_FIRST_YEAR, "value"].iloc[0])
    end_c = float(ext_c.loc[ext_c["year"] == EXT_FIRST_YEAR, "value"].iloc[0])

    # Discontinuities (BEA 1997 vs Book 1989)
    disc_a = (end_a - book_1989) / book_1989 * 100.0
    disc_b = (end_b - book_1989) / book_1989 * 100.0
    disc_c = (end_c - book_1989) / book_1989 * 100.0

    # Build combined series for the scratch CSV
    comb_a = build_combined(book, ext_a).rename(columns={"value": "variant_A"})
    comb_b = build_combined(book, ext_b).rename(columns={"value": "variant_B"})
    comb_c = build_combined(book, ext_c).rename(columns={"value": "variant_C"})

    merged = comb_a.merge(comb_b, on="year", how="outer").merge(comb_c, on="year", how="outer")
    merged = merged.sort_values("year").reset_index(drop=True)

    SCRATCH_CSV.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(SCRATCH_CSV, index=False)

    # Console report
    print("=" * 72)
    print("S503 GFP Alternative Extension — Variant Comparison")
    print("=" * 72)
    print(f"Book endpoint (1989, GFP_star)         : {book_1989:>10.2f} Bn USD")
    print()
    print(f"{'Variant':<10} {'Partition':<42} {'BEA 1997':>10} {'Disc.':>9}")
    print("-" * 72)
    print(f"{'A':<10} {'[11,21,22,23,31G,42,44RT,48TW]':<42} {end_a:>10.2f} {disc_a:>+8.1f}%")
    print(f"{'B':<10} {'A + [51,54]':<42} {end_b:>10.2f} {disc_b:>+8.1f}%")
    print(f"{'C':<10} {'A + [51,54,53]':<42} {end_c:>10.2f} {disc_c:>+8.1f}%")
    print()
    print(f"Wrote {SCRATCH_CSV}")
    print(f"Rows: {len(merged)}  (years {int(merged['year'].min())}..{int(merged['year'].max())})")


if __name__ == "__main__":
    main()

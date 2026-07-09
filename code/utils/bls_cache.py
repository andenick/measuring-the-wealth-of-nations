"""Read BLS CES cached CSV responses.

The BLS CES cache lives at:
  data/raw/Inputs/API_Data/BLS/bls_ces_production_workers.csv

Format: wide-by-series with first column `year`, then one column per BLS CES
series ID. Each cell is `production workers (thousands)` or `all employees
(thousands)` depending on the series.

Coverage notes (from the cache as of 2026-02-24):
  - CES0500000001 (total private all employees):       1948-2024
  - CES0500000006 (total private production workers):  1964-2024 (NA before)
  - CES0600000001 (goods-producing all employees):     1948-2024
  - CES0600000006 (goods-producing production workers):1948-2024
  - CES1000000006 (mining/logging production):         1948-2024
  - CES2000000006 (construction production):           1948-2024
  - CES3000000006 (manufacturing production):          1948-2024
  - CES1000000001/2000000001/3000000001 (all employees): 1948-2024

For Shaikh-Tonak's productive employment Lp, the productive super-sectors
covered in this 5-super-sector cache are the goods-producing sectors
(mining/logging + construction + manufacturing). The book's full Appendix C
concordance covers 85 SIC sectors and additionally includes transportation
& public utilities and productive services — that finer partition is NOT
in this cache. This divergence is documented in the EPR.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .paths import ROOT


BLS_CES_CACHE = ROOT.parent / "Inputs" / "predecessor-build" / "Inputs" / "API_Data" / "BLS" / "bls_ces_production_workers.csv"

# Total nonfarm ALL EMPLOYEES incl. government (CES0000000001), fetched by
# code/L00_setup/L00_bls_fetch_total_nonfarm.py for the REVIEW_2026-07 D2
# S515/S516 seam redesign. This is the total-employment universe of the book's
# L (Table 5.5 / Appendix F, all sectors incl. government — FULL_TEXT.md L449).
BLS_TOTAL_NONFARM_CACHE = (
    ROOT.parent / "Inputs" / "predecessor-build" / "Inputs" / "API_Data" / "BLS"
    / "bls_ces_total_nonfarm_all_employees.csv"
)


def load_bls_ces() -> pd.DataFrame:
    """Load the cached BLS CES production-workers wide table.

    Returns DataFrame with `year` and one column per CES series ID, values
    in thousands. NaN where the series is not published for that year.
    """
    if not BLS_CES_CACHE.exists():
        raise FileNotFoundError(f"BLS CES cache missing: {BLS_CES_CACHE}")
    df = pd.read_csv(BLS_CES_CACHE)
    df["year"] = df["year"].astype(int)
    return df


# ---- Productive aggregates ----

# Goods-producing production workers = mining/logging + construction + manufacturing.
# This is the productive-sector partition available in the 5-super-sector cache.
# (Identical to CES0600000006 within rounding; we sum the components for transparency.)
PRODUCTIVE_PROD_WORKER_SERIES = [
    "CES1000000006",   # mining/logging production workers
    "CES2000000006",   # construction production workers
    "CES3000000006",   # manufacturing production workers
]

# All-employee total for the denominator L.
TOTAL_PRIVATE_ALL_EMPLOYEES = "CES0500000001"


def productive_employment_annual() -> pd.DataFrame:
    """Sum productive-sector production workers by year (thousands).

    Returns DataFrame [year, value] over 1948-2024. `value` is the sum of
    production workers across the 3 goods-producing super-sectors
    (mining/logging + construction + manufacturing) that compose the
    "productive" partition in the 5-super-sector BLS CES cache.

    CAVEAT: This is a super-sector aggregation. The book's Appendix C uses
    85 SIC sectors and additionally includes transportation/public utilities
    and productive services. See S511/S515 EPRs for the documented divergence.
    """
    df = load_bls_ces()
    cols = ["year"] + PRODUCTIVE_PROD_WORKER_SERIES
    sub = df[cols].dropna(subset=PRODUCTIVE_PROD_WORKER_SERIES, how="all")
    sub = sub.copy()
    sub["value"] = sub[PRODUCTIVE_PROD_WORKER_SERIES].sum(axis=1, skipna=False)
    return sub[["year", "value"]].sort_values("year").reset_index(drop=True)


def total_employment_annual() -> pd.DataFrame:
    """Total private all-employees (thousands) by year, 1948-2024.

    Used as the denominator L for the productive labor share Lp/L (S511 share).

    NOTE: this is the PRIVATE universe (CES0500000001). For the S515/S516 seam
    redesign (REVIEW_2026-07 D2) the total-employment L must include government;
    use ``total_nonfarm_all_employees_annual`` / ``reanchored_total_employment``
    instead for that book-faithful total.
    """
    df = load_bls_ces()
    out = df[["year", TOTAL_PRIVATE_ALL_EMPLOYEES]].rename(
        columns={TOTAL_PRIVATE_ALL_EMPLOYEES: "value"}
    )
    return out.sort_values("year").reset_index(drop=True)


# All-employee total for the book-faithful L (incl. government).
TOTAL_NONFARM_ALL_EMPLOYEES = "CES0000000001"


def total_nonfarm_all_employees_annual() -> pd.DataFrame:
    """BLS CES total nonfarm all-employees incl. government (thousands), 1948-2024.

    Series CES0000000001, fetched by L00_bls_fetch_total_nonfarm.py. This is the
    establishment-side total-employment universe closest to the book's L (total
    labor over all sectors incl. government, Table 5.5 / Appendix F). It excludes
    self-employed and agriculture; that residual concept gap is corrected at the
    1989 anchor by ``reanchored_total_employment`` and registered as a DIV.

    Returns DataFrame [year, value] in thousands (NaN-years dropped).
    """
    if not BLS_TOTAL_NONFARM_CACHE.exists():
        raise FileNotFoundError(
            f"Total-nonfarm cache missing: {BLS_TOTAL_NONFARM_CACHE}. "
            f"Run code/L00_setup/L00_bls_fetch_total_nonfarm.py first."
        )
    df = pd.read_csv(BLS_TOTAL_NONFARM_CACHE)
    df["year"] = df["year"].astype(int)
    df = df.dropna(subset=["value"]).copy()
    df["value"] = df["value"].astype(float)
    return df[["year", "value"]].sort_values("year").reset_index(drop=True)


def reanchored_total_employment(anchor_year: int, anchor_value: float) -> pd.DataFrame:
    """Book-anchored total-employment L: multiplicative level-splice of total
    nonfarm (incl. govt) so that L(anchor_year) == anchor_value (the book L).

        L_reanchored[y] = anchor_value * CES0000000001[y] / CES0000000001[anchor_year]

    This is the book's own L universe (total labor incl. government) rebased to
    the book level at the overlap year, exactly analogous to the S511/S512
    level-splices at 1989. Both P02_S515 (Lp = share * L) and P02_S516
    (Lu = L - Lp) consume THIS single L so the identity L = Lp + Lu holds with a
    single consistent basis and anchor year.

    Returns DataFrame [year, value] in thousands.
    """
    tnf = total_nonfarm_all_employees_annual().set_index("year")["value"]
    if anchor_year not in tnf.index:
        raise ValueError(f"anchor_year {anchor_year} missing from total-nonfarm cache")
    scale = anchor_value / float(tnf.loc[anchor_year])
    out = (tnf * scale).reset_index()
    out.columns = ["year", "value"]
    return out.sort_values("year").reset_index(drop=True)

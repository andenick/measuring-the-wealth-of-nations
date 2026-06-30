"""Read BLS CES cached CSV responses.

The BLS CES cache lives at:
  data/raw/bls/bls_ces_production_workers.csv

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


BLS_CES_CACHE = ROOT / "data" / "raw" / "bls" / "bls_ces_production_workers.csv"


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

    Used as the denominator L for the productive labor share Lp/L.
    """
    df = load_bls_ces()
    out = df[["year", TOTAL_PRIVATE_ALL_EMPLOYEES]].rename(
        columns={TOTAL_PRIVATE_ALL_EMPLOYEES: "value"}
    )
    return out.sort_values("year").reset_index(drop=True)

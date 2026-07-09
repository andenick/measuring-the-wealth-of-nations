"""L01 helper for S514 — load capacity utilization u.

Two sources (D1 decision, 2026-07-02):
  * load_book_u()  — the book's OWN utilization series (Shaikh 1992a) from
    Table 5.8, a FRACTION (0-1), 1948-1989. Used for the book-period arm
    S514-A so the divide operation r*'=r*/u reproduces the book's r*' row.
  * load_tcu()     — FRED Total Capacity Utilization (TCU), a PERCENT (0-100),
    1967-present. Used (as TCU/100) for the extension arm S514-EXT, where the
    book's Shaikh-1992 series is unavailable.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import ROOT  # noqa: E402

TCU_CSV = ROOT / "data" / "raw" / "fred" / "fred_tcu_capacity_utilization.csv"
BOOK_U_CSV = ROOT / "data" / "source" / "book_tables" / "Table5_8_u_capacity_utilization.csv"


def load_tcu() -> pd.DataFrame:
    df = pd.read_csv(TCU_CSV)
    return df[["year", "value"]].rename(columns={"value": "TCU"})


def load_book_u() -> pd.DataFrame:
    """Book Shaikh-1992a capacity utilization u (fraction 0-1), 1948-1989.

    Source: MWoN Table 5.8 row 'u' (KB v2 _combined/5.8.csv). u=1 is
    normal/full capacity; values >1 (1966=1.01) denote above-normal use.
    """
    df = pd.read_csv(BOOK_U_CSV, comment="#")
    return df[["year", "u"]].copy()


if __name__ == "__main__":
    tcu = load_tcu()
    u = load_book_u()
    print(f"    [L01_S514] TCU loaded: {len(tcu)} rows, {tcu['year'].min()}-{tcu['year'].max()}")
    print(f"    [L01_S514] book u loaded: {len(u)} rows, {u['year'].min()}-{u['year'].max()}, "
          f"range {u['u'].min():.2f}-{u['u'].max():.2f}")

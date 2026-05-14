"""P02_S516 — Compute Unproductive Employment (Lu = L_total - Lp_total), 1948-1961.

Source: Appendix E.3 (TableE3_LaborStatistics.csv), rows `L_total` and
`Lp_total`. Computed as the residual. No separate L01 — both rows are loaded
inline from the source. Status: book_period_partial_1948_1961.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES  # noqa: E402
from utils.io import read_book_table, write_series_csv  # noqa: E402


SERIES_ID = "S516"
SUBSERIES = "S516-A"
SOURCE_FILE = BOOK_TABLES / "TableE3_LaborStatistics.csv"


def compute() -> pd.DataFrame:
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
    out["series_id"]  = SUBSERIES
    out["units"]      = "thousands"
    out["stage"]      = "book_period"
    out["provenance"] = "TableE3_LaborStatistics.csv:L_total - Lp_total"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.0f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

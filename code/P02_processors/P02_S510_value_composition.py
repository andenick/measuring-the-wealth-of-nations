"""P02_S510 — Compute Value Composition of Capital (K/V*) = S517 / S504.

The flow-based composition uses the book's Mp (constant capital flow, S502).
The stock-based composition uses K* (capital stock, S517). Book reports both;
S510 in the registry is the STOCK ratio (matches book's Table 5.10 column).

DERIVED — no L01 loader.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S510"
SUBSERIES = "S510-A"


def compute() -> pd.DataFrame:
    s517 = pd.read_csv(DATA_FINAL / "S517.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s517 = s517[s517["series_id"] == "S517-A"][["year", "value"]].rename(columns={"value": "K_star"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    merged = s517.merge(s504, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["K_star"] / merged["V_star"]
    merged["series_id"]  = SUBSERIES
    merged["units"]      = "ratio"
    merged["stage"]      = "book_period_derived"
    merged["provenance"] = "S517 / S504"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S510] {len(df)} rows; first={df.iloc[0]['value']:.2f}, last={df.iloc[-1]['value']:.2f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

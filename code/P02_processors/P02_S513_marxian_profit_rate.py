"""P02_S513 — Compute Marxian Profit Rate r* = S* / (K* + V*).

The book's central rate of profit, using:
- S* = surplus value (S505)
- K* = productive constant capital STOCK (S517) — note: stock not flow
- V* = variable capital (S504)

Book finding 1948-1989: r* declines roughly 0.42 → 0.36 secularly, with
recovery 1980s.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S513"
SUBSERIES = "S513-A"


def compute() -> pd.DataFrame:
    s505 = pd.read_csv(DATA_FINAL / "S505.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s517 = pd.read_csv(DATA_FINAL / "S517.csv")
    s505 = s505[s505["series_id"] == "S505-A"][["year", "value"]].rename(columns={"value": "S_star"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    s517 = s517[s517["series_id"] == "S517-A"][["year", "value"]].rename(columns={"value": "K_star"})
    merged = s505.merge(s504, on="year").merge(s517, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["S_star"] / (merged["K_star"] + merged["V_star"])
    merged["series_id"]  = SUBSERIES
    merged["units"]      = "rate"
    merged["stage"]      = "book_period_derived"
    merged["provenance"] = "S505 / (S517 + S504)"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S513] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

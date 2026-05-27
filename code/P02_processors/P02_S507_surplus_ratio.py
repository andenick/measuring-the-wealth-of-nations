"""P02_S507 — Compute Surplus Ratio (S*/(S*+V*)) from S505 and S504.

This is a derived series — no direct column in Appendix H.1. The formula
S* / (S* + V*) is equivalent to S* / VA* (since VA* = V* + S*) but we compute
from S* and V* because both are first-class series in the project (validated
against the book) and the ratio composition is more transparent.

Since the construction is purely a per-year ratio of two already-built series,
there is no separate L01 loader — P02 reads the final/S504.csv and final/S505.csv
directly. The Anu Framework permits this when the upstream series already
exist in canonical form.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S507"
SUBSERIES = "S507-A"


def compute() -> pd.DataFrame:
    s505 = pd.read_csv(DATA_FINAL / "S505.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s505 = s505[s505["series_id"] == "S505-A"][["year", "value"]].rename(columns={"value": "S_star"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    merged = s505.merge(s504, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["S_star"] / (merged["S_star"] + merged["V_star"])
    merged["series_id"]  = SUBSERIES
    merged["units"]      = "ratio"
    merged["stage"]      = "book_period"
    merged["provenance"] = "S505/(S505+S504)"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

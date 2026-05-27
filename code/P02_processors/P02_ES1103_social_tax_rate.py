"""P02_ES1103 — Social Tax Rate (S&T 1987) (derived ratio).

Computed as S604 / S617.

Uses Ch6 NSW component series (S604/S605/S606) and S617 (Employee Compensation
from H.1). This is the Shaikh & Tonak (1987) framework — what fraction of
total compensation flows back to workers via the state in each direction.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv
from utils.paths import DATA_FINAL

SERIES_ID = "ES1103"
SUBSERIES = "ES1103-A"

def _load(sid: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_FINAL / f"{sid}.csv")
    return df[df["series_id"] == f"{sid}-A"][["year", "value"]].rename(columns={"value": sid})

def compute() -> pd.DataFrame:
    S604 = _load('S604')
    S617 = _load('S617')
    merged = S604.merge(S617, on='year').sort_values('year').reset_index(drop=True)
    merged["value"] = merged['S604'] / merged['S617']
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "analytical_derivation"
    merged["provenance"] = "S604 / S617"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]

def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_ES1103] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df

if __name__ == "__main__":
    run()

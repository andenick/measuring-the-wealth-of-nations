"""P02_S608 — Compute NSW/V* ratio from S607 (NSW) and S504 (Variable Capital).

A derived ratio. No L01 loader: reads final/S607.csv and final/S504.csv
directly. The ratio sign indicates whether workers receive net transfers
from the state (positive) or subsidize it (negative).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S608"
SUBSERIES = "S608-A"


def compute() -> pd.DataFrame:
    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s607 = s607[s607["series_id"] == "S607-A"][["year", "value"]].rename(columns={"value": "NSW"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    merged = s607.merge(s504, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["NSW"] / merged["V_star"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "book_period"
    merged["provenance"] = "S607 / S504"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

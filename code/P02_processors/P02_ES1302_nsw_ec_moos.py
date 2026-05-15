"""P02_ES1302 — Moos NSW / compensation (Moos's own compensation column)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_moos_2017 import load_moos  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "ES1302"
SUBSERIES = "ES1302-A"


def compute() -> pd.DataFrame:
    moos = load_moos()
    df = moos[["year", "nsw1", "compensation"]].copy()
    df["value"] = df["nsw1"] / df["compensation"]
    df["series_id"] = SUBSERIES
    df["units"] = "share"
    df["stage"] = "derived"
    df["provenance"] = "Moos nsw1 / Moos compensation"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_ES1302] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

"""L01 helper for S514 — load FRED TCU from cache."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import ROOT  # noqa: E402

TCU_CSV = ROOT / "data" / "raw" / "fred" / "fred_tcu_capacity_utilization.csv"


def load_tcu() -> pd.DataFrame:
    df = pd.read_csv(TCU_CSV)
    return df[["year", "value"]].rename(columns={"value": "TCU"})


if __name__ == "__main__":
    df = load_tcu()
    print(f"    [L01_S514] TCU loaded: {len(df)} rows, {df['year'].min()}-{df['year'].max()}")

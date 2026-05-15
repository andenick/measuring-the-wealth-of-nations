"""P02_S514 — Capacity-adjusted Marxian profit rate: r*_adj = r* × TCU/100.

TCU = Federal Reserve total capacity utilization (FRED series TCU).
Available 1967-2024; for 1948-1966 (no TCU data), emit NaN per the
no-synthetic-data rule.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S514_capacity_adj_profit_rate_tcu import load_tcu  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S514"
SUBSERIES = "S514-A"


def compute() -> pd.DataFrame:
    s513 = pd.read_csv(DATA_FINAL / "S513.csv")
    s513 = s513[s513["series_id"] == "S513-A"][["year", "value"]].rename(columns={"value": "r_star"})
    tcu = load_tcu()
    merged = s513.merge(tcu, on="year", how="left").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["r_star"] * (merged["TCU"] / 100)
    merged["series_id"]  = SUBSERIES
    merged["units"]      = "rate"
    merged["stage"]      = "book_period_derived"
    merged["provenance"] = "S513 × (TCU/100); TCU NaN pre-1967"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    n_valid = df["value"].notna().sum()
    print(f"    [P02_S514] {len(df)} rows ({n_valid} with TCU, {len(df) - n_valid} NaN pre-1967); wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

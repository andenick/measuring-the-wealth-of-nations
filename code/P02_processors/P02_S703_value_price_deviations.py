"""P02_S703 — Value-Price Deviations: percent deviation of S702 prices from S701 values.

Book Chapter 7 finding: deviations are small (2-15%) — labor value is a
good first approximation to price. Computed as: (S702 - S701) / S701 × 100.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S703"
SUBSERIES = "S703-A"


def compute() -> pd.DataFrame:
    s701 = pd.read_csv(DATA_FINAL / "S701.csv")
    s701 = s701[s701["series_id"] == "S701-A"][["year", "value"]].rename(columns={"value": "lambda"})
    s702 = pd.read_csv(DATA_FINAL / "S702.csv")
    s702 = s702[s702["series_id"] == "S702-A"][["year", "value"]].rename(columns={"value": "p"})
    merged = s701.merge(s702, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = (merged["p"] - merged["lambda"]) / merged["lambda"] * 100
    merged["series_id"] = SUBSERIES
    merged["units"] = "percent"
    merged["stage"] = "benchmark_only_derived"
    merged["provenance"] = "(S702 - S701) / S701 × 100"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S703] {len(df)} rows; range=[{df['value'].min():.2f}%, {df['value'].max():.2f}%]; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

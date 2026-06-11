"""P02_S801 — Cross-study comparison (Ch8): ST vs Mohun.

Merges S506 (ST exploitation rate), S511 (ST productive labor share),
XS1401 (Mohun exploitation rate), XS1402 (Mohun productive labor share)
into one wide table for side-by-side comparison.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S801"
SUBSERIES = "S801-A"


def _load(sid: str, col_name: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_FINAL / f"{sid}.csv")
    return df[df["series_id"] == f"{sid}-A"][["year", "value"]].rename(columns={"value": col_name})


def compute() -> pd.DataFrame:
    s506 = _load("S506", "ST_e")
    s511 = _load("S511", "ST_LpL")
    es1401 = _load("XS1401", "Mohun_e")
    es1402 = _load("XS1402", "Mohun_LpL")

    merged = s506.merge(s511, on="year").merge(es1401, on="year").merge(es1402, on="year")
    merged = merged.sort_values("year").reset_index(drop=True)
    merged["e_diff"] = merged["ST_e"] - merged["Mohun_e"]
    merged["LpL_diff"] = merged["ST_LpL"] - merged["Mohun_LpL"]
    merged["value"] = merged["ST_e"]  # canonical column = ST_e for series ID
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "cross_study"
    merged["provenance"] = "merge(S506, S511, XS1401, XS1402)"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S801] {len(df)} comparison years 1948-1989; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

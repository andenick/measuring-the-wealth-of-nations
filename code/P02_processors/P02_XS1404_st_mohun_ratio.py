"""P02_XS1404 — Compute ST/Mohun Exploitation Rate Ratio.

XS1404 = S506 (book e) / XS1401 (Mohun e). A cross-classification sensitivity
metric: how much does the productive/unproductive boundary choice affect the
headline exploitation finding?
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS1404"
SUBSERIES = "XS1404-A"


def compute() -> pd.DataFrame:
    s506    = pd.read_csv(DATA_FINAL / "S506.csv")
    es1401  = pd.read_csv(DATA_FINAL / "XS1401.csv")
    s506    = s506[s506["series_id"] == "S506-A"][["year","value"]].rename(columns={"value":"e_ST"})
    es1401  = es1401[es1401["series_id"] == "XS1401-A"][["year","value"]].rename(columns={"value":"e_Mohun"})
    merged  = s506.merge(es1401, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["e_ST"] / merged["e_Mohun"]
    merged["series_id"]  = SUBSERIES
    merged["units"]      = "ratio"
    merged["stage"]      = "cross_validation"
    merged["provenance"] = "S506 / XS1401"
    return merged[["series_id","year","value","units","stage","provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

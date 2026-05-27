"""P02_ES1301 — Moos 2017 NSW/GDP (extended via post-1989 NIPA reconstruction).

Moos applies the ST methodology through 2012 using post-1989 NIPA data with
a slightly different unproductive-sector boundary. nsw1 = his preferred
measure (matches ST's narrow productive partition).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.shared_moos_2017_loader import load_moos  # noqa: E402
from utils.bea_cache import load_bea_line  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "ES1301"
SUBSERIES = "ES1301-A"


def compute() -> pd.DataFrame:
    moos = load_moos()
    gdp = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 1)
    gdp["value"] = gdp["value"] / 1000.0
    gdp = gdp.rename(columns={"value": "GDP"})

    merged = moos[["year", "nsw1"]].merge(gdp, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["nsw1"] / merged["GDP"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "derived"
    merged["provenance"] = "Moos nsw1 / NIPA 1.7.5 GDP"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_ES1301] {len(df)} rows {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

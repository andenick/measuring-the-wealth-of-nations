"""P02_ES1201 — NSW / GDP (ST 2002) using S607 + cached NIPA 1.7.5 GDP.

The Shaikh & Tonak 2002 paper revisits NSW through the Clinton era,
normalizing by GDP. Our overlap with their period (1952-1997): full.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.bea_cache import load_bea_line  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "ES1201"
SUBSERIES = "ES1201-A"


def compute() -> pd.DataFrame:
    gdp = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 1)
    gdp["value"] = gdp["value"] / 1000.0  # millions -> billions
    gdp = gdp.rename(columns={"value": "GDP"})

    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s607 = s607[s607["series_id"] == "S607-COMBINED"][["year", "value"]].rename(columns={"value": "NSW"})

    merged = s607.merge(gdp, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["NSW"] / merged["GDP"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "derived"
    merged["provenance"] = "S607-COMBINED / NIPA 1.7.5 GDP"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    v_1952 = float(df[df["year"] == 1952]["value"].iloc[0]) if (df["year"] == 1952).any() else None
    v_1997 = float(df[df["year"] == 1997]["value"].iloc[0]) if (df["year"] == 1997).any() else None
    v_2024 = float(df[df["year"] == 2024]["value"].iloc[0]) if (df["year"] == 2024).any() else None
    print(f"    [P02_ES1201] {len(df)} rows; NSW/GDP: 1952={v_1952:.4f}, 1997={v_1997:.4f}, 2024={v_2024:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

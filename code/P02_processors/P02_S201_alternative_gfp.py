"""P02_S201 — Compute Marxian-vs-orthodox aggregate comparison.

Per book Chapter 2: GFP* (Marxian, S503) differs from orthodox GDP because
it excludes non-productive transfer activities (finance, trade margins,
government services) from gross final product. The S201 series exposes the
key ratios:

  GFP_GDP_ratio = S503 / GDP
  FP_NDP_ratio  = (S503 - CFC_productive) / NDP

We approximate CFC_productive as total CFC × (S503/GDP), preserving the
share-proportional assumption stated in book Ch 2.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S201_alternative_gfp import load_nipa_aggregates  # noqa: E402
from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S201"
SUBSERIES = "S201-A"


def compute() -> pd.DataFrame:
    nipa = load_nipa_aggregates()
    s503 = pd.read_csv(DATA_FINAL / "S503.csv")
    s503 = s503[s503["series_id"] == "S503-A"][["year", "value"]].rename(columns={"value": "GFP_star"})
    merged = nipa.merge(s503, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["GFP_GDP_ratio"] = merged["GFP_star"] / merged["GDP"]
    merged["FP_star"] = merged["GFP_star"] - merged["CFC"] * (merged["GFP_star"] / merged["GDP"])
    merged["FP_NDP_ratio"] = merged["FP_star"] / merged["NDP"]
    merged["value"] = merged["GFP_GDP_ratio"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "book_period_derived"
    merged["provenance"] = "S503 / NIPA 1.7.5 GDP"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S201] {len(df)} rows; "
          f"GFP/GDP: 1948={df[df['year']==1948]['value'].iloc[0]:.3f}, "
          f"1989={df[df['year']==1989]['value'].iloc[0]:.3f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

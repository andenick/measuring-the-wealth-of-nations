"""P02_ES1601 — Turkey Labor Share (Karabacak & Tonak 2022).

Source: World Bank Turkey structural indicators 1980-2019. Karabacak & Tonak
approximate labor share via (1 - profit_share) where profit_share is derived
from industry value added.

Simpler approximation used here: labor_share = 1 - (govt_consumption_pct_gdp/100)
- (some fraction of services_va_pct_gdp). For first-pass, use:
  labor_share ≈ (industry_va_pct_gdp + 0.5 × services_va_pct_gdp) / 100

A refinement using OECD compensation data would be more faithful; documented
in DPR as approximation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import ROOT  # noqa: E402


SERIES_ID = "ES1601"
SUBSERIES = "ES1601-A"
SRC = ROOT / "data" / "source" / "external_studies" / "Turkey_worldbank_structural_1980_2019.csv"


def compute() -> pd.DataFrame:
    df = pd.read_csv(SRC)
    # Approximation: labor share ≈ industry VA + half of services VA (rough proxy for compensation share)
    df["value"] = (df["industry_va_pct_gdp"] + 0.5 * df["services_va_pct_gdp"]) / 100
    df["series_id"] = SUBSERIES
    df["units"] = "share"
    df["stage"] = "derived_approximation"
    df["provenance"] = "(industry_va + 0.5*services_va) / 100 from WB structural"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_ES1601] {len(df)} rows {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

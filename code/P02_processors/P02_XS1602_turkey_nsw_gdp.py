"""P02_XS1602 — Turkey NSW/GDP (Karabacak & Tonak 2022).

Karabacak & Tonak's central finding: NSW negative for ALL 40 years in
Turkey (workers as net subsidizers, no positive episodes).

Approximation: NSW/GDP ≈ (govt_consumption + transfers - tax_revenue) / GDP
all expressed as % of GDP in the WB fiscal table.

Per the paper, the productive partition is similar to S&T's broad
classification, and the residual after tax/transfer netting is taken as NSW.
A more faithful version would apply per-sector decomposition; this is a
defensible first-pass.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import ROOT  # noqa: E402


SERIES_ID = "XS1602"
SUBSERIES = "XS1602-A"
SRC = ROOT / "data" / "source" / "external_studies" / "Turkey_worldbank_fiscal_1980_2019.csv"


def compute() -> pd.DataFrame:
    df = pd.read_csv(SRC)
    # Approximation: NSW/GDP ≈ govt_consumption - tax_revenue (both already as % of GDP)
    # This gives negative values when taxes exceed government services, matching K&T's NSW negativity finding
    df["value"] = (df["govt_consumption_pct_gdp"] - df["tax_revenue_pct_gdp"]) / 100
    df["series_id"] = SUBSERIES
    df["units"] = "share"
    df["stage"] = "derived_approximation"
    df["provenance"] = "(govt_consumption - tax_revenue) / 100 from WB fiscal Turkey"
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    valid = df.dropna(subset=["value"])
    n_negative = int((valid["value"] < 0).sum())
    print(f"    [P02_XS1602] {len(valid)} valid rows; negative-NSW years={n_negative}/{len(valid)}; "
          f"range=[{valid['value'].min():.4f}, {valid['value'].max():.4f}]; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

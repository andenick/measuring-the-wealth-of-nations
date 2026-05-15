"""L01_S201 — Load orthodox GDP, GNP, CFC, NDP for Chapter 2's alternative
GFP comparison.

Source: BEA NIPA Table 1.7.5 (cached). Lines:
  1  GDP
  4  GNP (= GDP + net foreign income)
  5  CFC (consumption of fixed capital, depreciation)
 14  NDP (= GNP - CFC, net national product)
 16  NI (national income)

These are the orthodox aggregates we compare to S&T's Marxian GFP*.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.bea_cache import load_bea_line  # noqa: E402


def load_nipa_aggregates() -> pd.DataFrame:
    """Returns DataFrame: year, GDP, GNP, CFC, NDP (all in BILLIONS USD)."""
    GDP = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 1).rename(columns={"value": "GDP"})
    GNP = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 4).rename(columns={"value": "GNP"})
    CFC = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 5).rename(columns={"value": "CFC"})
    NDP = load_bea_line("nipa_1_7_5_gross_output_by_industry.csv", 14).rename(columns={"value": "NDP"})
    merged = GDP.merge(GNP, on="year").merge(CFC, on="year").merge(NDP, on="year")
    # millions -> billions
    for c in ("GDP", "GNP", "CFC", "NDP"):
        merged[c] = merged[c] / 1000.0
    return merged.sort_values("year").reset_index(drop=True)


def run():
    df = load_nipa_aggregates()
    print(f"    [L01_S201] NIPA aggregates: {len(df)} rows {df['year'].min()}-{df['year'].max()}; "
          f"GDP 1929=${df.iloc[0]['GDP']:.1f}B, 2024=${df.iloc[-1]['GDP']:.0f}B")
    return df


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""M02 - Adjust Profit Rates: restrict K to productive K* (DIV-001 resolution).

Removes financial-sector capital stock from the denominator of the Marxian
profit rate r* = S* / (C*m + K*).

Approximation: K* = Total private nonresidential - Financial corporate
(BEA Fixed Assets Table 4.1, Lines 1 and 33)

This is a FIRST APPROXIMATION. The book's K* also excludes real estate,
legal services, and other unproductive sectors, but Table 4.1 doesn't
provide that level of industry detail. See DEC-010.

Inputs:
  - Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv
  - data/final-data/series/T505.csv (S* — surplus value)
  - data/final-data/series/T504.csv (V* — variable capital)
Outputs:
  - data/adjusted-final-data/T513_adjusted.csv (r* with K*)
  - data/adjusted-final-data/T514_adjusted.csv (r*_adj with K*)
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import SERIES_OUT, ADJUSTED, INPUTS, API_DATA, ensure_dirs

ADJUSTMENT_ID = "ADJ-001"


def _load_capital_stock():
    """Load K and K* from BEA Fixed Assets Table 4.1."""
    path = API_DATA / "BEA" / "fixed_assets_4_1_net_stock.csv"
    df = pd.read_csv(path)

    # Line 1 = Total private nonresidential fixed assets
    total = df[df["LineNumber"] == 1][["TimePeriod", "DataValue"]].copy()
    total["DataValue"] = total["DataValue"].astype(str).str.replace(",", "").astype(float)
    total = total.set_index("TimePeriod")["DataValue"]
    total.index = total.index.astype(int)

    # Line 33 = Financial corporate (unproductive capital)
    financial = df[df["LineNumber"] == 33][["TimePeriod", "DataValue"]].copy()
    financial["DataValue"] = financial["DataValue"].astype(str).str.replace(",", "").astype(float)
    financial = financial.set_index("TimePeriod")["DataValue"]
    financial.index = financial.index.astype(int)

    # K* = Total - Financial
    common = total.index.intersection(financial.index)
    k_total = total.loc[common]
    k_star = total.loc[common] - financial.loc[common]

    return k_total, k_star


def adjust(series_filter=None):
    """Execute ADJ-001: restrict K to K* for profit rate."""
    ensure_dirs()
    ADJUSTED.mkdir(parents=True, exist_ok=True)
    steps = []

    k_total, k_star = _load_capital_stock()
    steps.append(f"Capital stock: {len(k_total)} years ({k_total.index.min()}-{k_total.index.max()})")

    # K is already in millions (UNIT_MULT=6 in BEA = millions of dollars)
    # T505 (S*) is also in millions, so units are consistent
    k_total_m = k_total
    k_star_m = k_star

    # Load S* and V*
    t505 = pd.read_csv(SERIES_OUT / "T505.csv", index_col=0)["combined"]
    t504 = pd.read_csv(SERIES_OUT / "T504.csv", index_col=0)["combined"]
    steps.append(f"S*: {len(t505)} rows, V*: {len(t504)} rows")

    # Load existing T513 (current r* with total K)
    t513 = pd.read_csv(SERIES_OUT / "T513.csv", index_col=0)
    t513_book = t513["book"] if "book" in t513.columns else t513.iloc[:, 0]
    t513_combined = t513["combined"]

    # T513 is already a correctly computed ratio from pre-computed source data.
    # DIV-001: T513 used total K instead of productive K* in its denominator.
    # The adjustment: multiply T513 by K/K* (since smaller K* in denominator = higher r*)
    # r*_adjusted = r*_original × (K_total / K_productive)

    common_years = t513_combined.index.intersection(k_star_m.index).intersection(k_total_m.index)
    r_star_adj = pd.Series(dtype=float, name="r_star_adjusted")

    for yr in common_years:
        r_orig = t513_combined.get(yr)
        k_total_val = k_total_m.get(yr)
        k_star_val = k_star_m.get(yr)
        if r_orig is not None and k_star_val is not None and k_star_val > 0:
            adjustment_factor = k_total_val / k_star_val
            r_star_adj[yr] = r_orig * adjustment_factor

    steps.append(f"Adjusted r*: {len(r_star_adj)} years computed")

    # Compare with original
    common_comp = t513_combined.index.intersection(r_star_adj.index)
    if len(common_comp) > 0:
        orig = t513_combined.loc[common_comp]
        adj = r_star_adj.loc[common_comp]
        ratio = (adj / orig).dropna()
        if len(ratio) > 0:
            steps.append(f"K* adjustment effect: r* increases by {(ratio.mean()-1)*100:.1f}% on average")

    # Benchmark comparison
    for yr in [1948, 1958, 1967, 1977, 1989]:
        if yr in r_star_adj.index and yr in t513_combined.index:
            orig = t513_combined[yr]
            adj = r_star_adj[yr]
            steps.append(f"  r*[{yr}]: original={orig:.4f}, K*-adjusted={adj:.4f} ({(adj/orig-1)*100:+.1f}%)")

    # Save adjusted T513
    t513_out = pd.DataFrame({
        "book": t513_book,
        "combined": t513_combined,
        "k_star_adjusted": r_star_adj,
    })
    t513_out.index.name = "year"
    t513_path = ADJUSTED / "T513_adjusted.csv"
    t513_out.to_csv(t513_path)

    # T514 (capacity-adjusted) — apply same K*/K ratio
    t514 = pd.read_csv(SERIES_OUT / "T514.csv", index_col=0)
    t514_combined = t514["combined"]
    k_ratio = (k_star_m / k_total_m).reindex(t514_combined.index)
    t514_adj = t514_combined / k_ratio.reindex(t514_combined.index)  # scale up by K/K*

    t514_out = pd.DataFrame({
        "book": t514["book"] if "book" in t514.columns else t514.iloc[:, 0],
        "combined": t514_combined,
        "k_star_adjusted": t514_adj,
    })
    t514_out.index.name = "year"
    t514_path = ADJUSTED / "T514_adjusted.csv"
    t514_out.to_csv(t514_path)
    steps.append(f"T514 adjusted: {len(t514_adj.dropna())} years")

    print(f"    [M02] ADJ-001 executed: {len(steps)} steps")
    for s in steps:
        print(f"      {s}")

    return {
        "script": "M02_adjust_profit_rates",
        "adjustment_id": ADJUSTMENT_ID,
        "status": "ok",
        "steps": steps,
        "outputs": [str(t513_path), str(t514_path)],
    }


if __name__ == "__main__":
    result = adjust()
    print(json.dumps(result, indent=2, default=str))

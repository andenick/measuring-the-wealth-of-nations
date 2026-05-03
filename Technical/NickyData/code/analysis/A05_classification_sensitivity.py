#!/usr/bin/env python3
"""A05 - Classification Sensitivity: how sector classification affects exploitation rate.

Tests 3 NAICS classification variants:
  1. Broad (ST-like): 48 productive sectors (current default)
  2. Narrow (Mohun-like): Remove debatable sectors (~35 productive)
  3. Ultra-narrow: Only goods-producing + freight transport (~25 productive)

Output: outputs/analysis/classification_sensitivity.json
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import INPUTS, ANALYSIS_OUT
from utils.io.naics_classification import NAICS_CLASSIFICATION

GDP_PATH = INPUTS / "API_Data" / "BEA" / "gdp_by_industry_gross_output.csv"

# Classification variants
NARROW_REMOVE = {
    "61", "621", "622", "623", "624",  # Education + health
    "511", "513", "514",               # Information
    "81",                              # Other services
    "721", "722",                      # Accommodation + food services
}

ULTRA_NARROW_KEEP = {
    "111CA", "113FF",                  # Agriculture
    "211", "212", "213",               # Mining
    "22",                              # Utilities
    "23",                              # Construction
    "311FT", "313TT", "315AL", "321", "322", "323", "324", "325", "326", "327",
    "331", "332", "333", "334", "335", "3361MV", "3364OT", "337", "339",  # Manufacturing
    "481", "482", "483", "484", "486", # Transport (freight)
    "493",                             # Warehousing
}


def generate():
    ANALYSIS_OUT.mkdir(parents=True, exist_ok=True)

    if not GDP_PATH.exists():
        print("    [A05] GDP data not found")
        return {"status": "skip"}

    df = pd.read_csv(GDP_PATH)
    results = {}

    for year in [1997, 2002, 2007, 2012, 2017]:
        yr_data = df[df["Year"] == year].set_index("Industry")["DataValue"].astype(float)

        # Variant 1: Broad (current)
        broad_codes = [k for k, v in NAICS_CLASSIFICATION.items() if v == "productive"]
        broad_go = sum(yr_data.get(c, 0) for c in broad_codes)

        # Variant 2: Narrow (remove debatable)
        narrow_codes = [c for c in broad_codes if c not in NARROW_REMOVE]
        narrow_go = sum(yr_data.get(c, 0) for c in narrow_codes)

        # Variant 3: Ultra-narrow (goods + freight only)
        ultra_go = sum(yr_data.get(c, 0) for c in ULTRA_NARROW_KEEP)

        total = float(yr_data.get("II", yr_data.sum()))

        results[year] = {
            "broad": {"n_sectors": len(broad_codes), "go": round(broad_go, 1), "share": round(broad_go / total, 4) if total > 0 else 0},
            "narrow": {"n_sectors": len(narrow_codes), "go": round(narrow_go, 1), "share": round(narrow_go / total, 4) if total > 0 else 0},
            "ultra_narrow": {"n_sectors": len(ULTRA_NARROW_KEEP), "go": round(ultra_go, 1), "share": round(ultra_go / total, 4) if total > 0 else 0},
            "ratio_broad_narrow": round(broad_go / narrow_go, 4) if narrow_go > 0 else 0,
            "ratio_broad_ultra": round(broad_go / ultra_go, 4) if ultra_go > 0 else 0,
        }

        print(f"    [A05] {year}: broad={broad_go:.0f}B ({broad_go/total:.0%}), narrow={narrow_go:.0f}B ({narrow_go/total:.0%}), ultra={ultra_go:.0f}B ({ultra_go/total:.0%})")

    with open(ANALYSIS_OUT / "classification_sensitivity.json", "w") as f:
        json.dump(results, f, indent=2)

    return {"status": "ok", "results": results}


if __name__ == "__main__":
    generate()

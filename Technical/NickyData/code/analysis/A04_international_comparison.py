#!/usr/bin/env python3
"""A04 - International Comparison: US vs Turkey vs NZ.

Output: outputs/analysis/international_comparison.json
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, STUDIES_OUT, ANALYSIS_OUT

def _load(sid):
    for d in [SERIES_OUT, STUDIES_OUT]:
        path = d / f"{sid}.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            col = "combined" if "combined" in df.columns else df.columns[-1]
            return df[col]
    return pd.Series(dtype=float)

def generate():
    ANALYSIS_OUT.mkdir(parents=True, exist_ok=True)

    result = {}

    # Turkey NSW
    turkey = _load("N1602")
    if len(turkey) > 0:
        result["turkey"] = {
            "period": f"{int(turkey.index.min())}-{int(turkey.index.max())}",
            "mean_nsw_gdp": round(float(turkey.mean()), 4),
            "all_negative": bool((turkey < 0).all()),
            "n_years": len(turkey),
        }

    # NZ productive share
    nz = _load("N1701")
    if len(nz) > 0:
        result["new_zealand"] = {
            "period": f"{int(nz.index.min())}-{int(nz.index.max())}",
            "mean_productive_share": round(float(nz.mean()), 4),
            "n_years": len(nz),
        }

    with open(ANALYSIS_OUT / "international_comparison.json", "w") as f:
        json.dump(result, f, indent=2)

    for country, data in result.items():
        print(f"    [A04] {country}: {data}")
    return {"status": "ok", **result}

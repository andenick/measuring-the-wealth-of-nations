#!/usr/bin/env python3
"""A03 - Moos Structural Shift: quantify pre/post-2000 NSW reversal.

Key finding: NSW reverses from -1.1% to +1.4% GDP after 2000.

Output: outputs/analysis/moos_shift_analysis.json
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, STUDIES_OUT, ANALYSIS_OUT

def generate():
    ANALYSIS_OUT.mkdir(parents=True, exist_ok=True)

    # Load Moos NSW/GDP
    for d in [SERIES_OUT, STUDIES_OUT]:
        path = d / "N1301.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            nsw = df["combined"] if "combined" in df.columns else df.iloc[:, -1]
            break
    else:
        print("    [A03] N1301 not found")
        return {"status": "skip"}

    pre = nsw[(nsw.index >= 1959) & (nsw.index <= 2000)]
    post = nsw[(nsw.index >= 2001)]

    result = {
        "pre_2000": {"mean": round(float(pre.mean()), 4), "n_years": len(pre)} if len(pre) > 0 else None,
        "post_2000": {"mean": round(float(post.mean()), 4), "n_years": len(post)} if len(post) > 0 else None,
        "shift": round(float(post.mean() - pre.mean()), 4) if len(pre) > 0 and len(post) > 0 else None,
    }

    with open(ANALYSIS_OUT / "moos_shift_analysis.json", "w") as f:
        json.dump(result, f, indent=2)

    if result["shift"] is not None:
        print(f"    [A03] Moos shift: pre={result['pre_2000']['mean']:.4f}, post={result['post_2000']['mean']:.4f}, shift={result['shift']:+.4f}")
    return {"status": "ok", **result}

#!/usr/bin/env python3
"""A01 - NSW Cross-Study Comparison: unified NSW database across all studies.

Combines NSW estimates from: ST94 (book), ST87, ST02, Moos17, Turkey22.

Output: outputs/analysis/cross_study_nsw/nsw_comparison.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, STUDIES_OUT, ANALYSIS_OUT

def _load(sid, directory=SERIES_OUT):
    path = directory / f"{sid}.csv"
    if not path.exists():
        path = STUDIES_OUT / f"{sid}.csv"
    if not path.exists():
        return pd.Series(dtype=float, name=sid)
    df = pd.read_csv(path, index_col=0)
    col = "combined" if "combined" in df.columns else df.columns[-1]
    return df[col].rename(sid)

def generate():
    out_dir = ANALYSIS_OUT / "cross_study_nsw"
    out_dir.mkdir(parents=True, exist_ok=True)

    nsw = pd.DataFrame({
        "T607_ST94_NSW_billions": _load("T607"),
        "N1101_ST87_NetTransfer": _load("N1101"),
        "N1202_ST02_NSW_EC": _load("N1202"),
        "N1301_Moos_NSW_GDP": _load("N1301"),
        "N1302_Moos_NSW_EC": _load("N1302"),
        "N1602_Turkey_NSW_GDP": _load("N1602"),
    })
    nsw.index.name = "year"
    path = out_dir / "nsw_comparison.csv"
    nsw.to_csv(path)

    n = sum(1 for s in nsw.columns if nsw[s].notna().any())
    print(f"    [A01] NSW comparison: {len(nsw)} years x {n} studies -> {path.name}")
    return {"status": "ok", "studies": n, "years": len(nsw)}

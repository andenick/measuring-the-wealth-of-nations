#!/usr/bin/env python3
"""L13 - Load Cross-Study Comparison: T801.

Loads Mohun exploitation rates and the pre-built ST-vs-Mohun comparison
from Inputs/ExternalSources/Mohun/.

Inputs:  Inputs/ExternalSources/Mohun/mohun_exploitation_rates_1948_1989_CORRECTED.csv
         Inputs/ExternalSources/Mohun/detailed_exploitation_comparison_ST_vs_Mohun.csv
Outputs: parsed-raw/T801_mohun_parsed.csv, T801_comparison_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import INPUTS, PARSED_RAW, ensure_dirs

SERIES_IDS = ["T801"]

MOHUN_DIR = INPUTS / "ExternalSources" / "Mohun"


def load():
    """Load Mohun comparison data for cross-study analysis."""
    ensure_dirs()
    outputs = []

    # Load Mohun corrected exploitation rates (1948-1989)
    mohun_path = MOHUN_DIR / "mohun_exploitation_rates_1948_1989_CORRECTED.csv"
    if mohun_path.exists():
        df = pd.read_csv(mohun_path, index_col=0)
        df.index = df.index.astype(int)
        df.index.name = "year"
        out_path = PARSED_RAW / "T801_mohun_parsed.csv"
        df.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L13] T801: Mohun exploitation rates loaded ({len(df)} rows)")
    else:
        print(f"    [L13] T801: Mohun data not found at {mohun_path}")

    # Load pre-built detailed comparison
    comp_path = MOHUN_DIR / "detailed_exploitation_comparison_ST_vs_Mohun.csv"
    if comp_path.exists():
        comp = pd.read_csv(comp_path, index_col=0)
        comp.index = comp.index.astype(int)
        comp.index.name = "year"
        out_path = PARSED_RAW / "T801_comparison_parsed.csv"
        comp.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L13] T801: ST-vs-Mohun comparison loaded ({len(comp)} rows)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok" if outputs else "fail",
        "message": f"Cross-study comparison | {len(outputs)} files loaded",
        "outputs": outputs,
    }

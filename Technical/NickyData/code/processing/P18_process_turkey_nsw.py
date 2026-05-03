#!/usr/bin/env python3
"""P18 - Process Karabacak & Tonak (2022) Turkey NSW: N1601-N1602.

Loads real data from Inputs/ExternalSources/Turkey2022/ if available.
If data unavailable, marks series as data_unavailable (NO synthetic generation).

Key finding: NSW negative for ALL 40 years (1980-2019), average -1.13% GDP.

Inputs:  Inputs/ExternalSources/Turkey2022/*.csv (if available)
Outputs: final-data/studies/series/N1601-N1602.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import STUDIES_OUT, INPUTS, ensure_dirs

SERIES_ID = "N1601"
SERIES_IDS = ["N1601", "N1602"]
PRIORITY = 14

TURKEY_DIR = INPUTS / "ExternalSources" / "Turkey2022"


def process():
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    labor_share_path = TURKEY_DIR / "turkey_labor_share_1980_2019.csv"
    nsw_path = TURKEY_DIR / "turkey_nsw_gdp_1980_2019.csv"

    if labor_share_path.exists():
        df = pd.read_csv(labor_share_path, index_col=0)
        col = df.columns[0]
        labor_share = df[col].dropna()
        out = pd.DataFrame({"book": labor_share, "combined": labor_share})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1601.csv")
        data_dict["N1601"] = labor_share
        outputs.append(str(STUDIES_OUT / "N1601.csv"))
        steps.append(f"N1601: {len(labor_share)} years (Turkey labor share, primary)")
        print(f"    [P18] N1601: {len(labor_share)} years (primary)")
    else:
        steps.append("N1601: data_unavailable (requires TURKSTAT or figure digitization)")
        print("    [P18] N1601: data_unavailable")

    if nsw_path.exists():
        df = pd.read_csv(nsw_path, index_col=0)
        col = df.columns[0]
        nsw = df[col].dropna()
        out = pd.DataFrame({"book": nsw, "combined": nsw})
        out.index.name = "year"
        out.to_csv(STUDIES_OUT / "N1602.csv")
        data_dict["N1602"] = nsw
        outputs.append(str(STUDIES_OUT / "N1602.csv"))
        steps.append(f"N1602: {len(nsw)} years (Turkey NSW/GDP, primary)")
        print(f"    [P18] N1602: {len(nsw)} years (primary)")
    else:
        steps.append("N1602: data_unavailable (requires TURKSTAT or figure digitization)")
        print("    [P18] N1602: data_unavailable")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "data_unavailable",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

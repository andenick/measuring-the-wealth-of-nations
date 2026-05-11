#!/usr/bin/env python3
"""P11 - Process net social wage: T607 (NSW), T608 (NSW/V*), T609 (NSW/NI).

T607 and T609 from parsed CSVs. T608 = T607 / T504 (derived ratio).

Inputs:  parsed-raw/T607_parsed.csv, T609_parsed.csv (from L09)
         final-data/series/T504.csv (from P02 — for T608 derivation)
Outputs: final-data/series/T607.csv, T608.csv, T609.csv
Dependencies: L09, P02 (for T504)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from lib.paths import SERIES_OUT, ensure_dirs
from lib.data_io import load_parsed

SERIES_ID = "T607"
SERIES_IDS = ["T607", "T608", "T609"]
PRIORITY = 4


def process():
    """Process NSW series including derived NSW/V* ratio."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # T607: NSW (billions)
    t607_df, _ = load_parsed("T607")
    if t607_df is not None:
        nsw = t607_df["value"]
        out = pd.DataFrame({"book": nsw, "combined": nsw})
        out.index.name = "year"
        out_path = SERIES_OUT / "T607.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["T607"] = nsw
        steps.append(f"T607: {len(nsw)} rows")
        print(f"    [P11] T607: {len(nsw)} rows")

        # Validate: NSW should be < 0 for most years
        neg_frac = (nsw < 0).sum() / len(nsw)
        if neg_frac < 0.5:
            steps.append(f"T607 WARN: only {neg_frac:.0%} negative (expected >50%)")
    else:
        steps.append("T607: parsed file not found")

    # T608: NSW/V* (derived)
    t504_path = SERIES_OUT / "T504.csv"
    if t607_df is not None and t504_path.exists():
        v_star = pd.read_csv(t504_path, index_col=0)["combined"].dropna()
        nsw = t607_df["value"]
        common = nsw.index.intersection(v_star.index)
        nsw_v = nsw[common] / v_star[common]
        out = pd.DataFrame({"book": nsw_v, "combined": nsw_v})
        out.index.name = "year"
        out_path = SERIES_OUT / "T608.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["T608"] = nsw_v
        steps.append(f"T608: {len(nsw_v)} rows (NSW/V*)")
        print(f"    [P11] T608: {len(nsw_v)} rows (derived)")
    else:
        steps.append("T608: could not derive (T607 or T504 missing)")

    # T609: NSW/NI share
    t609_df, _ = load_parsed("T609")
    if t609_df is not None:
        nsw_ni = t609_df["value"]
        out = pd.DataFrame({"book": nsw_ni, "combined": nsw_ni})
        out.index.name = "year"
        out_path = SERIES_OUT / "T609.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict["T609"] = nsw_ni
        steps.append(f"T609: {len(nsw_ni)} rows")
        print(f"    [P11] T609: {len(nsw_ni)} rows")
    else:
        steps.append("T609: parsed file not found")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

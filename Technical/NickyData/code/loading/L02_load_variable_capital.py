#!/usr/bin/env python3
"""L02 - Load Variable Capital & Surplus Value: T504, T505.

Input:   ch05/VariableCapital_SurplusValue.csv (Format B, 1948-1989)
Column map: T504←T504_V_star (÷1000), T505←T505_S_star (÷1000)
Outputs: parsed-raw/T504_parsed.csv, T505_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T504", "T505"]

COLUMN_MAP = {
    "T504": "T504_V_star",
    "T505": "T505_S_star",
}


def load():
    """Load variable capital and surplus value, converting millions→billions."""
    ensure_dirs()

    source = ST_CHOPPED / "ch05" / "VariableCapital_SurplusValue.csv"
    if not source.exists():
        return {
            "series_id": SERIES_IDS[0],
            "status": "fail",
            "message": f"Source not found: {source}",
            "outputs": [],
        }

    df = load_chopped_direct(source, columns=list(COLUMN_MAP.values()))
    outputs = []

    for sid, col in COLUMN_MAP.items():
        if col not in df.columns:
            print(f"    [L02] {sid}: column {col} not found")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        # Convert millions to billions
        out["value"] = out["value"] / 1000.0
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L02] {sid}: {len(out)} rows ({col} ÷1000 → billions)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Variable capital/surplus | {len(outputs)} series, 1948-1989",
        "outputs": outputs,
    }

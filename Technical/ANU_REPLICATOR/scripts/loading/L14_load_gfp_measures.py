#!/usr/bin/env python3
"""L14 - Load Alternative GFP Measures: T201.

Loads orthodox GDP, CFC (consumption of fixed capital), and NDP from
BEA NIPA Table 1.7.5 for comparison with Marxian GFP/FP*.

Inputs:  data/api-data/BEA/nipa_1_7_5_gross_output_by_industry.csv
Outputs: parsed-raw/T201_orthodox_parsed.csv
Dependencies: None (requires BEA API data to have been fetched)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from lib.paths import API_DATA, PARSED_RAW, ensure_dirs
from lib.api_data_io import load_bea_nipa

SERIES_IDS = ["T201"]

NIPA_FILE = API_DATA / "BEA" / "nipa_1_7_5_gross_output_by_industry.csv"
LINES = [
    "Gross domestic product (GDP)",
    "Less: Consumption of fixed capital",
    "Net domestic product",
]


def load():
    """Load orthodox national accounts (GDP, CFC, NDP) for GFP comparison."""
    ensure_dirs()

    if not NIPA_FILE.exists():
        print(f"    [L14] T201: BEA NIPA file not found")
        return {
            "series_id": SERIES_IDS[0],
            "status": "fail",
            "message": f"BEA NIPA not found: {NIPA_FILE}",
            "outputs": [],
        }

    df = load_bea_nipa(NIPA_FILE, line_filter=LINES)

    # Rename columns to clean names
    col_map = {}
    for col in df.columns:
        if "GDP" in col:
            col_map[col] = "GDP"
        elif "Consumption of fixed capital" in col:
            col_map[col] = "CFC"
        elif "Net domestic product" in col:
            col_map[col] = "NDP"
    df = df.rename(columns=col_map)

    # CFC is reported as "Less: ..." so values are positive amounts to subtract
    # Verify NDP = GDP - CFC
    if "GDP" in df.columns and "CFC" in df.columns and "NDP" not in df.columns:
        df["NDP"] = df["GDP"] - df["CFC"]

    out_path = PARSED_RAW / "T201_orthodox_parsed.csv"
    df.to_csv(out_path)

    n_years = len(df)
    yr_range = f"{df.index.min()}-{df.index.max()}"
    print(f"    [L14] T201: orthodox GDP/CFC/NDP loaded ({n_years} rows, {yr_range})")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Alternative GFP measures | {n_years} rows ({yr_range})",
        "outputs": [str(out_path)],
    }

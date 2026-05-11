#!/usr/bin/env python3
"""L15 - Load Mohun (2005) data: N1401-N1404.

Loads exploitation rates, employment, and variable capital from
existing Mohun CSV files at Inputs/ExternalSources/Mohun/.

Inputs:
  - Inputs/ExternalSources/Mohun/mohun_exploitation_rates_1948_1989.csv
  - Inputs/ExternalSources/Mohun/mohun_employment_annual_1948_1989.csv
  - Inputs/ExternalSources/Mohun/detailed_exploitation_comparison_ST_vs_Mohun.csv
Outputs:
  - data/raw-data/parsed/N1401_parsed.csv (exploitation rate)
  - data/raw-data/parsed/N1402_parsed.csv (productive labor)
  - data/raw-data/parsed/N1403_parsed.csv (variable capital)
  - data/raw-data/parsed/N1404_parsed.csv (ST vs Mohun comparison)
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import INPUTS, RAW_DATA, ensure_dirs

SERIES_ID = "N1401"
SERIES_IDS = ["N1401", "N1402", "N1403", "N1404"]
PRIORITY = 12

MOHUN_DIR = INPUTS / "ExternalSources" / "Mohun"


def load():
    ensure_dirs()
    parsed_dir = RAW_DATA / "parsed"
    parsed_dir.mkdir(parents=True, exist_ok=True)
    steps = []
    outputs = []

    # N1401: Mohun exploitation rate (e_mohun)
    expl_path = MOHUN_DIR / "mohun_exploitation_rates_1948_1989.csv"
    if expl_path.exists():
        df = pd.read_csv(expl_path)
        if "year" in df.columns and "e_mohun" in df.columns:
            out = df[["year", "e_mohun"]].rename(columns={"e_mohun": "value"})
            out = out.set_index("year")
            out_path = parsed_dir / "N1401_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            steps.append(f"N1401: {len(out)} rows (Mohun e, {out.index.min()}-{out.index.max()})")
            print(f"    [L15] N1401: {len(out)} rows (Mohun exploitation rate)")

    # N1402: Mohun productive labor share (Lp/L)
    emp_path = MOHUN_DIR / "mohun_employment_annual_1948_1989.csv"
    if emp_path.exists():
        df = pd.read_csv(emp_path)
        if "year" in df.columns and "Lp_mohun_L_ratio" in df.columns:
            out = df[["year", "Lp_mohun_L_ratio"]].rename(columns={"Lp_mohun_L_ratio": "value"})
            out = out.set_index("year")
            out_path = parsed_dir / "N1402_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            steps.append(f"N1402: {len(out)} rows (Mohun Lp/L share)")
            print(f"    [L15] N1402: {len(out)} rows (Mohun productive labor share)")

    # N1403: Mohun variable capital
    vc_path = MOHUN_DIR / "mohun_variable_capital_1948_1989.csv"
    if vc_path.exists():
        df = pd.read_csv(vc_path)
        if "year" in df.columns:
            # Use the first value column
            val_cols = [c for c in df.columns if c != "year"]
            if val_cols:
                out = df[["year", val_cols[0]]].rename(columns={val_cols[0]: "value"})
                out = out.set_index("year")
                out_path = parsed_dir / "N1403_parsed.csv"
                out.to_csv(out_path)
                outputs.append(str(out_path))
                steps.append(f"N1403: {len(out)} rows (Mohun V*)")
                print(f"    [L15] N1403: {len(out)} rows (Mohun variable capital)")

    # N1404: ST vs Mohun comparison
    comp_path = MOHUN_DIR / "detailed_exploitation_comparison_ST_vs_Mohun.csv"
    if comp_path.exists():
        df = pd.read_csv(comp_path)
        if "year" in df.columns:
            out_path = parsed_dir / "N1404_parsed.csv"
            df.to_csv(out_path, index=False)
            outputs.append(str(out_path))
            steps.append(f"N1404: {len(df)} rows (ST vs Mohun comparison)")
            print(f"    [L15] N1404: {len(df)} rows (comparison)")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if outputs else "fail",
        "message": f"Loaded {len(outputs)} Mohun series",
        "steps": steps,
        "outputs": outputs,
    }

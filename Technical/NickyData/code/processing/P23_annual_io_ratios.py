#!/usr/bin/env python3
"""P23 - Compute annual IO productive sector ratios from L21/L22 data.

Replaces the frozen IO_productive_ratios.csv with annually-varying ratios.
For 1990-1996 (SIC-era gap): log-linear interpolation per DEC-007.
For 1978-1989: extrapolation from 1977 SIC benchmark.

Inputs:  parsed-raw/annual_io_va_ratios.csv (from L21)
         parsed-raw/annual_productive_employment.csv (from L22)
         parsed-raw/annual_productive_compensation.csv (from L22)
         final-data/book/series/K_star_by_industry.csv (from L20)
Outputs: final-data/book/series/IO_productive_ratios.csv (replaces frozen version)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs

SERIES_IDS = []
PRIORITY = 23

BOOK_RATIOS = {
    1948: {"output": 0.574, "employment": 0.570, "compensation": 0.540},
    1958: {"output": 0.560, "employment": 0.520, "compensation": 0.490},
    1967: {"output": 0.550, "employment": 0.480, "compensation": 0.460},
    1972: {"output": 0.540, "employment": 0.470, "compensation": 0.440},
    1977: {"output": 0.530, "employment": 0.450, "compensation": 0.420},
    1989: {"output": 0.520, "employment": 0.370, "compensation": 0.360},
}


def _interpolate_book_period() -> pd.DataFrame:
    """Interpolate between SIC benchmark years for 1948-1989."""
    years = sorted(BOOK_RATIOS.keys())
    all_years = list(range(1948, 1990))
    rows = []

    for yr in all_years:
        if yr in BOOK_RATIOS:
            rows.append({"year": yr, **BOOK_RATIOS[yr]})
        else:
            below = max(y for y in years if y <= yr)
            above = min(y for y in years if y >= yr)
            frac = (yr - below) / (above - below) if above != below else 0
            row = {"year": yr}
            for key in ["output", "employment", "compensation"]:
                row[key] = BOOK_RATIOS[below][key] + frac * (BOOK_RATIOS[above][key] - BOOK_RATIOS[below][key])
            rows.append(row)

    return pd.DataFrame(rows).set_index("year")


def process():
    ensure_dirs()
    steps = []

    # Load NAICS-era data from L21/L22
    va_path = PARSED_RAW / "annual_io_va_ratios.csv"
    emp_path = PARSED_RAW / "annual_productive_employment.csv"
    comp_path = PARSED_RAW / "annual_productive_compensation.csv"

    naics_va = pd.read_csv(va_path, index_col="year") if va_path.exists() else pd.DataFrame()
    naics_emp = pd.read_csv(emp_path, index_col="year") if emp_path.exists() else pd.DataFrame()
    naics_comp = pd.read_csv(comp_path, index_col="year") if comp_path.exists() else pd.DataFrame()

    # Book period (1948-1989): interpolated from SIC benchmarks
    book = _interpolate_book_period()
    steps.append(f"Book period: {len(book)} years (1948-1989) interpolated from {len(BOOK_RATIOS)} benchmarks")

    # Build output DataFrame
    all_years = list(range(1948, 2025))
    result = pd.DataFrame(index=all_years)
    result.index.name = "year"

    # --- Productive output ratio ---
    result["ratio_productive_output"] = np.nan
    result.loc[book.index, "ratio_productive_output"] = book["output"]
    if "ratio_productive_va" in naics_va.columns:
        for yr in naics_va.index:
            if yr in result.index:
                result.loc[yr, "ratio_productive_output"] = naics_va.loc[yr, "ratio_productive_va"]

    # --- Productive employment ratio ---
    result["ratio_productive_employment"] = np.nan
    result.loc[book.index, "ratio_productive_employment"] = book["employment"]
    if "Lp_L" in naics_emp.columns:
        for yr in naics_emp.index:
            if yr in result.index:
                result.loc[yr, "ratio_productive_employment"] = naics_emp.loc[yr, "Lp_L"]

    # --- Productive compensation ratio ---
    result["ratio_productive_compensation"] = np.nan
    result.loc[book.index, "ratio_productive_compensation"] = book["compensation"]
    if "V_star_W" in naics_comp.columns:
        for yr in naics_comp.index:
            if yr in result.index:
                result.loc[yr, "ratio_productive_compensation"] = naics_comp.loc[yr, "V_star_W"]

    # --- Productive materials ratio ---
    result["ratio_productive_materials"] = np.nan
    result.loc[book.index, "ratio_productive_materials"] = book["output"] * 0.3

    # Interpolate 1990-1997 gap (log-linear between 1989 and first NAICS year)
    for col in result.columns:
        val_1989 = result.loc[1989, col]
        first_naics = result.loc[1998:, col].first_valid_index()
        if first_naics and pd.notna(val_1989):
            val_naics = result.loc[first_naics, col]
            if val_1989 > 0 and val_naics > 0:
                for yr in range(1990, first_naics):
                    frac = (yr - 1989) / (first_naics - 1989)
                    result.loc[yr, col] = val_1989 * (val_naics / val_1989) ** frac

    result = result.dropna(how="all")
    steps.append(f"NAICS era: {len(naics_va)} VA years, {len(naics_emp)} FTE years, {len(naics_comp)} comp years")
    steps.append(f"Total: {len(result)} years ({result.index.min()}-{result.index.max()})")

    # Write output (replaces frozen version)
    out_path = SERIES_OUT / "IO_productive_ratios.csv"
    result.to_csv(out_path)

    summary = f"IO ratios: {len(result)} years, book+NAICS, annually varying"
    print(f"    [P23] {summary}")
    return {"status": "ok", "summary": summary, "steps": steps}

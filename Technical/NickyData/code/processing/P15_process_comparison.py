#!/usr/bin/env python3
"""P15 - Process cross-study comparison (T801) and alternative GFP (T201).

T801: Merge ST pipeline exploitation/labor metrics with Mohun data.
T201: Compare Marxian GFP/FP* to orthodox GDP/NDP.

Inputs:  parsed-raw/T801_mohun_parsed.csv (from L13)
         parsed-raw/T201_orthodox_parsed.csv (from L14)
         final-data/series/T506.csv, T511.csv, T512.csv (from P04, P05)
         final-data/series/T503.csv (from P01)
Outputs: final-data/series/T801.csv, T201.csv
Dependencies: L13, L14, P01 (T503), P04 (T506), P05 (T511/T512)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs

SERIES_ID = "T801"
SERIES_IDS = ["T801", "T201"]
PRIORITY = 12


def _load_series_csv(series_id):
    """Load a final series CSV from SERIES_OUT."""
    path = SERIES_OUT / f"{series_id}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    return df


def _process_t801():
    """Cross-study comparison: ST pipeline vs Mohun."""
    steps = []
    outputs = []

    # Load Mohun parsed data
    mohun_path = PARSED_RAW / "T801_mohun_parsed.csv"
    if not mohun_path.exists():
        steps.append("T801: Mohun parsed data not found")
        return None, steps, outputs

    mohun = pd.read_csv(mohun_path, index_col=0)
    mohun.index = mohun.index.astype(int)

    # Load ST pipeline results
    t506 = _load_series_csv("T506")  # exploitation rate
    t511 = _load_series_csv("T511")  # Lp/L
    t512 = _load_series_csv("T512")  # V*/W

    if t506 is None:
        steps.append("T801: T506 (exploitation rate) not available")
        return None, steps, outputs

    # Build comparison table at overlapping years
    st_e = t506["combined"] if "combined" in t506.columns else t506.iloc[:, 0]
    mohun_e = mohun["e_mohun"] if "e_mohun" in mohun.columns else pd.Series(dtype=float)

    common_years = sorted(set(st_e.dropna().index) & set(mohun_e.dropna().index))
    if not common_years:
        steps.append("T801: no overlapping years between ST and Mohun")
        return None, steps, outputs

    out = pd.DataFrame(index=common_years)
    out.index.name = "year"
    out["ST_e"] = st_e.reindex(common_years)
    out["Mohun_e"] = mohun_e.reindex(common_years)
    out["e_diff"] = out["ST_e"] - out["Mohun_e"]

    if t511 is not None:
        st_lpl = t511["combined"] if "combined" in t511.columns else t511.iloc[:, 0]
        out["ST_LpL"] = st_lpl.reindex(common_years)
    if "lambda_lp_pct" in mohun.columns:
        out["Mohun_LpL"] = (mohun["lambda_lp_pct"] / 100).reindex(common_years)
    if t512 is not None:
        st_vw = t512["combined"] if "combined" in t512.columns else t512.iloc[:, 0]
        out["ST_VW"] = st_vw.reindex(common_years)

    # Deviation metrics
    valid = out[["ST_e", "Mohun_e"]].dropna()
    if len(valid) > 2:
        mad = np.abs(valid["ST_e"] - valid["Mohun_e"]).mean()
        corr = valid["ST_e"].corr(valid["Mohun_e"])
        steps.append(f"T801: {len(valid)} overlapping years, MAD={mad:.4f}, corr={corr:.4f}")
    else:
        steps.append(f"T801: {len(valid)} overlapping years (insufficient for metrics)")

    out_path = SERIES_OUT / "T801.csv"
    out.to_csv(out_path)
    outputs.append(str(out_path))
    print(f"    [P15] T801: {len(out)} years, ST vs Mohun exploitation rates")

    return out["ST_e"], steps, outputs


def _process_t201():
    """Alternative GFP: Marxian GFP/FP* vs orthodox GDP/NDP."""
    steps = []
    outputs = []

    # Load orthodox measures
    orthodox_path = PARSED_RAW / "T201_orthodox_parsed.csv"
    if not orthodox_path.exists():
        steps.append("T201: orthodox GDP/CFC/NDP data not found")
        return None, steps, outputs

    orthodox = pd.read_csv(orthodox_path, index_col=0)
    orthodox.index = orthodox.index.astype(int)

    # Load Marxian GFP from T503
    t503 = _load_series_csv("T503")
    if t503 is None:
        steps.append("T201: T503 (GFP) not available from pipeline")
        return None, steps, outputs

    gfp = t503["combined"] if "combined" in t503.columns else t503.iloc[:, 0]

    # Build comparison at overlapping years
    gdp = orthodox["GDP"] if "GDP" in orthodox.columns else pd.Series(dtype=float)
    cfc = orthodox["CFC"] if "CFC" in orthodox.columns else pd.Series(dtype=float)
    ndp = orthodox["NDP"] if "NDP" in orthodox.columns else pd.Series(dtype=float)

    common_years = sorted(set(gfp.dropna().index) & set(gdp.dropna().index))
    if not common_years:
        steps.append("T201: no overlapping years between GFP and GDP")
        return None, steps, outputs

    out = pd.DataFrame(index=common_years)
    out.index.name = "year"
    out["GFP"] = gfp.reindex(common_years)
    out["GDP"] = gdp.reindex(common_years)
    out["CFC"] = cfc.reindex(common_years)
    out["NDP"] = ndp.reindex(common_years)

    # FP* = GFP - CFC (apply orthodox depreciation to Marxian measure)
    if "CFC" in out.columns:
        out["FP_star"] = out["GFP"] - out["CFC"]

    # Ratios: how much of orthodox GDP is "productive" in Marxian sense
    out["GFP_GDP_ratio"] = out["GFP"] / out["GDP"].replace(0, float("nan"))
    if "FP_star" in out.columns and "NDP" in out.columns:
        out["FP_NDP_ratio"] = out["FP_star"] / out["NDP"].replace(0, float("nan"))

    # Summary stats for book period (1948-1961)
    book_mask = (out.index >= 1948) & (out.index <= 1961)
    book_ratio = out.loc[book_mask, "GFP_GDP_ratio"].dropna()
    if len(book_ratio) > 0:
        steps.append(f"T201: book period GFP/GDP ratio: "
                     f"mean={book_ratio.mean():.4f}, range={book_ratio.min():.4f}-{book_ratio.max():.4f}")

    steps.append(f"T201: {len(out)} years, GFP vs GDP comparison")

    out_path = SERIES_OUT / "T201.csv"
    out.to_csv(out_path)
    outputs.append(str(out_path))
    print(f"    [P15] T201: {len(out)} years, Marxian GFP vs orthodox GDP")

    return out["GFP_GDP_ratio"], steps, outputs


def process():
    """Process cross-study comparison and alternative GFP measures."""
    ensure_dirs()
    all_steps = []
    data_dict = {}
    all_outputs = []

    # T801: Cross-study comparison
    t801_data, t801_steps, t801_outputs = _process_t801()
    all_steps.extend(t801_steps)
    all_outputs.extend(t801_outputs)
    if t801_data is not None:
        data_dict["T801"] = t801_data

    # T201: Alternative GFP
    t201_data, t201_steps, t201_outputs = _process_t201()
    all_steps.extend(t201_steps)
    all_outputs.extend(t201_outputs)
    if t201_data is not None:
        data_dict["T201"] = t201_data

    status = "ok" if data_dict else "fail"

    return {
        "series_id": SERIES_ID,
        "status": status,
        "steps": all_steps,
        "data_dict": data_dict,
        "outputs": all_outputs,
    }

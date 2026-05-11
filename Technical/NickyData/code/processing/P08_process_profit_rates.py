#!/usr/bin/env python3
"""P08 - Process profit rates: T513 (r*), T514 (r*_adj).

Uses pre-extended values from ProfitRates_Extended.csv (1948-2024).

Inputs:  parsed-raw/T513_parsed.csv, T514_parsed.csv (from L06)
         parsed-raw/T513_ext_parsed.csv, T514_ext_parsed.csv (from L06)
Outputs: final-data/series/T513.csv, T514.csv
Dependencies: L06. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T513"
SERIES_IDS = ["T513", "T514"]
PRIORITY = 4


def _compute_r_star_from_k_star():
    """Compute r* = S*/K* using industry-level K* if available."""
    k_path = SERIES_OUT / "K_star_by_industry.csv"
    s_path = SERIES_OUT / "T505.csv"
    if not k_path.exists() or not s_path.exists():
        return None, None

    k_df = pd.read_csv(k_path, index_col="year")
    s_df = pd.read_csv(s_path, index_col="year")

    if "K_star_bn" not in k_df.columns:
        return None, None

    k_star = k_df["K_star_bn"].dropna()
    s_star = s_df["combined"].dropna() if "combined" in s_df.columns else None
    if s_star is None:
        return None, None

    common = k_star.index.intersection(s_star.index)
    ext_years = common[common > 1989]
    if len(ext_years) == 0:
        return None, None

    r_star = s_star[ext_years] / k_star[ext_years]
    return r_star, k_star


def process():
    """Process profit rates. Prefer K*-based r* if available, else pre-extended."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Try K*-based computation first
    r_star_k, k_star = _compute_r_star_from_k_star()
    if r_star_k is not None:
        steps.append(f"K* available: {len(k_star)} years, mean K*/K from IO classification")

    for sid in SERIES_IDS:
        book_df, _ = load_parsed(sid)
        book = book_df["value"] if book_df is not None else pd.Series(dtype=float)

        # For T513: try K*-based r* first
        if sid == "T513" and r_star_k is not None:
            combined = pd.concat([book, r_star_k])
            combined = combined[~combined.index.duplicated(keep="first")].sort_index()
            steps.append(f"T513: K*-based r* for {len(r_star_k)} extension years")
            print(f"    [P08] T513: {len(book)} book + {len(r_star_k)} ext (K*-based r*=S*/K*)")
        elif sid == "T514" and r_star_k is not None:
            # r*_adj = r* / TCU
            try:
                from utils.fetchers.fred_fetcher import fetch_fred
                tcu_data = fetch_fred("TCU", start_date="1990-01-01")
                tcu_obs = {int(o["date"][:4]): float(o["value"])/100
                           for o in tcu_data.get("observations", [])
                           if o["value"] != "."}
                tcu = pd.Series(tcu_obs)
                common = r_star_k.index.intersection(tcu.index)
                r_adj = r_star_k[common] / tcu[common]
                combined = pd.concat([book, r_adj])
                combined = combined[~combined.index.duplicated(keep="first")].sort_index()
                steps.append(f"T514: K*-based r*_adj for {len(r_adj)} years")
                print(f"    [P08] T514: {len(book)} book + {len(r_adj)} ext (K*-based, TCU-adjusted)")
            except Exception:
                ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
                if ext_path.exists():
                    ext_df = pd.read_csv(ext_path, index_col=0)
                    ext_df.index = ext_df.index.astype(int)
                    combined = ext_df["value"].dropna().sort_index()
                else:
                    combined = book
        else:
            ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
            if ext_path.exists():
                ext_df = pd.read_csv(ext_path, index_col=0)
                ext_df.index = ext_df.index.astype(int)
                combined = ext_df["value"]
            else:
                combined = book
            combined = combined.dropna().sort_index()

        out = pd.DataFrame({"book": book, "combined": combined})
        out.index.name = "year"
        out_path = SERIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict[sid] = combined

        n_book = book.notna().sum()
        n_total = len(combined)
        steps.append(f"{sid}: {n_book} book, {n_total} combined")
        print(f"    [P08] {sid}: {n_book} book, {n_total} combined rows")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

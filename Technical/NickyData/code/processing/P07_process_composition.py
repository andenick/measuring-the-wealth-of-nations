#!/usr/bin/env python3
"""P07 - Process composition ratios: T507 (S*/Y), T510 (C*/V*).

T507 = S* / (S* + V*) = surplus ratio (share of new value going to surplus)
T510 = C* / V* = value composition of capital (flow ratio)

Book period: passthrough from L05 parsed data.
Extension period: derived from T504 (V*) and T505 (S*) final series.

Inputs:  parsed-raw/T507_parsed.csv, T510_parsed.csv (from L05)
         final-data/series/T504.csv, T505.csv (for extension)
Outputs: final-data/series/T507.csv, T510.csv
Dependencies: L05, P02 (T504), P03 (T505)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T507"
SERIES_IDS = ["T507", "T510"]
PRIORITY = 1


def process():
    """Process composition ratios — book data + derived extension."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Load T504 (V*) and T505 (S*) for extension computation
    t504_path = SERIES_OUT / "T504.csv"
    t505_path = SERIES_OUT / "T505.csv"
    t504 = None
    t505 = None
    if t504_path.exists() and t505_path.exists():
        t504 = pd.read_csv(t504_path, index_col=0)["combined"]
        t505 = pd.read_csv(t505_path, index_col=0)["combined"]

    for sid in SERIES_IDS:
        df, path = load_parsed(sid)
        if df is None:
            steps.append(f"{sid}: parsed file not found at {path}")
            continue

        book = df["value"]

        # Try to extend using T504/T505
        if t504 is not None and t505 is not None:
            ext_years = t504.index[t504.index > book.index.max()]

            if sid == "T507":
                # T507 = S* / (S* + V*) = surplus ratio
                # Only extend where both S* and V* are positive (T505 extension
                # has structural issues near splice point — negative S* values)
                ext = pd.Series(dtype=float)
                for yr in ext_years:
                    s = t505.get(yr)
                    v = t504.get(yr)
                    if s is not None and v is not None and s > 0 and v > 0:
                        ext[yr] = s / (s + v)

            elif sid == "T510":
                # T510 = C*/V* = K*/V* (value composition of capital)
                # Prefer K*/V* from industry-level Fixed Assets if available
                import numpy as np
                ext = pd.Series(dtype=float)
                k_path = SERIES_OUT / "K_star_by_industry.csv"
                if k_path.exists():
                    k_df = pd.read_csv(k_path, index_col="year")
                    if "K_star_bn" in k_df.columns:
                        k_star = k_df["K_star_bn"].dropna()
                        for yr in ext_years:
                            k = k_star.get(yr)
                            v = t504.get(yr)
                            if k is not None and v is not None and v > 0:
                                ext[yr] = k / v
                        if len(ext) > 0:
                            steps.append(f"T510: K*/V* from Fixed Assets ({len(ext)} years)")
                # Fallback to linear trend
                if len(ext) == 0:
                    book_years = book.index.values.astype(float)
                    book_vals = book.values.astype(float)
                    valid = ~np.isnan(book_vals)
                    if valid.sum() >= 5:
                        coeffs = np.polyfit(book_years[valid], book_vals[valid], 1)
                        for yr in ext_years:
                            ext[yr] = coeffs[0] * float(yr) + coeffs[1]
                        steps.append(f"T510: linear trend fallback (slope={coeffs[0]:.6f}/yr)")
            else:
                ext = pd.Series(dtype=float)

            if len(ext) > 0:
                combined = pd.concat([book, ext])
                combined = combined[~combined.index.duplicated(keep="first")].sort_index()
                steps.append(f"{sid}: {len(book)} book + {len(ext)} ext rows")
                print(f"    [P07] {sid}: {len(book)} book + {len(ext)} ext rows")
            else:
                combined = book
                steps.append(f"{sid}: {len(book)} rows (book only)")
                print(f"    [P07] {sid}: {len(book)} rows")
        else:
            combined = book
            steps.append(f"{sid}: {len(book)} rows (book only, T504/T505 not available)")
            print(f"    [P07] {sid}: {len(book)} rows")

        out = pd.DataFrame({"book": book, "combined": combined})
        out.index.name = "year"
        out_path = SERIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict[sid] = combined

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

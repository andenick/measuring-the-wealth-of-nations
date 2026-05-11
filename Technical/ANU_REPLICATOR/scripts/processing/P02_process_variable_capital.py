#!/usr/bin/env python3
"""P02 - Process variable capital: T504 (V*).

V*_ext = W x (V*/W) using T512-COMBINED from P05.
Spliced at 1989 using level method.

Inputs:  parsed-raw/T504_parsed.csv (from L02)
         final-data/series/T512.csv (from P05 — must run first)
         api-data/BEA/nipa_6_2D_compensation_by_industry.csv
Outputs: final-data/series/T504.csv
Dependencies: L02, P05 (for T512)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from lib.paths import SERIES_OUT, API_DATA, ensure_dirs
from lib.data_io import load_parsed
from lib.api_data_io import load_bea_nipa

SERIES_ID = "T504"
SERIES_IDS = ["T504"]
PRIORITY = 2


def process():
    """Process V* with BEA compensation extension."""
    ensure_dirs()
    steps = []

    # Load book V* (1948-1989, billions)
    book_df, _ = load_parsed("T504")
    if book_df is None:
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": ["T504 parsed not found"], "data_dict": {}, "outputs": []}

    book = book_df["value"]
    steps.append(f"T504 book: {len(book)} rows, {book.index.min()}-{book.index.max()}")

    # Load T512 combined (V*/W ratio) from final-data
    t512_path = SERIES_OUT / "T512.csv"
    if not t512_path.exists():
        # Fallback: book only
        out = pd.DataFrame({"book": book, "combined": book})
        out.index.name = "year"
        out_path = SERIES_OUT / "T504.csv"
        out.to_csv(out_path)
        steps.append("T512 not available — book only")
        print(f"    [P02] T504: book only ({len(book)} rows), T512 missing")
        return {"series_id": SERIES_ID, "status": "warn",
                "steps": steps, "data_dict": {"T504": book},
                "outputs": [str(out_path)]}

    t512 = pd.read_csv(t512_path, index_col=0)["combined"]

    # Load BEA total compensation W (for extension period 1998+)
    bea_path = API_DATA / "BEA" / "nipa_6_2D_compensation_by_industry.csv"
    if bea_path.exists():
        w_df = load_bea_nipa(bea_path, line_filter="Compensation of employees")
        w = w_df.iloc[:, 0] / 1e9  # scaled_value is already in dollars, convert to billions
        steps.append(f"BEA compensation: {len(w)} rows")
    else:
        # No BEA data — use book only
        out = pd.DataFrame({"book": book, "combined": book})
        out.index.name = "year"
        out_path = SERIES_OUT / "T504.csv"
        out.to_csv(out_path)
        steps.append("BEA compensation not found — book only")
        print(f"    [P02] T504: book only, BEA data missing")
        return {"series_id": SERIES_ID, "status": "warn",
                "steps": steps, "data_dict": {"T504": book},
                "outputs": [str(out_path)]}

    # Compute V*_ext = W × (V*/W) for extension period
    ext_years = t512.index[t512.index > 1989]
    v_star_ext = pd.Series(dtype=float)
    for yr in ext_years:
        if yr in w.index and yr in t512.index:
            v_star_ext[yr] = w[yr] * t512[yr]

    # Splice: level method at 1989
    if len(v_star_ext) > 0 and 1989 in book.index:
        combined = pd.concat([book, v_star_ext])
        combined = combined[~combined.index.duplicated(keep="first")]
        combined = combined.sort_index()

        # Interpolate 1990-1997 gap using log-linear growth between 1989 and 1998
        if 1989 in combined.index and 1998 in combined.index:
            val_89 = combined[1989]
            val_98 = combined[1998]
            if val_89 > 0 and val_98 > 0:
                for yr in range(1990, 1998):
                    if yr not in combined.index or pd.isna(combined.get(yr)):
                        frac = (yr - 1989) / (1998 - 1989)
                        combined[yr] = val_89 * (val_98 / val_89) ** frac
                combined = combined.sort_index()
                n_interp = sum(1 for yr in range(1990, 1998) if yr in combined.index)
                steps.append(f"Interpolated {n_interp} gap years (1990-1997) via log-linear growth")
                print(f"    [P02] T504: interpolated {n_interp} gap years (1990-1997)")
    else:
        combined = book

    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    out_path = SERIES_OUT / "T504.csv"
    out.to_csv(out_path)

    n_ext = len(v_star_ext)
    steps.append(f"Extension: {n_ext} years via W×(V*/W)")
    print(f"    [P02] T504: {len(book)} book + {n_ext} ext rows")

    return {
        "series_id": SERIES_ID,
        "status": "ok",
        "steps": steps,
        "data_dict": {"T504": combined},
        "outputs": [str(out_path)],
    }

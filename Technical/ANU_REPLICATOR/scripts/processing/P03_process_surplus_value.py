#!/usr/bin/env python3
"""P03 - Process surplus value: T505 (S* = GFP - V*).

If T503 (GFP) is incomplete, derives S* from e x V* using T506 and T504.

Inputs:  parsed-raw/T505_parsed.csv (from L02)
         final-data/series/T503.csv (from P01)
         final-data/series/T504.csv (from P02)
         final-data/series/T506.csv (from P04, fallback)
Outputs: final-data/series/T505.csv
Dependencies: L02, P01 (T503), P02 (T504), P04 (T506 fallback)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from lib.paths import SERIES_OUT, ensure_dirs
from lib.data_io import load_parsed

SERIES_ID = "T505"
SERIES_IDS = ["T505"]
PRIORITY = 3


def process():
    """Process S* using GFP-V* or e×V* fallback."""
    ensure_dirs()
    steps = []

    # Load book S*
    book_df, _ = load_parsed("T505")
    if book_df is None:
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": ["T505 parsed not found"], "data_dict": {}, "outputs": []}

    book = book_df["value"]
    steps.append(f"T505 book: {len(book)} rows")

    # Try to extend using GFP - V*
    t503_path = SERIES_OUT / "T503.csv"
    t504_path = SERIES_OUT / "T504.csv"
    t506_path = SERIES_OUT / "T506.csv"

    ext = pd.Series(dtype=float)

    if t503_path.exists() and t504_path.exists():
        gfp = pd.read_csv(t503_path, index_col=0)["combined"].dropna()
        v_star = pd.read_csv(t504_path, index_col=0)["combined"].dropna()
        # S* = GFP - V* for extension years
        common = gfp.index.intersection(v_star.index)
        ext_years = common[common > 1989]
        if len(ext_years) > 0:
            ext = gfp[ext_years] - v_star[ext_years]
            steps.append(f"Extension via GFP-V*: {len(ext)} years")
    elif t506_path.exists() and t504_path.exists():
        # Fallback: S* = e × V*
        e = pd.read_csv(t506_path, index_col=0)["combined"].dropna()
        v_star = pd.read_csv(t504_path, index_col=0)["combined"].dropna()
        common = e.index.intersection(v_star.index)
        ext_years = common[common > 1989]
        if len(ext_years) > 0:
            ext = e[ext_years] * v_star[ext_years]
            steps.append(f"Extension via e×V*: {len(ext)} years")

    # Combine
    if len(ext) > 0:
        combined = pd.concat([book, ext])
        combined = combined[~combined.index.duplicated(keep="first")].sort_index()
    else:
        combined = book
        steps.append("No extension data available")

    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    out_path = SERIES_OUT / "T505.csv"
    out.to_csv(out_path)

    n_ext = max(0, len(combined) - len(book))
    print(f"    [P03] T505: {len(book)} book + {n_ext} ext rows")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if len(combined) > 0 else "fail",
        "steps": steps,
        "data_dict": {"T505": combined},
        "outputs": [str(out_path)],
    }

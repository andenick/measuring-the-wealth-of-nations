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
from lib.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from lib.data_io import load_parsed

SERIES_ID = "T513"
SERIES_IDS = ["T513", "T514"]
PRIORITY = 4


def process():
    """Process profit rates using book + pre-extended data."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    for sid in SERIES_IDS:
        # Load book
        book_df, _ = load_parsed(sid)
        book = book_df["value"] if book_df is not None else pd.Series(dtype=float)

        # Load extended
        ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
        if ext_path.exists():
            ext_df = pd.read_csv(ext_path, index_col=0)
            ext_df.index = ext_df.index.astype(int)
            ext = ext_df["value"]
        else:
            ext = pd.Series(dtype=float)

        # Combined: extended where available, else book
        combined = ext if len(ext) > 0 else book
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

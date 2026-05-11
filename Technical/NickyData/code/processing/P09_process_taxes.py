#!/usr/bin/env python3
"""P09 - Process tax allocation: T601-T604.

Book data (1952-1989) + NIPA extension (1990-2025) via growth-rate splice.

Inputs:  parsed-raw/T601_parsed.csv .. T604_parsed.csv (book, from L07)
         parsed-raw/T601_ext_parsed.csv .. T604_ext_parsed.csv (extension, from L07)
Outputs: final-data/series/T601.csv .. T604.csv
Dependencies: L07. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T601"
SERIES_IDS = ["T601", "T602", "T603", "T604"]
PRIORITY = 1


def process():
    """Process tax accounts with NIPA extension."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    for sid in SERIES_IDS:
        df, path = load_parsed(sid)
        if df is None:
            steps.append(f"{sid}: parsed file not found at {path}")
            continue

        book = df["value"]

        # Try to load extension
        ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
        if ext_path.exists():
            ext_df = pd.read_csv(ext_path, index_col=0)
            ext = ext_df["value"].dropna()
            combined = pd.concat([book, ext])
            combined = combined[~combined.index.duplicated(keep="first")].sort_index()
            n_ext = len(combined) - len(book)
            steps.append(f"{sid}: {len(book)} book + {n_ext} ext rows")
            print(f"    [P09] {sid}: {len(combined)} rows ({len(book)} book + {n_ext} ext)")
        else:
            combined = book
            steps.append(f"{sid}: {len(book)} rows (book only)")
            print(f"    [P09] {sid}: {len(book)} rows")

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

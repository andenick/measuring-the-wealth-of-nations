#!/usr/bin/env python3
"""P09 - Process tax allocation: T601-T604.

Book-only passthrough (1952-1989, already in billions from L07).

Inputs:  parsed-raw/T601_parsed.csv .. T604_parsed.csv (from L07)
Outputs: final-data/series/T601.csv .. T604.csv
Dependencies: L07. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from lib.paths import SERIES_OUT, ensure_dirs
from lib.data_io import load_parsed

SERIES_ID = "T601"
SERIES_IDS = ["T601", "T602", "T603", "T604"]
PRIORITY = 1


def process():
    """Process tax accounts — book data only."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    for sid in SERIES_IDS:
        df, path = load_parsed(sid)
        if df is None:
            steps.append(f"{sid}: parsed file not found at {path}")
            continue

        out = pd.DataFrame({"book": df["value"], "combined": df["value"]})
        out.index.name = "year"
        out_path = SERIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict[sid] = df["value"]
        steps.append(f"{sid}: {len(df)} rows (book only)")
        print(f"    [P09] {sid}: {len(df)} rows")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

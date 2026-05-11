#!/usr/bin/env python3
"""L02 - Load Variable Capital & Surplus Value: T504, T505.

Primary source: book_tableH1_1948_1989.csv (digitized from book PDF, DEC-020).
Column map: T504 <- V_star (billions), T505 <- S_star (billions)

Outputs: parsed-raw/T504_parsed.csv, T505_parsed.csv
Dependencies: None (reads digitized H.1 data directly)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import PARSED_RAW, SERIES_OUT, ensure_dirs

SERIES_IDS = ["T504", "T505"]

H1_COL_MAP = {
    "T504": "V_star",
    "T505": "S_star",
}


def load():
    """Load V* and S* from digitized Table H.1 (billions)."""
    ensure_dirs()
    outputs = []

    h1_path = SERIES_OUT / "book_tableH1_1948_1989.csv"
    if not h1_path.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Table H.1 not found: {h1_path}", "outputs": []}

    df = pd.read_csv(h1_path, comment="#", index_col="year")

    for sid, col in H1_COL_MAP.items():
        if col not in df.columns:
            print(f"    [L02] {sid}: column {col} not found in Table H.1")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L02] {sid}: {len(out)} rows (Table H.1, billions)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"V*/S* from Table H.1 | {len(outputs)} series, 1948-1989",
        "outputs": outputs,
    }

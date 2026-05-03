#!/usr/bin/env python3
"""L04 - Load Employment: T515, T516.

Input:   ch05/Employment_1948_1989.csv (Format A, 1948-1989)
Column map: T515←T515 (thousands), T516←T516 (thousands)
Outputs: parsed-raw/T515_parsed.csv, T516_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T515", "T516"]


def load():
    """Load employment data (productive Lp and unproductive Lu)."""
    ensure_dirs()

    source = ST_CHOPPED / "ch05" / "Employment_1948_1989.csv"
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source, columns=["T515", "T516"])
    outputs = []

    for sid in SERIES_IDS:
        if sid not in df.columns:
            print(f"    [L04] {sid}: column not found")
            continue
        out = df[[sid]].rename(columns={sid: "value"}).dropna()
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L04] {sid}: {len(out)} rows (thousands)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Employment | {len(outputs)} series, 1948-1989",
        "outputs": outputs,
    }

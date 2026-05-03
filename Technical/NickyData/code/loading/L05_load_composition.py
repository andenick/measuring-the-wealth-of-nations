#!/usr/bin/env python3
"""L05 - Load Composition: T507, T510.

Input:   ch05/ExploitationComposition_1948_1989.csv (Format A, 1948-1989)
Column map: T507←T509_surplus_ratio, T510←T510_value_composition
Outputs: parsed-raw/T507_parsed.csv, T510_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T507", "T510"]

COLUMN_MAP = {
    "T507": "T509_surplus_ratio",
    "T510": "T510_value_composition",
}


def load():
    """Load exploitation composition ratios."""
    ensure_dirs()

    source = ST_CHOPPED / "ch05" / "ExploitationComposition_1948_1989.csv"
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source, columns=list(COLUMN_MAP.values()))
    outputs = []

    for sid, col in COLUMN_MAP.items():
        if col not in df.columns:
            print(f"    [L05] {sid}: column {col} not found")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L05] {sid}: {len(out)} rows from {col}")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Composition ratios | {len(outputs)} series, 1948-1989",
        "outputs": outputs,
    }

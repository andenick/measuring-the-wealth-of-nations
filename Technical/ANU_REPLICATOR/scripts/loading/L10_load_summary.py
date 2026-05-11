#!/usr/bin/env python3
"""L10 - Load Summary Indicators: T901.

Input:   ch09/Table9_1_SummaryIndicators.csv (Format B, 1948-1989)
Loads all columns as-is (already in correct units as ratios).
Outputs: parsed-raw/T901_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from lib.data_io import load_chopped_direct

SERIES_IDS = ["T901"]


def load():
    """Load summary indicators table."""
    ensure_dirs()

    source = ST_CHOPPED / "ch09" / "Table9_1_SummaryIndicators.csv"
    if not source.exists():
        return {"series_id": "T901", "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source)
    out_path = PARSED_RAW / "T901_parsed.csv"
    df.to_csv(out_path)
    print(f"    [L10] T901: {len(df)} rows, {len(df.columns)} columns")

    return {
        "series_id": "T901",
        "status": "ok",
        "message": f"Summary indicators | {len(df)} rows, {len(df.columns)} cols",
        "outputs": [str(out_path)],
    }

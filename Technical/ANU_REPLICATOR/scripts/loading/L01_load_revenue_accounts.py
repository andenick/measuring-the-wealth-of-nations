#!/usr/bin/env python3
"""L01 - Load Revenue Accounts: T501, T502, T503, T508, T509.

Input:  ch05/TableE2_RevenueAccounts.csv (Format A, 1948-1961)
Column map: T501←TP_star, T502←C_star_m, T503←GFP, T508←CON_star, T509←IG_star
Outputs: parsed-raw/T501_parsed.csv .. T509_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from lib.data_io import load_chopped_direct

SERIES_IDS = ["T501", "T502", "T503", "T508", "T509"]

COLUMN_MAP = {
    "T501": "TP_star",
    "T502": "C_star_m",
    "T503": "GFP",
    "T508": "CON_star",
    "T509": "IG_star",
}


def load():
    """Load revenue accounts from TableE2 chopped file."""
    ensure_dirs()

    source = ST_CHOPPED / "ch05" / "TableE2_RevenueAccounts.csv"
    if not source.exists():
        return {
            "series_id": SERIES_IDS[0],
            "status": "fail",
            "message": f"Source not found: {source}",
            "outputs": [],
        }

    df = load_chopped_direct(source, columns=list(COLUMN_MAP.values()))
    outputs = []

    for sid, col in COLUMN_MAP.items():
        if col not in df.columns:
            print(f"    [L01] {sid}: column {col} not found")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L01] {sid}: {len(out)} rows from {col} (1948-1961)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Revenue accounts | {len(outputs)} series, 1948-1961 only",
        "outputs": outputs,
    }

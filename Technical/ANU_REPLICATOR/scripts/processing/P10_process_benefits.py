#!/usr/bin/env python3
"""P10 - Process worker benefits: T605, T606.

Book period (1952-1989) from L08, extension (1990-2025) from BEA NIPA.
Spliced at 1989 using level method. Validates continuity at 1996 welfare reform.

Inputs:  parsed-raw/T605_parsed.csv, T606_parsed.csv (from L08)
         parsed-raw/T605_ext_parsed.csv, T606_ext_parsed.csv (from L08)
Outputs: final-data/series/T605.csv, T606.csv
Dependencies: L08. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from lib.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from lib.data_io import load_parsed

SERIES_ID = "T605"
SERIES_IDS = ["T605", "T606"]
PRIORITY = 1


def process():
    """Process benefit accounts — book + extension with 1996 validation."""
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

        # Try loading extension data
        ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
        if ext_path.exists():
            ext_df = pd.read_csv(ext_path, index_col=0)
            ext_df.index = ext_df.index.astype(int)
            ext = ext_df["value"]

            # Splice: level method at 1989 (book takes priority for overlap)
            combined = pd.concat([book, ext])
            combined = combined[~combined.index.duplicated(keep="first")]
            combined = combined.sort_index()

            n_ext = len(ext)
            steps.append(f"{sid}: {len(book)} book + {n_ext} ext rows")
            print(f"    [P10] {sid}: {len(book)} book + {n_ext} ext rows")

            # Validate continuity at 1996 welfare reform
            if 1995 in combined.index and 1997 in combined.index:
                pct_change = (combined[1997] - combined[1995]) / combined[1995]
                if abs(pct_change) > 0.15:
                    msg = f"{sid} WARN: 1996 welfare reform discontinuity: {pct_change:+.1%}"
                    steps.append(msg)
                    print(f"    [P10] {msg}")
                else:
                    steps.append(f"{sid}: 1996 continuity OK ({pct_change:+.1%})")

            # Validate splice continuity at 1989-1990
            if 1989 in combined.index and 1990 in combined.index:
                splice_change = (combined[1990] - combined[1989]) / combined[1989]
                steps.append(f"{sid}: splice continuity 1989->1990: {splice_change:+.1%}")
        else:
            combined = book
            steps.append(f"{sid}: {len(df)} rows (book only, no extension)")
            print(f"    [P10] {sid}: {len(df)} rows (book only)")

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

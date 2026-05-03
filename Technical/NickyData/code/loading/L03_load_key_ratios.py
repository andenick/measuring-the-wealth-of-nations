#!/usr/bin/env python3
"""L03 - Load Key Ratios: T506, T511, T512.

Inputs:
  - ch05/Table5_7_KeyRatios.csv (Format A, 1948-1989) — book values
  - ch05/Table5_7_Extended.csv (Format A, 1948-2024) — pre-spliced COMBINED
Outputs: parsed-raw/T506_parsed.csv, T511_parsed.csv, T512_parsed.csv,
         plus *_ext_parsed.csv for extended series
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T506", "T511", "T512"]

# Book columns (Format A: first column is empty = year index)
BOOK_COLS = {"T506": "T506A", "T511": "T511A", "T512": "T512A"}
# Extended columns
EXT_COLS = {"T506": "T506_COMBINED", "T511": "T511_COMBINED", "T512": "T512_COMBINED"}


def load():
    """Load key ratios from book and extended chopped files."""
    ensure_dirs()
    outputs = []

    # Book data
    book_src = ST_CHOPPED / "ch05" / "Table5_7_KeyRatios.csv"
    if not book_src.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {book_src}", "outputs": []}

    book_df = load_chopped_direct(book_src)
    for sid, col in BOOK_COLS.items():
        if col not in book_df.columns:
            print(f"    [L03] {sid}: column {col} not found in book")
            continue
        out = book_df[[col]].rename(columns={col: "value"}).dropna()
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L03] {sid}: {len(out)} book rows from {col}")

    # Extended data (pre-spliced)
    ext_src = ST_CHOPPED / "ch05" / "Table5_7_Extended.csv"
    if ext_src.exists():
        ext_df = load_chopped_direct(ext_src)
        for sid, col in EXT_COLS.items():
            if col not in ext_df.columns:
                print(f"    [L03] {sid}: extended column {col} not found")
                continue
            out = ext_df[[col]].rename(columns={col: "value"}).dropna()
            out_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            print(f"    [L03] {sid}: {len(out)} extended rows from {col}")
    else:
        print("    [L03] Extended file not found, book-only")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Key ratios | {len(outputs)} files, book + extended",
        "outputs": outputs,
    }

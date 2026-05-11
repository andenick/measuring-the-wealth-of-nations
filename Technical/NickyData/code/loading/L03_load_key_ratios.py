#!/usr/bin/env python3
"""L03 - Load Key Ratios: T506, T511, T512.

T506 (S*/V*): Prefer actual annual data from digitized Table H.1 (Step 1, DEC-020).
  Falls back to interpolated Table5_7_KeyRatios.csv if H.1 not available.
T511 (Lp/L), T512 (V*/W): From Table5_7_KeyRatios.csv (book) + Extended.csv (extension).

Inputs:
  - book_tableH1_1948_1989.csv (actual annual data, 42 years)
  - ch05/Table5_7_KeyRatios.csv (Format A, 1948-1989)
  - ch05/Table5_7_Extended.csv (Format A, 1948-2024) — pre-spliced COMBINED
Outputs: parsed-raw/T506_parsed.csv, T511_parsed.csv, T512_parsed.csv
Dependencies: L02b (Table H.1 digitization)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import ST_CHOPPED, PARSED_RAW, SERIES_OUT, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T506", "T511", "T512"]

BOOK_COLS = {"T506": "T506A", "T511": "T511A", "T512": "T512A"}
EXT_COLS = {"T506": "T506_COMBINED", "T511": "T511_COMBINED", "T512": "T512_COMBINED"}


def load():
    """Load key ratios. T506 from Table H.1 if available, else Table 5.7."""
    ensure_dirs()
    outputs = []

    # T506: prefer actual annual S*/V* from digitized Table H.1
    h1_path = SERIES_OUT / "book_tableH1_1948_1989.csv"
    if h1_path.exists():
        h1 = pd.read_csv(h1_path, comment="#", index_col="year")
        if "S_star_V_star" in h1.columns:
            out = h1[["S_star_V_star"]].rename(columns={"S_star_V_star": "value"}).dropna()
            out_path = PARSED_RAW / "T506_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            print(f"    [L03] T506: {len(out)} rows from Table H.1 (actual annual S*/V*)")
            t506_from_h1 = True
        else:
            t506_from_h1 = False
    else:
        t506_from_h1 = False

    # Book data for T511, T512 (and T506 fallback)
    book_src = ST_CHOPPED / "ch05" / "Table5_7_KeyRatios.csv"
    if not book_src.exists():
        if not t506_from_h1:
            return {"series_id": SERIES_IDS[0], "status": "fail",
                    "message": f"Source not found: {book_src}", "outputs": outputs}
    else:
        book_df = load_chopped_direct(book_src)
        for sid, col in BOOK_COLS.items():
            if sid == "T506" and t506_from_h1:
                continue
            if col not in book_df.columns:
                print(f"    [L03] {sid}: column {col} not found in book")
                continue
            out = book_df[[col]].rename(columns={col: "value"}).dropna()
            out_path = PARSED_RAW / f"{sid}_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            print(f"    [L03] {sid}: {len(out)} book rows from {col}")

    # NOTE: Table5_7_Extended.csv is DEPRECATED (Session 23, DEC-019).
    # T506 extended by P04 from S*/V* components.
    # T511 extended by P05 from IO productive ratio.
    # T512 extended by P05 from V*/W components.

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Key ratios | {len(outputs)} files, book + extended",
        "outputs": outputs,
    }

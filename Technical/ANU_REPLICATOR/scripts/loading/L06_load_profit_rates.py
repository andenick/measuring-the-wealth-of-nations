#!/usr/bin/env python3
"""L06 - Load Profit Rates: T513, T514.

Inputs:
  - ch05/ProfitRates_1948_1989.csv (Format B, 1948-1989) — book values
  - ch05/ProfitRates_Extended.csv (Format B, 1948-2024) — pre-extended
Column map: T513←T513_r_star_pct (÷100), T514←T514_r_star_adj_pct (÷100)
Outputs: parsed-raw/T513_parsed.csv, T514_parsed.csv, *_ext_parsed.csv,
         plus T513_capacity_utilization_parsed.csv etc. (cross-validation)
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from lib.data_io import load_chopped_direct

SERIES_IDS = ["T513", "T514"]

COLUMN_MAP = {
    "T513": "T513_r_star_pct",
    "T514": "T514_r_star_adj_pct",
}


def load():
    """Load profit rates, converting percentage to ratio (÷100)."""
    ensure_dirs()
    outputs = []

    # Book data
    book_src = ST_CHOPPED / "ch05" / "ProfitRates_1948_1989.csv"
    if not book_src.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {book_src}", "outputs": []}

    book_df = load_chopped_direct(book_src)
    for sid, col in COLUMN_MAP.items():
        if col not in book_df.columns:
            print(f"    [L06] {sid}: column {col} not found in book")
            continue
        out = book_df[[col]].rename(columns={col: "value"}).dropna()
        out["value"] = out["value"] / 100.0  # pct → ratio
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L06] {sid}: {len(out)} book rows (÷100 → ratio)")

    # Also save cross-validation columns from book
    for extra_col in ["capacity_utilization", "S_star_bn", "K_bn"]:
        if extra_col in book_df.columns:
            out = book_df[[extra_col]].rename(columns={extra_col: "value"}).dropna()
            out_path = PARSED_RAW / f"T513_{extra_col}_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))

    # Extended data (pre-computed)
    ext_src = ST_CHOPPED / "ch05" / "ProfitRates_Extended.csv"
    if ext_src.exists():
        ext_df = load_chopped_direct(ext_src)
        for sid, col in COLUMN_MAP.items():
            if col not in ext_df.columns:
                continue
            out = ext_df[[col]].rename(columns={col: "value"}).dropna()
            out["value"] = out["value"] / 100.0
            out_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            print(f"    [L06] {sid}: {len(out)} extended rows")
    else:
        print("    [L06] Extended file not found, book-only")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Profit rates | {len(outputs)} files",
        "outputs": outputs,
    }

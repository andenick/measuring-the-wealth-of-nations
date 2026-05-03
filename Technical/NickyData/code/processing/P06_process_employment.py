#!/usr/bin/env python3
"""P06 - Process employment: T515 (Lp), T516 (Lu).

Book data 1948-1989. Extension via BLS CES production workers.

Inputs:  parsed-raw/T515_parsed.csv, T516_parsed.csv (from L04)
         api-data/BLS/bls_ces_production_workers.csv
Outputs: final-data/series/T515.csv, T516.csv
Dependencies: L04. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, API_DATA, ensure_dirs
from utils.data_io import load_parsed
from utils.api_data_io import load_bls_csv

SERIES_ID = "T515"
SERIES_IDS = ["T515", "T516"]
PRIORITY = 1


def process():
    """Process employment levels with BLS extension."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    # Load book data
    lp_df, _ = load_parsed("T515")
    lu_df, _ = load_parsed("T516")

    if lp_df is None or lu_df is None:
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": ["Parsed employment data not found"], "data_dict": {}, "outputs": []}

    lp_book = lp_df["value"]
    lu_book = lu_df["value"]

    # Try BLS extension
    bls_path = API_DATA / "BLS" / "bls_ces_production_workers.csv"
    lp_ext = pd.Series(dtype=float)
    lu_ext = pd.Series(dtype=float)

    if bls_path.exists():
        bls = load_bls_csv(bls_path)
        # CES0500000006 = total private production workers
        # CES0500000001 = total private all employees
        if "CES0500000006" in bls.columns and "CES0500000001" in bls.columns:
            prod = bls["CES0500000006"].dropna()
            total = bls["CES0500000001"].dropna()

            # Scale to match book levels at 1989
            ext_years = prod.index[prod.index > 1989]
            if 1989 in lp_book.index and 1989 in prod.index:
                scale = lp_book[1989] / prod[1989]
                lp_ext = prod[ext_years] * scale

                # Lu = total - Lp (scaled similarly)
                total_scale = (lp_book[1989] + lu_book[1989]) / total[1989]
                total_scaled = total[ext_years] * total_scale
                lu_ext = total_scaled - lp_ext
                steps.append(f"BLS extension: {len(ext_years)} years")

    # Write T515 (Lp)
    lp_combined = pd.concat([lp_book, lp_ext])
    lp_combined = lp_combined[~lp_combined.index.duplicated(keep="first")].sort_index()
    out = pd.DataFrame({"book": lp_book, "combined": lp_combined})
    out.index.name = "year"
    out_path = SERIES_OUT / "T515.csv"
    out.to_csv(out_path)
    outputs.append(str(out_path))
    data_dict["T515"] = lp_combined

    # Write T516 (Lu)
    lu_combined = pd.concat([lu_book, lu_ext])
    lu_combined = lu_combined[~lu_combined.index.duplicated(keep="first")].sort_index()
    out = pd.DataFrame({"book": lu_book, "combined": lu_combined})
    out.index.name = "year"
    out_path = SERIES_OUT / "T516.csv"
    out.to_csv(out_path)
    outputs.append(str(out_path))
    data_dict["T516"] = lu_combined

    n_book = len(lp_book)
    n_ext = max(0, len(lp_combined) - n_book)
    steps.append(f"T515/T516: {n_book} book + {n_ext} ext rows")
    print(f"    [P06] T515/T516: {n_book} book + {n_ext} ext rows")

    return {
        "series_id": SERIES_ID,
        "status": "ok",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

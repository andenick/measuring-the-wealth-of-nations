#!/usr/bin/env python3
"""P06 - Process employment: T515 (Lp), T516 (Lu).

Book data 1948-1989. Extension via BLS CES production workers.
Total employment from FRED PAYEMS (total nonfarm, includes govt) preferred
over CES0500000001 (total private) per KB Appendix F finding (DEC-019).

Inputs:  parsed-raw/T515_parsed.csv, T516_parsed.csv (from L04)
         parsed-raw/total_nonfarm_employment.csv (from L04b, FRED PAYEMS)
         api-data/BLS/bls_ces_production_workers.csv
Outputs: final-data/series/T515.csv, T516.csv
Dependencies: L04, L04b. No upstream P## dependencies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, API_DATA, PARSED_RAW, ensure_dirs
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

    # Load FRED employment data
    payems_path = PARSED_RAW / "total_nonfarm_employment.csv"
    sector_path = PARSED_RAW / "sector_employment.csv"
    total_nonfarm = None
    sector_emp = None

    if payems_path.exists():
        tnf = pd.read_csv(payems_path, index_col="year")
        total_nonfarm = tnf["value"].dropna()
        steps.append(f"FRED PAYEMS: {len(total_nonfarm)} years")

    if sector_path.exists():
        sector_emp = pd.read_csv(sector_path, index_col="year")
        steps.append(f"Sector employment: {len(sector_emp)} years, cols={list(sector_emp.columns)}")

    if bls_path.exists():
        bls = load_bls_csv(bls_path)
        if "CES0500000006" in bls.columns:
            prod = bls["CES0500000006"].dropna()

            # Total employment: use PAYEMS (includes govt, matches book's L)
            if total_nonfarm is not None:
                total = total_nonfarm
                total_source = "PAYEMS (total nonfarm)"
            elif "CES0500000001" in bls.columns:
                total = bls["CES0500000001"].dropna()
                total_source = "CES0500000001 (total private)"
            else:
                total = None
                total_source = "none"

            if total is not None:
                ext_years = prod.index[prod.index > 1989]
                if 1989 in lp_book.index and 1989 in prod.index:
                    scale = lp_book[1989] / prod[1989]
                    lp_ext = prod[ext_years] * scale

                    book_total_1989 = lp_book[1989] + lu_book[1989]
                    total_1989 = total.get(1989, None)
                    if total_1989 is None and len(total[total.index >= 1989]) > 0:
                        total_1989 = total[total.index >= 1989].iloc[0]
                    if total_1989 is not None and total_1989 > 0:
                        total_scale = book_total_1989 / total_1989
                        common_ext = ext_years.intersection(total.index)
                        total_scaled = total[common_ext] * total_scale
                        lu_ext = total_scaled - lp_ext.reindex(common_ext).fillna(0)
                        steps.append(f"Extension via {total_source}: {len(common_ext)} years, total_scale={total_scale:.3f}")
                        print(f"    [P06] total_scale={total_scale:.3f} ({total_source})")

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

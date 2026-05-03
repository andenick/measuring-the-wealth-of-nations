#!/usr/bin/env python3
"""P12 - Process summary assembly: T901.

Assembles combined summary table from all upstream final series
(T506, T511-T514, T608).

Inputs:  final-data/series/T506.csv, T511.csv, T512.csv, T513.csv, T514.csv, T608.csv
         parsed-raw/T901_parsed.csv (from L10, for reference)
Outputs: final-data/series/T901.csv
Dependencies: L10, P04 (T506), P05 (T511/T512), P08 (T513/T514), P11 (T608)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T901"
SERIES_IDS = ["T901"]
PRIORITY = 5

# Series to assemble into summary
COMPONENT_SERIES = {
    "T506_exploitation_rate": "T506",
    "T511_productive_labor_share": "T511",
    "T512_productive_wage_share": "T512",
    "T513_marxian_profit_rate": "T513",
    "T514_capacity_adj_profit_rate": "T514",
    "T608_nsw_v_star": "T608",
}


def process():
    """Assemble T901 summary from upstream series."""
    ensure_dirs()
    steps = []

    # Load book T901 for reference
    book_df, _ = load_parsed("T901")
    book_years = set()
    if book_df is not None:
        book_years = set(book_df.index)
        steps.append(f"T901 book: {len(book_df)} rows")

    # Load each component from final-data
    assembled = {}
    for col_name, sid in COMPONENT_SERIES.items():
        path = SERIES_OUT / f"{sid}.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            if "combined" in df.columns:
                assembled[col_name] = df["combined"]
                steps.append(f"{col_name}: {df['combined'].notna().sum()} rows from {sid}")
            else:
                steps.append(f"{col_name}: no 'combined' column in {sid}")
        else:
            steps.append(f"{col_name}: {sid}.csv not found")

    if not assembled:
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": steps, "data_dict": {}, "outputs": []}

    summary = pd.DataFrame(assembled)
    summary.index.name = "year"
    summary = summary.sort_index()

    out_path = SERIES_OUT / "T901.csv"
    summary.to_csv(out_path)

    print(f"    [P12] T901: {len(summary)} rows, {len(assembled)} columns assembled")
    steps.append(f"Summary: {len(summary)} rows, {len(assembled)}/{len(COMPONENT_SERIES)} columns")

    # Return first column as representative Series for Shiny export
    first_col = summary.iloc[:, 0] if len(summary.columns) > 0 else pd.Series(dtype=float)

    return {
        "series_id": SERIES_ID,
        "status": "ok",
        "steps": steps,
        "data_dict": {"T901": first_col},
        "outputs": [str(out_path)],
    }

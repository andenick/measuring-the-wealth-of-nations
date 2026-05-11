#!/usr/bin/env python3
"""P03 - Process surplus value: T505 (S* = GFP* - Dp - V*).

S* = VA* - V* where VA* = GFP* - Dp (net value added of productive sectors).
Dp = depreciation of productive fixed capital.

Sources for Dp:
- 1948-1989: Book Table H.1 "Dp" column
- 1990-2024: FRED COFC × productive output ratio (from integrated TP series)

If T503 (GFP) is incomplete, derives S* from e x V* using T506 and T504.

Inputs:  parsed-raw/T505_parsed.csv (from L02)
         final-data/series/T503.csv (from P01)
         final-data/series/T504.csv (from P02)
         final-data/series/T506.csv (from P04, fallback)
         final-data/book/series/book_tableH1_1948_1989.csv (for Dp)
         raw-data/parsed/integrated_tp_series.csv (for productive share)
Outputs: final-data/series/T505.csv
Dependencies: L02, P01 (T503), P02 (T504), L19 (integrated TP)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T505"
SERIES_IDS = ["T505"]
PRIORITY = 3

BOOK_DATA = Path(__file__).resolve().parent.parent.parent / "data" / "final-data" / "book" / "series"


def _load_depreciation() -> pd.Series:
    """Load Dp: book values (1948-1989) + COFC × productive ratio (1990-2024)."""
    dp = pd.Series(dtype=float)

    # Book Dp
    h1_path = BOOK_DATA / "book_tableH1_1948_1989.csv"
    if h1_path.exists():
        h1 = pd.read_csv(h1_path, comment="#").set_index("year")
        if "Dp" in h1.columns:
            dp = h1["Dp"].copy()

    # Extension: COFC × productive share
    # Load FRED COFC from cached API data
    api_data = Path(__file__).resolve().parent.parent.parent.parent / "Inputs" / "API_Data"
    cofc = pd.Series(dtype=float)
    fred_path = api_data / "FRED" / "fred_tcu_capacity_utilization.csv"
    # COFC comes from FRED fetch in nickydata — check parsed raw
    integ_path = PARSED_RAW / "integrated_tp_series.csv"
    if integ_path.exists():
        integ = pd.read_csv(integ_path, index_col="year")
        prod_share = integ.get("productive_go_share", pd.Series(dtype=float))

        # Use book-implied ratio for transition
        if not dp.empty:
            dp_1989 = dp.get(1989, dp.iloc[-1])
            # We need COFC — approximate from book: Dp(1989)/0.75 ≈ total depreciation
            # For now, extend Dp using GFP growth rate as proxy
            if "gfp_star" in integ.columns:
                gfp = integ["gfp_star"].dropna()
                gfp_1989 = gfp.get(1989, gfp.iloc[0])
                for yr in range(1990, 2025):
                    if yr in gfp.index and gfp_1989 > 0:
                        dp[yr] = dp_1989 * (gfp[yr] / gfp_1989)

    return dp


def process():
    """Process S* = GFP* - Dp - V*."""
    ensure_dirs()
    steps = []

    # Load book S*
    book_df, _ = load_parsed("T505")
    if book_df is None:
        return {"series_id": SERIES_ID, "status": "fail",
                "steps": ["T505 parsed not found"], "data_dict": {}, "outputs": []}

    book = book_df["value"]
    steps.append(f"T505 book: {len(book)} rows")

    # Load depreciation
    dp = _load_depreciation()
    if not dp.empty:
        steps.append(f"Depreciation: {len(dp)} years ({int(dp.index.min())}-{int(dp.index.max())})")

    # Try to extend using GFP* - Dp - V*
    t503_path = SERIES_OUT / "T503.csv"
    t504_path = SERIES_OUT / "T504.csv"
    t506_path = SERIES_OUT / "T506.csv"

    ext = pd.Series(dtype=float)

    if t503_path.exists() and t504_path.exists():
        gfp = pd.read_csv(t503_path, index_col=0)["combined"].dropna()
        v_star = pd.read_csv(t504_path, index_col=0)["combined"].dropna()
        common = gfp.index.intersection(v_star.index)
        ext_years = common[common > 1989]
        if len(ext_years) > 0:
            for yr in ext_years:
                dp_yr = dp.get(yr, 0)
                ext[yr] = gfp[yr] - dp_yr - v_star[yr]
            steps.append(f"Extension via GFP*-Dp-V*: {len(ext)} years")
    elif t506_path.exists() and t504_path.exists():
        e = pd.read_csv(t506_path, index_col=0)["combined"].dropna()
        v_star = pd.read_csv(t504_path, index_col=0)["combined"].dropna()
        common = e.index.intersection(v_star.index)
        ext_years = common[common > 1989]
        if len(ext_years) > 0:
            ext = e[ext_years] * v_star[ext_years]
            steps.append(f"Extension via e×V* (fallback): {len(ext)} years")

    # Combine
    if len(ext) > 0:
        combined = pd.concat([book, ext])
        combined = combined[~combined.index.duplicated(keep="first")].sort_index()
    else:
        combined = book
        steps.append("No extension data available")

    out = pd.DataFrame({"book": book, "combined": combined})
    out.index.name = "year"
    out_path = SERIES_OUT / "T505.csv"
    out.to_csv(out_path)

    n_ext = max(0, len(combined) - len(book))
    print(f"    [P03] T505: {len(book)} book + {n_ext} ext rows")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if len(combined) > 0 else "fail",
        "steps": steps,
        "data_dict": {"T505": combined},
        "outputs": [str(out_path)],
    }

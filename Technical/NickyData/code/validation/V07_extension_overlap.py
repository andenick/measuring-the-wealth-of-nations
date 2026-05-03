#!/usr/bin/env python3
"""V07 - Extension Overlap: verify correlation between book and API data in overlap period.

For each extended series, checks the overlap window around the splice year to ensure
the book-period data and extension data are correlated and consistent.

Inputs:
  - data/final-data/series/*.csv (must have book-period and extension subseries columns)
  - Technical/EXTENSION_LOG.json
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import SERIES_OUT, TECHNICAL

VALIDATOR_NAME = "V07_extension_overlap"

# Minimum number of overlap years required for meaningful correlation
MIN_OVERLAP_YEARS = 3
# Minimum acceptable correlation in overlap period
MIN_CORRELATION = 0.90


def _load_extension_log():
    ext_path = TECHNICAL / "EXTENSION_LOG.json"
    if not ext_path.exists():
        return []
    with open(ext_path, encoding="utf-8") as f:
        data = json.load(f)
    # Handle both formats: flat array or {"extensions": [...]}
    return data if isinstance(data, list) else data.get("extensions", [])


def validate(series_filter=None, chapter_filter=None):
    extensions = _load_extension_log()
    checks = []

    for ext in extensions:
        series_id = ext.get("series_id", "")
        splice_year = ext.get("splice_year")
        if not series_id or not splice_year:
            continue

        if series_filter and series_id not in series_filter:
            continue

        splice_year = int(splice_year)
        csv_path = SERIES_OUT / f"{series_id}.csv"
        if not csv_path.exists():
            checks.append({
                "series": series_id,
                "status": "SKIP",
                "message": f"File not found",
            })
            continue

        df = pd.read_csv(csv_path)
        if "year" not in df.columns:
            df = df.rename(columns={df.columns[0]: "year"})

        # Look for book-period column and extension data
        book_col = None
        ext_col = None
        for col in df.columns:
            col_upper = col.upper()
            if "EXT" in col_upper and series_id.upper() in col_upper:
                ext_col = col
            elif col_upper.endswith("-A") or col_upper.endswith("_A"):
                book_col = col
            elif col_upper == "BOOK":
                book_col = col
            elif col_upper == "EXT":
                ext_col = col

        # If no explicit ext column, check if combined extends beyond book
        if ext_col is None and book_col and "combined" in df.columns:
            book_data = df[book_col].dropna()
            comb_data = df["combined"].dropna()
            if len(comb_data) > len(book_data):
                ext_col = "combined"  # combined IS the extension

        if book_col is None or ext_col is None:
            checks.append({
                "series": series_id,
                "splice_year": splice_year,
                "status": "SKIP",
                "message": f"{series_id}: cannot identify separate book/extension columns",
            })
            continue

        # Find overlap period (years where both have data)
        overlap = df[[
            "year", book_col, ext_col
        ]].dropna(subset=[book_col, ext_col])

        if len(overlap) < MIN_OVERLAP_YEARS:
            checks.append({
                "series": series_id,
                "splice_year": splice_year,
                "overlap_years": len(overlap),
                "status": "SKIP",
                "message": (
                    f"{series_id}: only {len(overlap)} overlap years "
                    f"(need {MIN_OVERLAP_YEARS})"
                ),
            })
            continue

        # Compute correlation
        corr = float(overlap[book_col].corr(overlap[ext_col]))

        checks.append({
            "series": series_id,
            "splice_year": splice_year,
            "overlap_years": len(overlap),
            "correlation": round(corr, 4),
            "min_correlation": MIN_CORRELATION,
            "status": "PASS" if corr >= MIN_CORRELATION else "WARN",
            "message": (
                f"{series_id}: overlap correlation={corr:.4f} "
                f"({len(overlap)} years, threshold={MIN_CORRELATION})"
            ),
        })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")
    n_skip = sum(1 for c in checks if c["status"] == "SKIP")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_warn == 0 else "warn",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_warn} WARN, {n_skip} SKIP out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))

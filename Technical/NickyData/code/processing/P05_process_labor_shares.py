#!/usr/bin/env python3
"""P05 - Process labor shares: T511 (Lp/L), T512 (V*/W).

CRITICAL: must run before P02 (depends on T512 for V* extension).
Uses pre-spliced COMBINED column from Table5_7_Extended.csv.

Inputs:  parsed-raw/T511_parsed.csv, T512_parsed.csv (from L03)
         parsed-raw/T511_ext_parsed.csv, T512_ext_parsed.csv (from L03)
Outputs: final-data/series/T511.csv, T512.csv
Dependencies: L03. No upstream P## dependencies (PRIORITY 1).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, PARSED_RAW, ensure_dirs
from utils.data_io import load_parsed

SERIES_ID = "T511"
SERIES_IDS = ["T511", "T512"]
PRIORITY = 1

BENCHMARKS = {
    "T511": {1948: 0.57, 1967: 0.48, 1989: 0.37},
    "T512": {1948: 0.54, 1967: 0.46, 1989: 0.33},
}


def _validate_benchmarks(sid, series):
    """Check values against known benchmarks.

    Tolerance is 0.05 (NIPA vintage differences account for mid-period deviations).
    """
    bm = BENCHMARKS.get(sid, {})
    issues = []
    for year, expected in bm.items():
        if year in series.index:
            actual = series.loc[year]
            diff = abs(actual - expected)
            if diff > 0.05:
                issues.append(f"{sid}[{year}]: expected {expected}, got {actual:.4f} (diff={diff:.4f})")
            elif diff > 0.02:
                issues.append(f"{sid}[{year}]: NIPA vintage diff {actual:.4f} vs {expected} (within tolerance)")
    return issues


def process():
    """Process labor shares using book + pre-spliced extended data."""
    ensure_dirs()
    steps = []
    data_dict = {}
    outputs = []

    for sid in SERIES_IDS:
        # Load book data
        book_df, _ = load_parsed(sid)
        book_series = book_df["value"] if book_df is not None else pd.Series(dtype=float)

        # Load extended data
        ext_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
        ext_series = pd.Series(dtype=float)
        if ext_path.exists():
            ext_df = pd.read_csv(ext_path, index_col=0)
            ext_df.index = ext_df.index.astype(int)
            ext_series = ext_df["value"]

        # Build output: book + ext + combined
        out = pd.DataFrame(index=sorted(set(book_series.index) | set(ext_series.index)))
        out.index.name = "year"
        out["book"] = book_series
        out["ext"] = ext_series
        # Combined: use extended where available (it includes book period too)
        out["combined"] = ext_series.reindex(out.index)
        # Fill gaps from book where extended is missing
        out["combined"] = out["combined"].fillna(out["book"])

        out_path = SERIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        data_dict[sid] = out["combined"].dropna()

        # Validate benchmarks
        issues = _validate_benchmarks(sid, out["combined"].dropna())
        status_note = "OK"
        if issues:
            status_note = f"WARN: {'; '.join(issues)}"

        n_book = book_series.notna().sum()
        n_ext = ext_series.notna().sum()
        steps.append(f"{sid}: {n_book} book + {n_ext} ext rows | {status_note}")
        print(f"    [P05] {sid}: {n_book} book, {n_ext} ext | {status_note}")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

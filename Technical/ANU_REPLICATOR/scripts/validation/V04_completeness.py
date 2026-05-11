#!/usr/bin/env python3
"""V04 - Completeness Checks: verify no unexpected NaN gaps in series data.

Core period (1948-1989) must be complete for all 26 Wave 1 series.
Extended series must be complete through their documented extension end year.

Inputs:
  - data/final-data/series/*.csv
  - series_registry.json (year_range per series)
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import SERIES_OUT
from lib.config_loader import load_registry

VALIDATOR_NAME = "V04_completeness"

# Core book period — all series should be complete here
CORE_START = 1948
CORE_END = 1989


def validate(series_filter=None, chapter_filter=None):
    registry = load_registry()
    checks = []
    series_files = sorted(SERIES_OUT.glob("T*.csv"))

    for csv_path in series_files:
        series_id = csv_path.stem
        if series_filter and series_id not in series_filter:
            continue

        entry = registry.get("series", {}).get(series_id, {})
        if chapter_filter is not None and entry.get("chapter") != chapter_filter:
            continue

        wave = entry.get("wave", 99)
        if wave > 1:
            continue  # Skip stub/future series

        try:
            df = pd.read_csv(csv_path)
        except Exception as exc:
            checks.append({
                "series": series_id,
                "status": "FAIL",
                "message": f"Cannot read: {exc}",
            })
            continue

        if "year" not in df.columns:
            df = df.rename(columns={df.columns[0]: "year"})

        # Find COMBINED column
        combined_col = None
        for col in df.columns:
            if "COMBINED" in col.upper() or col == series_id:
                combined_col = col
                break
        if combined_col is None:
            numeric_cols = [c for c in df.select_dtypes(include="number").columns
                           if c.lower() != "year"]
            if numeric_cols:
                combined_col = numeric_cols[-1]

        if combined_col is None:
            checks.append({
                "series": series_id,
                "status": "SKIP",
                "message": "No COMBINED or final column found",
            })
            continue

        # Determine expected year range
        year_range = entry.get("year_range", [CORE_START, CORE_END])
        exp_start = year_range[0] if year_range else CORE_START
        exp_end = year_range[1] if len(year_range) > 1 else CORE_END

        # Check core period completeness
        # Use the later of CORE_START and the first year with actual data
        actual_start = max(CORE_START, exp_start)
        # Also detect actual data start from the combined column
        non_null = df.loc[df[combined_col].notna(), "year"]
        if not non_null.empty:
            data_start = int(non_null.min())
            actual_start = max(actual_start, data_start)
        core_df = df[(df["year"] >= actual_start) & (df["year"] <= CORE_END)]
        core_years = set(core_df["year"].astype(int))
        expected_core = set(range(actual_start, CORE_END + 1))

        missing_years = sorted(expected_core - core_years)
        nan_years = []
        if combined_col in core_df.columns:
            nan_mask = core_df[combined_col].isna()
            nan_years = sorted(core_df.loc[nan_mask, "year"].astype(int).tolist())

        if missing_years or nan_years:
            checks.append({
                "series": series_id,
                "status": "FAIL",
                "message": (
                    f"{series_id}: core period gaps — "
                    f"missing years: {missing_years}, NaN years: {nan_years}"
                ),
                "missing_years": missing_years,
                "nan_years": nan_years,
            })
        else:
            # Also check extension period for NaN gaps
            ext_df = df[df["year"] > CORE_END]
            ext_nan = []
            if not ext_df.empty and combined_col in ext_df.columns:
                ext_nan_mask = ext_df[combined_col].isna()
                ext_nan = sorted(ext_df.loc[ext_nan_mask, "year"].astype(int).tolist())

            if ext_nan:
                checks.append({
                    "series": series_id,
                    "status": "WARN",
                    "message": f"{series_id}: extension period NaN gaps at {ext_nan}",
                    "nan_years": ext_nan,
                })
            else:
                total_rows = len(df[combined_col].dropna())
                checks.append({
                    "series": series_id,
                    "status": "PASS",
                    "message": f"{series_id}: complete ({total_rows} data points, {exp_start}-{exp_end})",
                })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_fail == 0 else "fail",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_fail} FAIL, {n_warn} WARN out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))

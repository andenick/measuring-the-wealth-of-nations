#!/usr/bin/env python3
"""V01 - Reference Value Validation: compare final series to published book values.

Checks series against benchmark_validation entries in config/validation_config.json.
Uses tolerance thresholds from the same config (rate_series, dollar_series, share_series).

Inputs:
  - data/final-data/series/*.csv
  - config/validation_config.json (benchmark_validation, tolerances, series_overrides)
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import SERIES_OUT, CONFIG

VALIDATOR_NAME = "V01_reference_values"


def _load_config():
    config_path = CONFIG / "validation_config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def validate(series_filter=None, chapter_filter=None):
    config = _load_config()
    benchmarks = config.get("benchmark_validation", {})
    tolerances = config.get("tolerances", {})
    overrides = config.get("series_overrides", {})

    checks = []

    for series_id, ref_values in benchmarks.items():
        if series_filter and series_id not in series_filter:
            continue

        csv_path = SERIES_OUT / f"{series_id}.csv"
        if not csv_path.exists():
            checks.append({
                "series": series_id,
                "status": "SKIP",
                "message": f"Series file not found: {csv_path.name}",
            })
            continue

        df = pd.read_csv(csv_path)
        if "year" not in df.columns:
            # Try first column as year
            df = df.rename(columns={df.columns[0]: "year"})

        # Find the COMBINED or final column
        combined_col = None
        for col in df.columns:
            if "COMBINED" in col.upper() or col == series_id:
                combined_col = col
                break
        if combined_col is None:
            # Use last numeric column
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            numeric_cols = [c for c in numeric_cols if c != "year"]
            if numeric_cols:
                combined_col = numeric_cols[-1]

        if combined_col is None:
            checks.append({
                "series": series_id,
                "status": "SKIP",
                "message": "No COMBINED or final column found",
            })
            continue

        # Determine tolerance
        series_type = overrides.get(series_id, "dollar_series")
        tol = tolerances.get(series_type, {"relative": 0.01, "absolute": 1.0})
        rel_tol = tol["relative"]
        abs_tol = tol["absolute"]

        for year_str, expected in ref_values.items():
            year = int(year_str)
            row = df[df["year"] == year]
            if row.empty:
                checks.append({
                    "series": series_id,
                    "year": year,
                    "expected": expected,
                    "actual": None,
                    "status": "FAIL",
                    "message": f"Year {year} not found in data",
                })
                continue

            actual = float(row[combined_col].iloc[0])
            abs_diff = abs(actual - expected)
            rel_diff = abs_diff / abs(expected) if expected != 0 else abs_diff

            passed = rel_diff <= rel_tol or abs_diff <= abs_tol
            checks.append({
                "series": series_id,
                "year": year,
                "expected": expected,
                "actual": round(actual, 6),
                "abs_diff": round(abs_diff, 6),
                "rel_diff": round(rel_diff, 6),
                "tolerance_type": series_type,
                "status": "PASS" if passed else "FAIL",
                "message": (
                    f"{series_id}[{year}]: {actual:.4f} vs {expected:.4f} "
                    f"(rel={rel_diff:.4%}, tol={rel_tol:.4%})"
                ),
            })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_fail == 0 else "fail",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_fail} FAIL out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))

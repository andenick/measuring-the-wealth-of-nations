#!/usr/bin/env python3
"""V06 - Splice Quality: assess transition quality at extension splice points.

Uses transition_checks from config/validation_config.json:
  - connection_ratio_range: [0.95, 1.05]
  - max_growth_rate_deviation: 0.05
  - min_trend_correlation: 0.95

Inputs:
  - data/final-data/series/*.csv
  - Technical/EXTENSION_LOG.json (splice years and methods)
  - config/validation_config.json
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import SERIES_OUT, CONFIG, TECHNICAL

VALIDATOR_NAME = "V06_splice_quality"

# Window size around splice year for trend analysis
WINDOW = 5


def _load_config():
    config_path = CONFIG / "validation_config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def _load_extension_log():
    ext_path = TECHNICAL / "EXTENSION_LOG.json"
    if not ext_path.exists():
        return []
    with open(ext_path, encoding="utf-8") as f:
        data = json.load(f)
    # Handle both formats: flat array or {"extensions": [...]}
    return data if isinstance(data, list) else data.get("extensions", [])


def validate(series_filter=None, chapter_filter=None):
    config = _load_config()
    tc = config.get("transition_checks", {})
    cr_range = tc.get("connection_ratio_range", [0.95, 1.05])
    max_gr_dev = tc.get("max_growth_rate_deviation", 0.05)

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
                "splice_year": splice_year,
                "status": "SKIP",
                "message": f"{series_id}: file not found",
            })
            continue

        df = pd.read_csv(csv_path)
        if "year" not in df.columns:
            df = df.rename(columns={df.columns[0]: "year"})
        df = df.sort_values("year").reset_index(drop=True)

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
            continue

        values = df.set_index("year")[combined_col].dropna()

        # Connection ratio: value at splice_year+1 / value at splice_year
        pre_val = values.get(splice_year)
        post_val = values.get(splice_year + 1)

        if pre_val is None or post_val is None or pre_val == 0:
            checks.append({
                "series": series_id,
                "splice_year": splice_year,
                "status": "SKIP",
                "message": f"{series_id}: missing values at splice point",
            })
            continue

        connection_ratio = float(post_val / pre_val)
        cr_ok = cr_range[0] <= connection_ratio <= cr_range[1]

        # Growth rate continuity: compare pre-splice and post-splice growth rates
        pre_window = values.loc[
            (values.index >= splice_year - WINDOW) & (values.index <= splice_year)
        ]
        post_window = values.loc[
            (values.index >= splice_year) & (values.index <= splice_year + WINDOW)
        ]

        gr_check = None
        if len(pre_window) >= 3 and len(post_window) >= 3:
            pre_gr = pre_window.pct_change().dropna().mean()
            post_gr = post_window.pct_change().dropna().mean()
            gr_deviation = abs(post_gr - pre_gr)
            gr_check = {
                "pre_growth_rate": round(float(pre_gr), 4),
                "post_growth_rate": round(float(post_gr), 4),
                "deviation": round(float(gr_deviation), 4),
                "passed": gr_deviation <= max_gr_dev,
            }

        overall_pass = cr_ok and (gr_check is None or gr_check["passed"])

        checks.append({
            "series": series_id,
            "splice_year": splice_year,
            "method": ext.get("splice_method", "unknown"),
            "connection_ratio": round(connection_ratio, 4),
            "connection_ratio_range": cr_range,
            "connection_ratio_ok": cr_ok,
            "growth_rate_check": gr_check,
            "status": "PASS" if overall_pass else "WARN",
            "message": (
                f"{series_id}[{splice_year}]: CR={connection_ratio:.4f} "
                f"({'OK' if cr_ok else 'OUT OF RANGE'})"
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

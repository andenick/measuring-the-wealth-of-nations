#!/usr/bin/env python3
"""V02 - Range Checks: verify all series values fall within expected bounds.

Uses tolerances and series_overrides from config/validation_config.json to determine
expected ranges per series type (rate_series, dollar_series, share_series).

Inputs:
  - data/final-data/series/*.csv
  - config/validation_config.json
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import SERIES_OUT, CONFIG, REGISTRY
from utils.config_loader import load_registry

VALIDATOR_NAME = "V02_range_checks"

# Expected value ranges by series type
# AS2 dollar series are in billions (1948: ~$100B, 2024: ~$30T)
RANGE_BOUNDS = {
    "rate_series": {"min": -10.0, "max": 100.0},
    "dollar_series": {"min": -10000.0, "max": 50000.0},
    "share_series": {"min": -0.1, "max": 1.1},
}

# Per-series overrides for non-standard ranges
SERIES_RANGE_OVERRIDES = {
    "T201": {"min": -1000.0, "max": 35000.0},
    "T515": {"min": 0.0, "max": 200000.0},
    "T516": {"min": 0.0, "max": 200000.0},
    "T513": {"min": 0.0, "max": 5.0},
    "T514": {"min": 0.0, "max": 5.0},
    "T608": {"min": -10.0, "max": 10.0},
    "T901": {"min": -10000.0, "max": 100000.0},
}


def _load_config():
    config_path = CONFIG / "validation_config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def validate(series_filter=None, chapter_filter=None):
    config = _load_config()
    overrides = config.get("series_overrides", {})
    registry = load_registry()

    checks = []
    series_files = sorted(SERIES_OUT.glob("T*.csv"))

    for csv_path in series_files:
        series_id = csv_path.stem
        if series_filter and series_id not in series_filter:
            continue

        if chapter_filter is not None:
            entry = registry.get("series", {}).get(series_id, {})
            if entry.get("chapter") != chapter_filter:
                continue

        try:
            df = pd.read_csv(csv_path)
        except Exception as exc:
            checks.append({
                "series": series_id,
                "status": "FAIL",
                "message": f"Cannot read {csv_path.name}: {exc}",
            })
            continue

        # Determine series type and bounds
        series_type = overrides.get(series_id, "dollar_series")
        if series_id in SERIES_RANGE_OVERRIDES:
            bounds = SERIES_RANGE_OVERRIDES[series_id]
        else:
            bounds = RANGE_BOUNDS.get(series_type, RANGE_BOUNDS["dollar_series"])

        # Check all numeric columns (excluding year)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        numeric_cols = [c for c in numeric_cols if c.lower() != "year"]

        for col in numeric_cols:
            values = df[col].dropna()
            if values.empty:
                continue

            vmin = float(values.min())
            vmax = float(values.max())
            out_of_range = (vmin < bounds["min"]) or (vmax > bounds["max"])

            checks.append({
                "series": series_id,
                "column": col,
                "min": round(vmin, 4),
                "max": round(vmax, 4),
                "expected_range": bounds,
                "type": series_type,
                "status": "FAIL" if out_of_range else "PASS",
                "message": (
                    f"{series_id}.{col}: [{vmin:.4f}, {vmax:.4f}] "
                    f"vs [{bounds['min']}, {bounds['max']}]"
                ),
            })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")

    for c in checks:
        if c["status"] == "FAIL":
            print(f"    [V02] FAIL: {c['message']}")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_fail == 0 else "fail",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_fail} FAIL out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))

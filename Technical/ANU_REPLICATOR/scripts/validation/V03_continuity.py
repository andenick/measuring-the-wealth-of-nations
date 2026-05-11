#!/usr/bin/env python3
"""V03 - Continuity Checks: detect unexpected year-over-year jumps.

Flags values where the year-over-year change exceeds a threshold, excluding
documented splice years from EXTENSION_LOG.json.

Inputs:
  - data/final-data/series/*.csv
  - Technical/EXTENSION_LOG.json (splice years to exclude)
  - config/validation_config.json
Dependencies: P00 must complete
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import SERIES_OUT, CONFIG, TECHNICAL
from lib.config_loader import load_registry

VALIDATOR_NAME = "V03_continuity"

# Maximum year-over-year relative change before flagging (200% = tripling)
MAX_YOY_CHANGE = 2.0
# For rate series, use absolute change threshold instead
MAX_RATE_ABS_CHANGE = 1.0


def _load_splice_years():
    """Load splice years from EXTENSION_LOG.json to exclude from continuity checks."""
    ext_log_path = TECHNICAL / "EXTENSION_LOG.json"
    splice_years = {}
    if ext_log_path.exists():
        with open(ext_log_path, encoding="utf-8") as f:
            ext_log = json.load(f)
        # Handle both formats: flat array or {"extensions": [...]}
        entries = ext_log if isinstance(ext_log, list) else ext_log.get("extensions", [])
        for entry in entries:
            sid = entry.get("series_id", "")
            sy = entry.get("splice_year")
            if sid and sy:
                splice_years.setdefault(sid, set()).add(int(sy))
    return splice_years


def _load_config():
    config_path = CONFIG / "validation_config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def validate(series_filter=None, chapter_filter=None):
    config = _load_config()
    overrides = config.get("series_overrides", {})
    splice_years = _load_splice_years()
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
        except Exception:
            continue

        if "year" not in df.columns:
            df = df.rename(columns={df.columns[0]: "year"})

        df = df.sort_values("year").reset_index(drop=True)
        excluded = splice_years.get(series_id, set())
        series_type = overrides.get(series_id, "dollar_series")
        is_rate = series_type in ("rate_series", "share_series")

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

        values = df[["year", combined_col]].dropna()
        discontinuities = []

        for i in range(1, len(values)):
            year = int(values.iloc[i]["year"])
            prev_year = int(values.iloc[i - 1]["year"])

            if year in excluded or (year - 1) in excluded:
                continue

            curr = float(values.iloc[i][combined_col])
            prev = float(values.iloc[i - 1][combined_col])

            if is_rate:
                abs_change = abs(curr - prev)
                if abs_change > MAX_RATE_ABS_CHANGE:
                    discontinuities.append({
                        "year": year,
                        "prev_year": prev_year,
                        "value": round(curr, 4),
                        "prev_value": round(prev, 4),
                        "abs_change": round(abs_change, 4),
                    })
            else:
                if prev != 0:
                    rel_change = abs((curr - prev) / prev)
                    if rel_change > MAX_YOY_CHANGE:
                        discontinuities.append({
                            "year": year,
                            "prev_year": prev_year,
                            "value": round(curr, 4),
                            "prev_value": round(prev, 4),
                            "rel_change": round(rel_change, 4),
                        })

        if discontinuities:
            checks.append({
                "series": series_id,
                "column": combined_col,
                "status": "WARN",
                "message": (
                    f"{series_id}: {len(discontinuities)} discontinuit(ies) "
                    f"(splice years excluded: {sorted(excluded) if excluded else 'none'})"
                ),
                "discontinuities": discontinuities,
            })
        else:
            checks.append({
                "series": series_id,
                "column": combined_col,
                "status": "PASS",
                "message": f"{series_id}: continuous (no unexpected jumps)",
            })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_warn == 0 else "warn",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_warn} WARN out of {len(checks)} checks",
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2, default=str))

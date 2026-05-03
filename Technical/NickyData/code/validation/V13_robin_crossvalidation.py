#!/usr/bin/env python3
"""V13 - Robin Cross-Validation: compare T513 profit rate against Robin's independent series.

Robin has an independently computed profit rate time series at
Robin/DATA/SHAIKH_TONAK/OUTPUT_DATA/Data/[2025.09.28] 01_HISTORICAL_REPLICATION_1958-1989.csv

Inputs: T513.csv, Robin profit rate CSV
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import SERIES_OUT

VALIDATOR_NAME = "V13_robin_crossvalidation"
ROBIN_PATH = Path("D:/Arcanum/Council/Robin/DATA/SHAIKH_TONAK/OUTPUT_DATA/Data/[2025.09.28] 01_HISTORICAL_REPLICATION_1958-1989.csv")


def validate(series_filter=None, chapter_filter=None):
    checks = []

    if not ROBIN_PATH.exists():
        return {"validator": VALIDATOR_NAME, "status": "skip",
                "checks": [{"status": "SKIP", "message": "Robin data not found"}],
                "summary": "Robin data not available"}

    robin = pd.read_csv(ROBIN_PATH)
    if "year" not in robin.columns or "profit_rate" not in robin.columns:
        return {"validator": VALIDATOR_NAME, "status": "skip",
                "checks": [{"status": "SKIP", "message": "Robin CSV format unexpected"}],
                "summary": "Robin format issue"}

    robin_r = robin.set_index("year")["profit_rate"].dropna()

    t513_path = SERIES_OUT / "T513.csv"
    if not t513_path.exists():
        return {"validator": VALIDATOR_NAME, "status": "skip",
                "checks": [{"status": "SKIP", "message": "T513 not found"}],
                "summary": "T513 not available"}

    t513 = pd.read_csv(t513_path, index_col=0)["combined"].dropna()

    common = t513.index.intersection(robin_r.index)
    if len(common) < 5:
        checks.append({"status": "SKIP", "message": f"Only {len(common)} overlapping years"})
    else:
        corr = float(t513[common].corr(robin_r[common]))
        t513_gr = t513[common].pct_change().dropna()
        robin_gr = robin_r[common].pct_change().dropna()
        gr_common = t513_gr.index.intersection(robin_gr.index)
        gr_corr = float(t513_gr[gr_common].corr(robin_gr[gr_common])) if len(gr_common) > 2 else 0

        ratio = float((t513[common] / robin_r[common]).mean())

        checks.append({
            "check": "T513 vs Robin profit rate",
            "overlap_years": len(common),
            "level_correlation": round(corr, 4),
            "growth_rate_correlation": round(gr_corr, 4),
            "mean_ratio": round(ratio, 4),
            "status": "PASS" if corr > 0.7 else "WARN",
            "message": f"T513 vs Robin: corr={corr:.3f}, gr_corr={gr_corr:.3f}, ratio={ratio:.2f} ({len(common)} years)",
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
    import json
    print(json.dumps(validate(), indent=2))

#!/usr/bin/env python3
"""V11 - External Study Benchmark Validation: check N-series against HDARP values.

Validates external study series against benchmark values extracted from
the original papers via HDARP.

Inputs:
  - data/final-data/book/series/N*.csv (or studies/series/)
Dependencies: P16-P20 must complete
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, STUDIES_OUT

VALIDATOR_NAME = "V11_external_benchmarks"

# Benchmark values from HDARP extractions
BENCHMARKS = {
    # Mohun (2005): ST/Mohun exploitation ratio
    "N1404": {
        "check": "ST/Mohun exploitation ratio",
        "mean_range": [1.4, 1.8],  # Expected ~1.61
    },
    # Moos (2017): NSW/GDP statistics
    "N1301": {
        "check": "Moos NSW/GDP post-2000",
        "post_2000_positive": True,  # Moos found NSW positive after 2000
    },
    # Turkey (2022): All-negative NSW
    "N1602": {
        "check": "Turkey NSW all negative",
        "all_negative": True,
        "mean_range": [-0.025, -0.005],  # Expected ~-0.0113
    },
    # Tonak (1984): Labor share range
    "N1001": {
        "check": "Tonak labor share range",
        "mean_range": [0.68, 0.76],  # Expected 0.71-0.73
    },
    # Mohun (2013): Class decomposition ratio
    "N1501": {
        "check": "Mohun WC unproductive share ~81%",
        "mean_range": [0.75, 0.90],  # N1501/N1503 should be ~0.813
    },
}


def _load(sid):
    for d in [SERIES_OUT, STUDIES_OUT]:
        path = d / f"{sid}.csv"
        if path.exists():
            df = pd.read_csv(path, index_col=0)
            col = "combined" if "combined" in df.columns else df.columns[-1]
            return df[col].dropna()
    return pd.Series(dtype=float)


def validate(series_filter=None, chapter_filter=None):
    checks = []

    for sid, bm in BENCHMARKS.items():
        if series_filter and sid not in series_filter:
            continue

        series = _load(sid)
        if len(series) == 0:
            checks.append({
                "series": sid,
                "check": bm["check"],
                "status": "SKIP",
                "message": f"{sid}: not found",
            })
            continue

        # Check mean range
        if "mean_range" in bm:
            mean_val = float(series.mean())
            lo, hi = bm["mean_range"]
            in_range = lo <= mean_val <= hi
            checks.append({
                "series": sid,
                "check": f"{bm['check']} mean in [{lo}, {hi}]",
                "mean": round(mean_val, 4),
                "status": "PASS" if in_range else "WARN",
                "message": f"{sid}: mean={mean_val:.4f} {'in' if in_range else 'OUT OF'} [{lo}, {hi}]",
            })

        # Check all-negative
        if bm.get("all_negative"):
            all_neg = bool((series < 0).all())
            checks.append({
                "series": sid,
                "check": f"{bm['check']} all negative",
                "all_negative": all_neg,
                "status": "PASS" if all_neg else "WARN",
                "message": f"{sid}: all negative = {all_neg} ({len(series)} years)",
            })

        # Check post-2000 positive (Moos)
        if bm.get("post_2000_positive"):
            post = series[series.index > 2000]
            if len(post) > 0:
                mean_post = float(post.mean())
                is_positive = mean_post > 0
                checks.append({
                    "series": sid,
                    "check": f"{bm['check']}",
                    "post_2000_mean": round(mean_post, 4),
                    "status": "PASS" if is_positive else "WARN",
                    "message": f"{sid}: post-2000 mean={mean_post:.4f} ({'positive' if is_positive else 'negative'})",
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
    import json
    result = validate()
    print(json.dumps(result, indent=2))

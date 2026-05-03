#!/usr/bin/env python3
"""V12 - NSW Cross-Study Consistency: verify overlapping NSW estimates agree.

Checks correlation between NSW estimates from different studies for
overlapping time periods. Trends should agree even if levels differ.

Inputs: T607, N1101, N1202, N1302 series
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import SERIES_OUT, STUDIES_OUT

VALIDATOR_NAME = "V12_nsw_cross_study"

NSW_PAIRS = [
    ("T607", "N1302", "ST94 NSW vs Moos NSW/EC", 1952, 2012),
    ("N1101", "N1202", "ST87 net transfer vs ST02 NSW/EC", 1952, 1985),
]


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

    for sid_a, sid_b, desc, yr_start, yr_end in NSW_PAIRS:
        a = _load(sid_a)
        b = _load(sid_b)

        if len(a) == 0 or len(b) == 0:
            checks.append({"check": desc, "status": "SKIP", "message": f"{desc}: data missing"})
            continue

        common = a.index.intersection(b.index)
        common = [y for y in common if yr_start <= y <= yr_end]

        if len(common) < 5:
            checks.append({"check": desc, "status": "SKIP",
                          "message": f"{desc}: only {len(common)} overlapping years"})
            continue

        a_c = a[common]
        b_c = b[common]

        # Level correlation
        corr = float(a_c.corr(b_c)) if len(a_c) > 2 else 0

        # Growth rate correlation
        a_gr = a_c.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
        b_gr = b_c.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
        gr_common = a_gr.index.intersection(b_gr.index)
        gr_corr = float(a_gr[gr_common].corr(b_gr[gr_common])) if len(gr_common) > 2 else 0

        status = "PASS" if abs(corr) > 0.5 else "WARN"

        checks.append({
            "check": desc,
            "series_a": sid_a,
            "series_b": sid_b,
            "overlap_years": len(common),
            "level_correlation": round(corr, 4),
            "growth_rate_correlation": round(gr_corr, 4),
            "status": status,
            "message": f"{desc}: level_corr={corr:.3f}, gr_corr={gr_corr:.3f} ({len(common)} years)",
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

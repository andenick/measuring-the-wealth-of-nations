"""V03_XS1602 - Turkey NSW/GDP K&T finding + registry anchors + summary stats.

Refactored 2026-05-23 per Decision 0008:
  - `validation.reference_values` carries year-keyed scalars (1980, 2019).
  - `validation.derived_statistics` carries `mean` (-0.0113) and `n_negative` (40).
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402
from utils.registry_validator import (  # noqa: E402
    get_derived_statistics,
    get_reference_values,
)


SERIES_ID = "XS1602"
ANCHOR_TOL_ABS = 0.01
MEAN_TOL_ABS = 0.02
NEG_TOL_ABS = 5  # n_negative count tolerance (chopped may be missing years)


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == f"{SERIES_ID}-A"]
    valid = df.dropna(subset=["value"])
    n_neg = int((valid["value"] < 0).sum())
    n_total = len(valid)
    pct_negative = n_neg / n_total if n_total else 0
    # K&T finding: NSW negative for all/most of 1980-2019
    pct_finding_ok = pct_negative >= 0.7 and n_total >= 20

    # Year-anchor checks
    anchors = get_reference_values(SERIES_ID)
    anchor_checks = []
    for year, expected in anchors.items():
        row = df[df["year"] == year]
        if row.empty:
            anchor_checks.append({"year": year, "expected": expected, "status": "MISSING"})
            continue
        actual = float(row["value"].iloc[0])
        abs_err = abs(actual - float(expected))
        anchor_checks.append({
            "year": year, "expected": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6),
            "status": "PASS" if abs_err <= ANCHOR_TOL_ABS else "FAIL",
        })
    n_anchor_fail = sum(1 for c in anchor_checks if c["status"] == "FAIL")
    n_anchor_miss = sum(1 for c in anchor_checks if c["status"] == "MISSING")

    # Derived statistics
    stats = get_derived_statistics(SERIES_ID)
    stat_checks = []
    if "mean" in stats:
        expected = float(stats["mean"])
        actual = float(valid["value"].mean())
        abs_err = abs(actual - expected)
        stat_checks.append({
            "stat": "mean", "expected": expected, "actual": round(actual, 6),
            "abs_err": round(abs_err, 6),
            "status": "PASS" if abs_err <= MEAN_TOL_ABS else "FAIL",
        })
    if "n_negative" in stats:
        expected = int(stats["n_negative"])
        abs_err = abs(n_neg - expected)
        stat_checks.append({
            "stat": "n_negative", "expected": expected, "actual": n_neg,
            "abs_err": abs_err,
            "status": "PASS" if abs_err <= NEG_TOL_ABS else "FAIL",
        })
    n_stat_fail = sum(1 for c in stat_checks if c["status"] == "FAIL")

    ok = pct_finding_ok and n_anchor_fail == 0 and n_anchor_miss == 0 and n_stat_fail == 0
    status = "PASS" if ok else "FAIL"
    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status,
        "n_pass": (sum(1 for c in anchor_checks if c["status"] == "PASS")
                   + sum(1 for c in stat_checks if c["status"] == "PASS")),
        "n_fail": n_anchor_fail + n_stat_fail,
        "n_missing": n_anchor_miss,
        "kt_finding": {"n_negative": n_neg, "n_total": n_total,
                       "pct_negative": pct_negative,
                       "rule": "K&T 2022: NSW negative for nearly all 1980-2019 years"},
        "anchors": {"checks": anchor_checks},
        "derived_statistics": {"checks": stat_checks},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} {n_neg}/{n_total} negative years ({pct_negative:.0%})")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

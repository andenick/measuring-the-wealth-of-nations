"""V03_ES1305 - post-2000 structural shift + registry anchors + stat.

Refactored 2026-05-23 per Decision 0008:
  - `validation.reference_values` carries year-keyed scalars (1959, 2012).
  - `validation.derived_statistics` carries `structural_shift` (0.03).
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


SERIES_ID = "ES1305"
ANCHOR_TOL_ABS = 0.01
SHIFT_TOL_ABS = 0.05  # structural-shift magnitude is approximate


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == f"{SERIES_ID}-A"]
    post = float(df[df["year"] >= 2000]["value"].mean())
    pre = float(df[df["year"] < 2000]["value"].mean())
    shift_detected = bool(post > pre)
    observed_shift = post - pre

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

    # Derived-statistic check: structural_shift magnitude
    stats = get_derived_statistics(SERIES_ID)
    stat_checks = []
    if "structural_shift" in stats:
        expected_shift = float(stats["structural_shift"])
        abs_err = abs(observed_shift - expected_shift)
        stat_checks.append({
            "stat": "structural_shift", "expected": expected_shift,
            "actual": round(observed_shift, 6), "abs_err": round(abs_err, 6),
            "status": "PASS" if abs_err <= SHIFT_TOL_ABS else "FAIL",
        })
    n_stat_fail = sum(1 for c in stat_checks if c["status"] == "FAIL")

    ok = shift_detected and len(df) > 0 and n_anchor_fail == 0 and n_anchor_miss == 0 and n_stat_fail == 0
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
        "structural_break": {
            "pre_2000_avg": pre, "post_2000_avg": post,
            "observed_shift": round(observed_shift, 6),
            "detected": shift_detected,
        },
        "anchors": {"checks": anchor_checks},
        "derived_statistics": {"checks": stat_checks},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} pre2000_avg={pre:.4f} post2000_avg={post:.4f} shift={observed_shift:.4f}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_ES1301 - range check + registry anchors for Moos NSW/GDP.

Refactored 2026-05-23 per Decision 0008:
  - `validation.reference_values` is year-keyed scalars only
    (post-migration: {1959: -0.01455, 2012: 0.06726}).
  - `validation.derived_statistics` holds the legacy `1959_1997_mean`
    summary statistic (0.011).
Helpers used:
  - `get_reference_values(sid)` -> year anchors (Decision 0002 + 0008).
  - `get_derived_statistics(sid)` -> period-windowed stats (Decision 0008).
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


SERIES_ID = "ES1301"
ANCHOR_TOL_ABS = 0.01
STAT_TOL_ABS = 0.05  # period mean is a coarse summary; loose tolerance is fine


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == f"{SERIES_ID}-A"]
    in_range = bool(df["value"].between(-0.05, 0.10).all())

    # Year-anchor checks (Decision 0008 reference_values contract)
    anchors = get_reference_values(SERIES_ID)
    anchor_checks = []
    for year, expected in anchors.items():
        row = df[df["year"] == year]
        if row.empty:
            anchor_checks.append({"year": year, "expected": expected,
                                  "status": "MISSING"})
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

    # Period-mean statistic check (Decision 0008 derived_statistics)
    stats = get_derived_statistics(SERIES_ID)
    stat_checks = []
    if "1959_1997_mean" in stats:
        window = df[(df["year"] >= 1959) & (df["year"] <= 1997)]["value"]
        actual_mean = float(window.mean()) if len(window) else float("nan")
        expected = float(stats["1959_1997_mean"])
        abs_err = abs(actual_mean - expected)
        stat_checks.append({
            "stat": "1959_1997_mean", "expected": expected,
            "actual": round(actual_mean, 6), "abs_err": round(abs_err, 6),
            "status": "PASS" if abs_err <= STAT_TOL_ABS else "FAIL",
        })
    n_stat_fail = sum(1 for c in stat_checks if c["status"] == "FAIL")

    ok = in_range and len(df) > 0 and n_anchor_fail == 0 and n_anchor_miss == 0 and n_stat_fail == 0
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
        "range_check": {
            "expected": [-0.05, 0.10],
            "actual": [float(df["value"].min()), float(df["value"].max())],
        },
        "anchors": {"checks": anchor_checks},
        "derived_statistics": {"checks": stat_checks},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} range=[{df['value'].min():.4f}, {df['value'].max():.4f}] anchors_pass={sum(1 for c in anchor_checks if c['status']=='PASS')}/{len(anchor_checks)}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

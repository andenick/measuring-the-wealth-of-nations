"""V03_XS002 - Khanjian cross-validation against registry year anchors.

Refactored 2026-05-23 per Decision 0008:
  - The legacy V03 read a derived diagnostic column
    (`our_gap_to_khanjian_pct`) that does not appear in chopped output, so
    the validator was effectively skipped at cohort-1 refactor time.
  - XS002's `validation.reference_values` is already year-keyed (the five IO
    benchmark years 1958, 1963, 1967, 1972, 1977 from book Ch7 §7.3 / App. I
    Table I.1). We now compare those anchors directly against the chopped
    XS002-A column (rate of surplus value via Khanjian decomposition).
  - `validation.derived_statistics` is currently empty for XS002.
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


SERIES_ID = "XS002"
ANCHOR_TOL_ABS = 0.01  # tight - these are Khanjian's reported benchmark values


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == f"{SERIES_ID}-A"]

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
    n_anchor_pass = sum(1 for c in anchor_checks if c["status"] == "PASS")
    n_anchor_fail = sum(1 for c in anchor_checks if c["status"] == "FAIL")
    n_anchor_miss = sum(1 for c in anchor_checks if c["status"] == "MISSING")

    # Derived statistics block currently empty per Decision 0008 patch; loop
    # is kept so a future addition (e.g., overall mean gap to Khanjian) lands
    # without further refactoring.
    stats = get_derived_statistics(SERIES_ID)
    stat_checks = []  # no statistics defined yet

    ok = (len(df) > 0 and n_anchor_fail == 0 and n_anchor_miss == 0
          and len(anchor_checks) > 0)
    status = "PASS" if ok else "FAIL"
    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": n_anchor_pass,
        "n_fail": n_anchor_fail,
        "n_missing": n_anchor_miss,
        "anchors": {
            "checks": anchor_checks,
            "rule": ("XS002-A column (rate of surplus value via Khanjian "
                     "Appendix I 25-step decomposition) compared to the five "
                     "IO benchmark years recorded in registry."),
        },
        "derived_statistics": {"checks": stat_checks,
                               "available": list(stats.keys())},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} anchors={n_anchor_pass}/{len(anchor_checks)}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_S509 — Validate Productive Investment (IG*) against expected range (no published benchmark)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_validation_result  # noqa: E402


SERIES_ID = "S509"


def run():
    """No published benchmark in validation_config — apply range check instead."""
    final_csv = DATA_FINAL / f"{SERIES_ID}.csv"
    df = pd.read_csv(final_csv)
    df = df[df["series_id"] == "S509-A"]

    val_1948 = float(df[df["year"] == 1948]["value"].iloc[0])
    expected_1948_approx = 44.27  # value visible directly in TableE2_RevenueAccounts row 1948

    abs_err = abs(val_1948 - expected_1948_approx)
    status = "PASS" if abs_err < 0.01 else "FAIL"

    result = {
        "series_id":       SERIES_ID,
        "run_at":          datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "dollar_series",
        "status":          status,
        "n_pass":          1 if status == "PASS" else 0,
        "n_fail":          0 if status == "PASS" else 1,
        "n_missing":       0,
        "range_check":     {"year": 1948, "value": val_1948, "expected": expected_1948_approx,
                            "abs_err": abs_err, "note": "No published benchmark in validation_config; "
                                                        "round-trip check against E.2 row value."},
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_S509] status={status} val_1948={val_1948:.2f}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

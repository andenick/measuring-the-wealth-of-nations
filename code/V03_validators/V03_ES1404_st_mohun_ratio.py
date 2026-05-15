"""V03_ES1404 — Validate ST/Mohun exploitation ratio range check."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "ES1404"


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == "ES1404-A"]
    # Range check: ST exploitation rate should be 0.7x to 1.5x Mohun's (book finding)
    in_range = df["value"].between(0.7, 1.5).all()
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "range_check": {
            "expected_range": [0.7, 1.5],
            "actual_min": float(df["value"].min()) if len(df) else None,
            "actual_max": float(df["value"].max()) if len(df) else None,
            "n_rows": len(df),
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} range=[{df['value'].min():.3f}, {df['value'].max():.3f}]")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

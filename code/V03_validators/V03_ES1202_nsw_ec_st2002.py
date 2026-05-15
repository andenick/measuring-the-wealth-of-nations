"""V03_ES1202 — NSW/EC range check."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "ES1202.csv")
    df = df[df["series_id"] == "ES1202-A"]
    in_range = bool(df["value"].between(-0.10, 0.20).all())
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "ES1202",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "range_check": {"expected": [-0.10, 0.20],
                        "actual": [float(df["value"].min()), float(df["value"].max())]},
    }
    write_validation_result("ES1202", result)
    print(f"    [V03_ES1202] status={status} NSW/EC range=[{df['value'].min():.4f}, {df['value'].max():.4f}]")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

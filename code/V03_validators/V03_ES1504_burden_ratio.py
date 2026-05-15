"""V03_ES1504 — Validate Lu/Lp ratio range."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "ES1504.csv")
    df = df[df["series_id"] == "ES1504-A"]
    # Burden ratio: expect 0.5 to 2.0 over the period
    in_range = bool(df["value"].between(0.5, 2.0).all())
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "ES1504",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status, "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "range_check": {"expected": [0.5, 2.0], "actual_min": float(df["value"].min()), "actual_max": float(df["value"].max())},
    }
    write_validation_result("ES1504", result)
    print(f"    [V03_ES1504] status={status} range=[{df['value'].min():.4f}, {df['value'].max():.4f}]")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

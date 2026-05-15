"""V03_ES1102 — Range check for Social Benefit Rate (S&T 1987)."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "ES1102.csv")
    df = df[df["series_id"] == "ES1102-A"]
    # Range: ratios should be small (single-digit percent of EC, so 0.0x-0.5x)
    in_range = bool(df["value"].between(-1.0, 1.0).all())
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "ES1102",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status, "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "range_check": {"expected": [-1.0, 1.0], "actual_min": float(df["value"].min()), "actual_max": float(df["value"].max())},
    }
    write_validation_result("ES1102", result)
    print(f"    [V03_ES1102] status={status} range=[{df['value'].min():.4f}, {df['value'].max():.4f}]")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

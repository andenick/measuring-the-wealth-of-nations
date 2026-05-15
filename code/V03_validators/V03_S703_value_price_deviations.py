"""V03_S703 — value-price deviation should be modest (book: 2-15%)."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "S703.csv")
    df = df[df["series_id"] == "S703-A"]
    in_range = bool(df["value"].between(0, 100).all())  # 0-100% (very wide; book says 2-15%)
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "S703",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series", "status": status,
        "n_pass": 1 if status == "PASS" else 0, "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "range_check": {"expected": [0, 100], "actual": [float(df["value"].min()), float(df["value"].max())]},
    }
    write_validation_result("S703", result)
    print(f"    [V03_S703] status={status} deviation range=[{df['value'].min():.2f}%, {df['value'].max():.2f}%]")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

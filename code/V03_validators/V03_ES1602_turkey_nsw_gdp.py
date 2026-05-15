"""V03_ES1602 — confirm Turkey NSW is mostly negative (K&T finding)."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "ES1602.csv")
    df = df[df["series_id"] == "ES1602-A"]
    valid = df.dropna(subset=["value"])
    n_neg = int((valid["value"] < 0).sum())
    n_total = len(valid)
    pct_negative = n_neg / n_total if n_total else 0
    # K&T finding: NSW negative for all/most of 1980-2019
    status = "PASS" if pct_negative >= 0.7 and n_total >= 20 else "FAIL"
    result = {
        "series_id": "ES1602",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series", "status": status,
        "n_pass": 1 if status == "PASS" else 0, "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "kt_finding": {"n_negative": n_neg, "n_total": n_total, "pct_negative": pct_negative,
                       "rule": "K&T 2022: NSW negative for nearly all 1980-2019 years"},
    }
    write_validation_result("ES1602", result)
    print(f"    [V03_ES1602] status={status} {n_neg}/{n_total} negative years ({pct_negative:.0%})")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

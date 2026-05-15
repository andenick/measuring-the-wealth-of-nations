"""V03_ES1305."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "ES1305.csv")
    df = df[df["series_id"] == "ES1305-A"]
    # Test: post-2000 deltas should average HIGHER than pre-2000 (the structural break)
    post = df[df["year"] >= 2000]["value"].mean()
    pre  = df[df["year"] < 2000]["value"].mean()  # should be 0 by construction
    shift_detected = bool(post > pre)
    status = "PASS" if shift_detected and len(df) > 0 else "FAIL"
    result = {
        "series_id": "ES1305",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series", "status": status,
        "n_pass": 1 if status == "PASS" else 0, "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "structural_break": {"pre_2000_avg": float(pre), "post_2000_avg": float(post), "detected": shift_detected},
    }
    write_validation_result("ES1305", result)
    print(f"    [V03_ES1305] status={status} pre2000_avg={pre:.4f}, post2000_avg={post:.4f}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_S402 — B trace ≥ n (since B = I + A + A² + ... so diagonal ≥ 1)."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    df = pd.read_csv(DATA_FINAL / "S402.csv")
    trace_ok = bool((df["b_trace"] >= df["n_sectors"] - 0.01).all())
    status = "PASS" if trace_ok and len(df) > 0 else "FAIL"
    result = {
        "series_id": "S402",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series", "status": status,
        "n_pass": 1 if status == "PASS" else 0, "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "checks": {
            "b_trace_ge_n": trace_ok,
            "n_benchmark_years": len(df),
            "frobenius_range": [float(df["b_frobenius_norm"].min()), float(df["b_frobenius_norm"].max())],
        },
    }
    write_validation_result("S402", result)
    print(f"    [V03_S402] status={status} trace_ge_n={trace_ok}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

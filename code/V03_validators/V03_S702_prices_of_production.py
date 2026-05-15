"""V03_S702 — prices of production > labor values (markup > 0)."""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_validation_result
from utils.paths import DATA_FINAL

def run():
    s701 = pd.read_csv(DATA_FINAL / "S701.csv")
    s701 = s701[s701["series_id"] == "S701-A"][["year", "value"]].rename(columns={"value": "lambda"})
    s702 = pd.read_csv(DATA_FINAL / "S702.csv")
    s702 = s702[s702["series_id"] == "S702-A"][["year", "value"]].rename(columns={"value": "p"})
    merged = s701.merge(s702, on="year")
    # p > λ (markup positive)
    markup_positive = bool((merged["p"] > merged["lambda"]).all())
    status = "PASS" if markup_positive and len(merged) > 0 else "FAIL"
    result = {
        "series_id": "S702",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series", "status": status,
        "n_pass": 1 if status == "PASS" else 0, "n_fail": 0 if status == "PASS" else 1, "n_missing": 0,
        "checks": {"markup_positive_all_years": markup_positive,
                   "n_benchmark_years": len(merged)},
    }
    write_validation_result("S702", result)
    print(f"    [V03_S702] status={status} markup_positive={markup_positive}")
    return result

if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

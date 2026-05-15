"""V03_S514 — Validate r*_adj range (must be lower than r* due to TCU<100)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S514.csv")
    df = df[df["series_id"] == "S514-A"]
    valid = df.dropna(subset=["value"])
    s513 = pd.read_csv(DATA_FINAL / "S513.csv")
    s513 = s513[s513["series_id"] == "S513-A"][["year", "value"]].rename(columns={"value": "r_star"})
    merged = valid.merge(s513, on="year")
    # r_adj <= r_star (since TCU <= 100)
    all_under = bool((merged["value"] <= merged["r_star"] + 1e-9).all())
    status = "PASS" if all_under and len(valid) > 0 else "FAIL"
    result = {
        "series_id": "S514",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": int(df["value"].isna().sum()),
        "checks": {
            "r_adj_always_le_r_star": all_under,
            "n_valid_years": len(valid),
            "n_pending_pre_1967": int(df["value"].isna().sum()),
        },
    }
    write_validation_result("S514", result)
    print(f"    [V03_S514] status={status} valid_years={len(valid)} pending_pre_1967={int(df['value'].isna().sum())}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

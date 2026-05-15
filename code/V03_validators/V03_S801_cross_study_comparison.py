"""V03_S801 — Confirm cross-study merge is well-formed."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S801.csv")
    df = df[df["series_id"] == "S801-A"]
    # Round-trip: S801 value column = ST_e = upstream S506
    s506 = pd.read_csv(DATA_FINAL / "S506.csv")
    s506 = s506[s506["series_id"] == "S506-A"][["year", "value"]].rename(columns={"value": "S506"})
    merged = df[["year", "value"]].rename(columns={"value": "S801"}).merge(s506, on="year")
    max_err = float((merged["S801"] - merged["S506"]).abs().max())
    status = "PASS" if max_err < 1e-9 and len(df) >= 30 else "FAIL"
    result = {
        "series_id": "S801",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "round_trip_check": {"vs_S506_max_err": max_err, "comparison_years": len(df)},
    }
    write_validation_result("S801", result)
    print(f"    [V03_S801] status={status} round_trip_max_err={max_err}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

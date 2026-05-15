"""V03_S201 — Validate GFP/GDP ratio range (book finding: ~0.55-0.65)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S201.csv")
    df = df[df["series_id"] == "S201-A"]
    in_range = bool(df["value"].between(0.6, 1.0).all())
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "S201",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "checks": {
            "GFP_GDP_range_expected": [0.6, 1.0],
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None,
            "v_1989": float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None,
        },
    }
    write_validation_result("S201", result)
    print(f"    [V03_S201] status={status} GFP/GDP range=[{df['value'].min():.3f}, {df['value'].max():.3f}]")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

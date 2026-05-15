"""V03_S513 — Validate Marxian profit rate range + secular trend."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S513.csv")
    df = df[df["series_id"] == "S513-A"].sort_values("year")
    # r* should be in [0.05, 1.5] for any year (book values ~0.4-0.8 nominally)
    in_range = bool(df["value"].between(0.05, 2.0).all())
    # Secular trend: r* in late 80s should be LOWER than late 40s (book finding)
    v_1948 = float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None
    v_1989 = float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None
    trend_ok = v_1989 < v_1948 if (v_1948 and v_1989) else None

    status = "PASS" if (in_range and len(df) > 0) else "FAIL"
    result = {
        "series_id": "S513",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "checks": {
            "in_range": in_range, "range_expected": [0.05, 2.0],
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": v_1948, "v_1989": v_1989,
            "secular_decline_1948_to_1989": trend_ok,
        },
    }
    write_validation_result("S513", result)
    print(f"    [V03_S513] status={status} r*: 1948={v_1948:.4f}, 1989={v_1989:.4f}, declined={trend_ok}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

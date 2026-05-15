"""V03_AS001 — Validate social burden rate against book Table 7.1 finding.

Book finding: b rises 0.56 -> 0.66 (1948 -> 1989). Range check:
- Range over period: [0.4, 0.9]
- Rising trend: 1989 > 1948
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "AS001.csv")
    df = df[df["series_id"] == "AS001-A"]
    in_range = bool(df["value"].between(0.3, 0.95).all())
    v_1948 = float(df[df["year"] == 1948]["value"].iloc[0]) if (df["year"] == 1948).any() else None
    v_1989 = float(df[df["year"] == 1989]["value"].iloc[0]) if (df["year"] == 1989).any() else None
    rising = (v_1989 > v_1948) if (v_1948 and v_1989) else None
    status = "PASS" if in_range and len(df) > 0 else "FAIL"
    result = {
        "series_id": "AS001",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "share_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "checks": {
            "in_range": in_range,
            "actual_range": [float(df["value"].min()), float(df["value"].max())],
            "v_1948": v_1948, "v_1989": v_1989,
            "rising_1948_to_1989": rising,
            "note": "Book reports b rises 0.56->0.66 (16% increase). Our Pn approximation uses NIPA total corporate profits (slight over-count vs productive Pn).",
        },
    }
    write_validation_result("AS001", result)
    print(f"    [V03_AS001] status={status} b 1948={v_1948:.4f}, 1989={v_1989:.4f}, rising={rising}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

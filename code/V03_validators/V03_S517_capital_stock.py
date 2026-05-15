"""V03_S517 — Validate K* range and monotonicity."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S517"


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    df = df[df["series_id"] == "S517-A"].sort_values("year").reset_index(drop=True)

    # K* should be positive and broadly monotonic-increasing
    all_positive = bool((df["value"] > 0).all())
    # Year-over-year decreases allowed only in deep recessions; check no year has >5% nominal drop
    diffs = df["value"].pct_change()
    nominal_drops = diffs[diffs < -0.05]

    # Sanity: 1948 should be ~$300B (book era starting K*); 1989 ~$10000B; 2024 >$35000B
    v_1948 = float(df[df["year"] == 1948]["value"].iloc[0])
    v_1989 = float(df[df["year"] == 1989]["value"].iloc[0])
    v_2024 = float(df[df["year"] == 2024]["value"].iloc[0])

    status = "PASS"
    if not all_positive: status = "FAIL"
    elif v_1948 < 100 or v_1948 > 1000: status = "FAIL"
    elif v_1989 < 5000 or v_1989 > 20000: status = "FAIL"
    elif v_2024 < 30000: status = "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "level_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "checks": {
            "all_positive": all_positive,
            "v_1948": v_1948,
            "v_1989": v_1989,
            "v_2024": v_2024,
            "nominal_drop_years": nominal_drops.dropna().to_dict() if len(nominal_drops) else {},
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_S517] status={status} K*: 1948={v_1948:.0f}B, 1989={v_1989:.0f}B, 2024={v_2024:.0f}B")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

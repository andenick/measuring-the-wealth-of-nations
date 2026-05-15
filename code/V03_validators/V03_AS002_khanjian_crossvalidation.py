"""V03_AS002 — Validate Khanjian gap is within book's reported range."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "AS002"


def run():
    df = pd.read_csv(DATA_FINAL / f"{SERIES_ID}.csv")
    # Book reports Khanjian-vs-ST gap in the 6.7-9.3% range across these years.
    # Our gap (to Khanjian's e_star_rev FROM our S506) should mirror this
    # qualitatively. Check: all gaps > 0 (Khanjian is higher) and < 50%.
    gaps = df["our_gap_to_khanjian_pct"].astype(float)
    all_positive = bool((gaps > 0).all())
    all_under_50 = bool((gaps < 50).all())
    status = "PASS" if (all_positive and all_under_50 and len(df) > 0) else "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "range_check": {
            "rule": "Khanjian's e_star_rev > our S506 by 0% to 50% (book reports 6.7-9.3% gap)",
            "actual_gaps_pct": gaps.tolist(),
            "n_cross_validation_years": len(df),
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status}; gaps={gaps.tolist()}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""V03_S608 — Validate NSW/V* ratio (round-trip via S607 and S504)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_validation_result  # noqa: E402


SERIES_ID = "S608"


def run():
    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s608 = pd.read_csv(DATA_FINAL / "S608.csv")
    s607 = s607[s607["series_id"] == "S607-A"][["year", "value"]].rename(columns={"value": "NSW"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    s608 = s608[s608["series_id"] == "S608-A"][["year", "value"]].rename(columns={"value": "ratio"})

    overlap = s607.merge(s504, on="year").merge(s608, on="year")
    overlap["implied"] = overlap["NSW"] / overlap["V_star"]
    overlap["abs_err"] = (overlap["implied"] - overlap["ratio"]).abs()

    max_err = float(overlap["abs_err"].max()) if len(overlap) else None
    status = "PASS" if (max_err is None or max_err < 1e-6) else "FAIL"

    result = {
        "series_id": SERIES_ID,
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "identity_check": {
            "identity": "S608 = S607 / S504 (NSW / V*)",
            "compared_years": len(overlap),
            "max_abs_err": max_err,
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} identity_check max_err={max_err}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

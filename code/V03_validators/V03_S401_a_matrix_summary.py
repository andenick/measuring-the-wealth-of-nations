"""V03_S401 — Hawkins-Simon condition (max_eigenvalue < 1) at every benchmark."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


def run():
    df = pd.read_csv(DATA_FINAL / "S401.csv")
    # Hawkins-Simon: max eigenvalue must be < 1 for productive economy
    hs_ok = bool((df["max_eigenvalue"] < 1.0).all())
    # Sparsity in [0, 1]
    sp_ok = bool(df["sparsity"].between(0, 1).all())
    status = "PASS" if hs_ok and sp_ok else "FAIL"
    result = {
        "series_id": "S401",
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status": status,
        "n_pass": 1 if status == "PASS" else 0,
        "n_fail": 0 if status == "PASS" else 1,
        "n_missing": 0,
        "checks": {
            "hawkins_simon_all_lt_1": hs_ok,
            "max_eig_max": float(df["max_eigenvalue"].max()),
            "sparsity_in_unit_interval": sp_ok,
            "n_benchmark_years": len(df),
        },
    }
    write_validation_result("S401", result)
    print(f"    [V03_S401] status={status} HS_ok={hs_ok} max_eig_max={df['max_eigenvalue'].max():.6f}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

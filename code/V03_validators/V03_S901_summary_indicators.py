"""V03_S901 — Validate Summary Indicators round-trip against upstream series."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_validation_result  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S901"


def run():
    """For each populated column (S506, S511, S512, S608), verify the
    summary row matches the upstream source year-by-year (zero tolerance)."""
    s901 = pd.read_csv(DATA_FINAL / "S901.csv")

    # Pivot to wide format for easy comparison
    wide = s901.pivot_table(index="year", columns="series_id", values="value", aggfunc="first").reset_index()
    columns_to_check = {
        "S901-A/e_S506":     "S506",
        "S901-A/LpL_S511":   "S511",
        "S901-A/VW_S512":    "S512",
        "S901-A/NSW_V_S608": "S608",
    }
    fails = []
    compared = 0
    for s901_col, upstream_id in columns_to_check.items():
        if s901_col not in wide.columns:
            continue
        upstream = pd.read_csv(DATA_FINAL / f"{upstream_id}.csv")
        upstream = upstream[upstream["series_id"] == f"{upstream_id}-A"][["year", "value"]]
        merged = wide[["year", s901_col]].merge(upstream, on="year", how="inner")
        merged["abs_err"] = (merged[s901_col] - merged["value"]).abs()
        bad = merged[(merged["abs_err"] > 1e-9) & merged[s901_col].notna()]
        compared += len(merged)
        if len(bad) > 0:
            fails.append({"column": s901_col, "fail_years": bad["year"].tolist(),
                          "max_abs_err": float(bad["abs_err"].max())})

    n_total_rows = len(s901)
    n_pending = int(s901["value"].isna().sum())
    status = "PASS" if not fails else "FAIL"
    result = {
        "series_id":       SERIES_ID,
        "run_at":          datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tolerance_class": "rate_series",
        "status":          status,
        "n_pass":          1 if status == "PASS" else 0,
        "n_fail":          len(fails),
        "n_missing":       0,
        "round_trip_check": {
            "compared_pairs":     compared,
            "fails":              fails,
            "rows_pending_K_TCU": n_pending,
            "rows_total":         n_total_rows,
        },
    }
    write_validation_result(SERIES_ID, result)
    print(f"    [V03_{SERIES_ID}] status={status} round_trip_pairs={compared} pending={n_pending}/{n_total_rows}")
    return result


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "PASS" else 1)

"""P02_S901 — Compute Chapter 9 Summary Indicators table.

The book's Table 9.1 / Figure 9.1 aggregates the headline Marxian ratios into
one summary view across the full book period. The new build computes this
table by merging the already-validated Ch5 ratio series:

  year, S506 (exploitation rate), S511 (productive labor share),
        S512 (productive wage share), S513 (Marxian profit rate*),
        S514 (capacity-adjusted profit rate*), S608 (NSW/V* ratio)

*S513 and S514 are PENDING (need K* and TCU); columns are written as
NaN in their slots and the DPR documents the pending status.

No L01 loader — purely composable from data/final/ of upstream series.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "S901"
SUBSERIES = "S901-A"


def _load_series(sid: str, col_name: str) -> pd.DataFrame:
    path = DATA_FINAL / f"{sid}.csv"
    if not path.exists():
        return pd.DataFrame(columns=["year", col_name])
    df = pd.read_csv(path)
    df = df[df["series_id"] == f"{sid}-A"][["year", "value"]].rename(columns={"value": col_name})
    return df


def compute() -> pd.DataFrame:
    """Compose the long-form summary table from upstream series."""
    parts = {
        "e_S506":     _load_series("S506", "e_S506"),
        "LpL_S511":   _load_series("S511", "LpL_S511"),
        "VW_S512":    _load_series("S512", "VW_S512"),
        "NSW_V_S608": _load_series("S608", "NSW_V_S608"),
    }
    merged = parts["e_S506"]
    for col, df in parts.items():
        if col == "e_S506":
            continue
        merged = merged.merge(df, on="year", how="outer")
    # S513, S514 pending — placeholder columns explicit-NaN (not synthesized)
    merged["r_S513"]     = float("nan")
    merged["r_adj_S514"] = float("nan")
    merged = merged.sort_values("year").reset_index(drop=True)

    # Reshape to long format consistent with all other series
    out_rows = []
    for _, row in merged.iterrows():
        for col in ("e_S506", "LpL_S511", "VW_S512", "NSW_V_S608", "r_S513", "r_adj_S514"):
            out_rows.append({
                "series_id": f"{SUBSERIES}/{col}",
                "year":      int(row["year"]),
                "value":     row[col],
                "units":     "ratio" if col != "r_S513" and col != "r_adj_S514" else "rate",
                "stage":     "summary_aggregation",
                "provenance": f"merged from final/{col.split('_')[-1]}.csv" if "S" in col else "pending_K_TCU",
            })
    return pd.DataFrame(out_rows)


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    n_with_data = df["value"].notna().sum()
    n_total     = len(df)
    print(f"    [P02_{SERIES_ID}] {n_total} rows ({n_with_data} with values, "
          f"{n_total - n_with_data} pending K*/TCU); wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

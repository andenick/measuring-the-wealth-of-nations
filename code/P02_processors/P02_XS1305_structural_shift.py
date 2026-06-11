"""P02_XS1305 — Post-2000 Structural Shift Indicator (Moos 2017).

Moos identifies a post-2000 break in NSW/GDP — the trend accelerates
upward as transfer programs expand faster than labor-tax base.
Indicator: rolling 5-year average of NSW/GDP delta from pre-2000 average.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS1305"
SUBSERIES = "XS1305-A"


def compute() -> pd.DataFrame:
    es1301 = pd.read_csv(DATA_FINAL / "XS1301.csv")
    es1301 = es1301[es1301["series_id"] == "XS1301-A"][["year", "value"]].rename(columns={"value": "NSW_GDP"})
    es1301 = es1301.sort_values("year").reset_index(drop=True)
    # Pre-2000 baseline: average 1980-1999
    pre2000 = es1301[(es1301["year"] >= 1980) & (es1301["year"] <= 1999)]["NSW_GDP"].mean()
    es1301["value"] = es1301["NSW_GDP"] - pre2000
    es1301["series_id"] = SUBSERIES
    es1301["units"] = "share_delta"
    es1301["stage"] = "structural_break_detection"
    es1301["provenance"] = f"XS1301 - mean(XS1301[1980-1999]={pre2000:.4f})"
    return es1301[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_XS1305] {len(df)} rows; post-2000 delta range=[{df[df['year']>=2000]['value'].min():.4f}, {df[df['year']>=2000]['value'].max():.4f}]; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

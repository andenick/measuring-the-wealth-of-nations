"""P02_XS1304 — Moos vs ST NSW/GDP comparison at overlap years 1959-1997.

The Moos vs ST delta isolates the effect of his slightly different
unproductive-sector boundary on the NSW finding.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402


SERIES_ID = "XS1304"
SUBSERIES = "XS1304-A"


def compute() -> pd.DataFrame:
    es1201 = pd.read_csv(DATA_FINAL / "XS1201.csv")
    es1201 = es1201[es1201["series_id"] == "XS1201-A"][["year", "value"]].rename(columns={"value": "ST_NSW_GDP"})
    es1301 = pd.read_csv(DATA_FINAL / "XS1301.csv")
    es1301 = es1301[es1301["series_id"] == "XS1301-A"][["year", "value"]].rename(columns={"value": "Moos_NSW_GDP"})
    merged = es1201.merge(es1301, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["Moos_NSW_GDP"] - merged["ST_NSW_GDP"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "cross_study_delta"
    merged["provenance"] = "XS1301 - XS1201"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_XS1304] {len(df)} overlap years; delta range=[{df['value'].min():.4f}, {df['value'].max():.4f}]; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

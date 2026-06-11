"""P02_XS1202 — NSW / Employee Compensation (ST 2002) using S607 + cached NIPA T20100."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL, ROOT  # noqa: E402


SERIES_ID = "XS1202"
SUBSERIES = "XS1202-A"


def compute() -> pd.DataFrame:
    ec_path = ROOT / "data" / "raw" / "bea" / "nipa_T20100_compensation_1929_2025.csv"
    ec = pd.read_csv(ec_path)
    ec["EC_billions"] = ec["compensation_millions"] / 1000.0
    ec = ec[["year", "EC_billions"]].rename(columns={"EC_billions": "EC"})

    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s607 = s607[s607["series_id"] == "S607-COMBINED"][["year", "value"]].rename(columns={"value": "NSW"})

    merged = s607.merge(ec, on="year", how="inner").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["NSW"] / merged["EC"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "derived"
    merged["provenance"] = "S607-COMBINED / NIPA T20100 compensation"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    v_1952 = float(df[df["year"] == 1952]["value"].iloc[0]) if (df["year"] == 1952).any() else None
    v_1997 = float(df[df["year"] == 1997]["value"].iloc[0]) if (df["year"] == 1997).any() else None
    print(f"    [P02_XS1202] {len(df)} rows; NSW/EC: 1952={v_1952:.4f}, 1997={v_1997:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

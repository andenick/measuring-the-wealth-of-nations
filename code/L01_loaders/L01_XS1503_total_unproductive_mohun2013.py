"""L01_XS1503 — Load Mohun (2013) TOTAL unproductive EMPLOYMENT SHARE.

D4 REBUILD (2026-07-02): rebuilt from Mohun's ACTUAL published estimates.
Source: mohun_2013_published_shares.csv (Mohun 2013, RRPE 46(3), pub 2014, Figure 1).
Total unproductive labour, share of total employment at benchmark years:
1964 = 42.0%, peak 2003 = 49.0%, 2010 = 47.5% (text-reported figure anchors,
table/text-grade). Decomposition identity XS1501-A + XS1502-A == XS1503-A holds at
the overlapping benchmark year 1964: 0.251 + 0.168 = 0.419 vs Mohun's stated 0.420
(0.1pp figure-rounding). Annual fill is figure-grade -> deferred to G2.

Prior 1948-1989 FTE-level Lu_mohun series was a mislabeled predecessor-build decomposition
(DIV-050); retained as a labeled variant arm under chopped/_variants_predecessor-build/.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES

SERIES_ID = "XS1503"
SUBSERIES = "XS1503-A"
SOURCE = EXTERNAL_STUDIES / "mohun_2013_published_shares.csv"


def load() -> pd.DataFrame:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source data missing: {SOURCE}")
    df = pd.read_csv(SOURCE)
    df = df[df["series_id"] == SUBSERIES].copy()
    df["year"] = df["year"].astype(int)
    df["value"] = df["value"].astype(float)
    df["units"] = "share"
    return df[["series_id", "year", "value", "units"]].reset_index(drop=True)


LOADER = load


def run() -> pd.DataFrame:
    df = load()
    print(f"    [L01_XS1503] loaded {len(df)} Mohun-2013 benchmark shares; "
          f"years={list(df['year'])}; first={df.iloc[0]['value']:.3f}")
    return df


if __name__ == "__main__":
    run()

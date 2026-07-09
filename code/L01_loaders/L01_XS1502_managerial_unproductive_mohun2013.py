"""L01_XS1502 — Load Mohun (2013) supervisory EMPLOYMENT SHARE.

D4 REBUILD (2026-07-02): rebuilt from Mohun's ACTUAL published estimates.
Source: mohun_2013_published_shares.csv (Mohun 2013, RRPE 46(3), pub 2014, Figure 3).
Supervisory = managers-plus-capitalists, share of total employment at benchmark
years: 1964 = 16.8%, peak 1991 = 19.9%, 2010 = 17.9% (text-reported figure anchors,
table/text-grade). Annual fill is figure-grade -> deferred to G2.

Prior 1948-1989 FTE-level Lum_mohun series was a mislabeled predecessor-build decomposition
(DIV-050); retained as a labeled variant arm under chopped/_variants_predecessor-build/.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES

SERIES_ID = "XS1502"
SUBSERIES = "XS1502-A"
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
    print(f"    [L01_XS1502] loaded {len(df)} Mohun-2013 benchmark shares; "
          f"years={list(df['year'])}; first={df.iloc[0]['value']:.3f}")
    return df


if __name__ == "__main__":
    run()

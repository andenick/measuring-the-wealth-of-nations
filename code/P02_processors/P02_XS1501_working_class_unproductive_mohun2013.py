"""P02_XS1501 — Mohun (2013) unproductive working-class employment share.

D4 REBUILD (2026-07-02): pass-through of Mohun's published benchmark shares
(Figure 2). Emits data/final/XS1501.csv as SHARE of total employment over
Mohun's 1964-2010 span (benchmark anchors 1964=0.251, 2007=0.300).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_XS1501_working_class_unproductive_mohun2013 import load  # noqa: E402
from utils.io import write_series_csv  # noqa: E402

PROV = "Mohun 2013 (RRPE 46(3), pub 2014), Figure 2 (p.10/364); mohun_2013_published_shares.csv"


def run():
    df = load()
    df["stage"] = "study_period"
    df["provenance"] = PROV
    df = df[["series_id", "year", "value", "units", "stage", "provenance"]]
    write_series_csv(df, "XS1501", stage="intermediate")
    final_path = write_series_csv(df, "XS1501", stage="final")
    print(f"    [P02_XS1501] {len(df)} benchmark rows; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

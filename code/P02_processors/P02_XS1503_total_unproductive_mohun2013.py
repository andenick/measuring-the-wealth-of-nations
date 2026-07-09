"""P02_XS1503 — Mohun (2013) total unproductive employment share (identity anchor).

D4 REBUILD (2026-07-02): pass-through of Mohun's published benchmark shares
(Figure 1). Emits data/final/XS1503.csv as SHARE of total employment over
Mohun's 1964-2010 span (benchmark anchors 1964=0.420, 2003=0.490, 2010=0.475).
Decomposition identity XS1501-A + XS1502-A == XS1503-A verified at the
overlapping benchmark year 1964 (0.251+0.168=0.419 vs 0.420, 0.1pp fig-rounding).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_XS1503_total_unproductive_mohun2013 import load  # noqa: E402
from utils.io import write_series_csv  # noqa: E402

PROV = "Mohun 2013 (RRPE 46(3), pub 2014), Figure 1 (p.7/361); mohun_2013_published_shares.csv"


def run():
    df = load()
    df["stage"] = "study_period"
    df["provenance"] = PROV
    df = df[["series_id", "year", "value", "units", "stage", "provenance"]]
    write_series_csv(df, "XS1503", stage="intermediate")
    final_path = write_series_csv(df, "XS1503", stage="final")
    print(f"    [P02_XS1503] {len(df)} benchmark rows; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

"""P02_XS1504 — Mohun (2013) unproductive burden ratio Lu/Lp (ST/Mohun comparison).

D4 REBUILD (2026-07-02). Rebuilt from Mohun's OWN published unproductive-employment
shares (XS1503, Figure 1) over his 1964-2010 span:

    Lu/Lp = s_u / (1 - s_u)         where s_u = total unproductive employment share

Benchmark values (Mohun's actual estimates, table/text-grade):
    1964: 0.420/0.580 = 0.7241
    2003: 0.490/0.510 = 0.9608   (peak)
    2010: 0.475/0.525 = 0.9048

ST/MOHUN COMPARISON (the point of this series): the retired 1948-1989 ST-method
(predecessor-build) backward decomposition gives Lu/Lp(1964) = 0.8085 -- i.e. predecessor-build classifies more
employment as unproductive than Mohun (predecessor-build Lu/L=44.7% vs Mohun 42.0%), so the predecessor-build
burden ratio runs ~+11.7% above Mohun's at the one overlapping benchmark year.
This divergence is registered (DIV-058) and is the honest replacement for the old
Lu/Lp series, whose 2010 refval (0.96) was mis-derived from the 2003 PEAK share and
was structurally unreachable by 1948-1989 data (DIV-051, now superseded).

Prior series used the predecessor-build CSV; that arm is retained under chopped/_variants_predecessor-build/.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import write_series_csv  # noqa: E402
from utils.paths import DATA_FINAL  # noqa: E402

SERIES_ID = "XS1504"
SUBSERIES = "XS1504-A"
PROV = "derived: Mohun 2013 unproductive employment share s_u (XS1503) -> Lu/Lp = s_u/(1-s_u)"


def compute() -> pd.DataFrame:
    s = pd.read_csv(DATA_FINAL / "XS1503.csv")
    s = s[s["series_id"] == "XS1503-A"][["year", "value"]].rename(columns={"value": "s_u"})
    s = s.sort_values("year").reset_index(drop=True)
    s["value"] = s["s_u"] / (1.0 - s["s_u"])
    s["series_id"] = SUBSERIES
    s["units"] = "ratio"
    s["stage"] = "analytical_derivation"
    s["provenance"] = PROV
    return s[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_XS1504] {len(df)} benchmark rows; "
          f"1964={df[df.year==1964]['value'].iloc[0]:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

"""P02_S608 — Net transfer normalized against variable capital (book Table N.2).

REVIEW 2026-07 (workpackage B) REBUILD. Previously S608 = NSW / V* (S607 / S504) directly,
which is NOT a quantity the book publishes and whose registry benchmarks failed 5/5.

Shaikh & Tonak (1994) Appendix N, Table N.2 normalizes the net transfer against
variable capital via:
    Ntrrate = net transfer rate  = (B1 - T1) / EC          (our reconstruction: NSW / EC = S607 / S617)
    NtrV*   = net transfer out of V* = (Ntrrate) * V*        (Table N.2 row "NtrV* = (Ntrrate)V*")
    S608    = NtrV* / V*  ==  Ntrrate                         (the book's normalized net-transfer measure)

We take the DIRECT Ntrrate / NtrV* row of Table N.2 as the reference (see V03),
NOT the reverse-engineered adjusted-vs-unadjusted rate-of-surplus-value chain
(S*/V* unadjusted vs S**/V** adjusted) that the superseded back-solve used.

The intermediate NtrV* (a dollar magnitude) is recorded in the provenance string
so the book construction is explicit even though S608 algebraically reduces to
Ntrrate = NSW/EC (V* cancels).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import DATA_FINAL  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S608"
SUBSERIES = "S608-A"


def compute() -> pd.DataFrame:
    s607 = pd.read_csv(DATA_FINAL / "S607.csv")
    s504 = pd.read_csv(DATA_FINAL / "S504.csv")
    s617 = pd.read_csv(DATA_FINAL / "S617.csv")
    s607 = s607[s607["series_id"] == "S607-A"][["year", "value"]].rename(columns={"value": "NSW"})
    s504 = s504[s504["series_id"] == "S504-A"][["year", "value"]].rename(columns={"value": "V_star"})
    s617 = s617[s617["series_id"] == "S617-A"][["year", "value"]].rename(columns={"value": "EC"})

    merged = (
        s607.merge(s504, on="year").merge(s617, on="year")
        .sort_values("year").reset_index(drop=True)
    )
    # Book Table N.2 construction.
    merged["Ntrrate"] = merged["NSW"] / merged["EC"]          # net transfer rate = (B1-T1)/EC
    merged["NtrV_star"] = merged["Ntrrate"] * merged["V_star"]  # NtrV* = (Ntrrate) V*
    merged["value"] = merged["NtrV_star"] / merged["V_star"]    # S608 = NtrV*/V* == Ntrrate
    merged["series_id"] = SUBSERIES
    merged["units"] = "ratio"
    merged["stage"] = "book_period"
    merged["provenance"] = (
        "NtrV*/V* per book Table N.2; NtrV* = (Ntrrate)V*, Ntrrate = NSW/EC = S607/S617; V* = S504"
    )
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

"""P02_S607 — Process NSW: emit S607-A (book), S607-EXT (extension), S607-COMBINED.

The extension uses identical methodology (same NIPA tables, same productive/
unproductive partition) so the splice is `direct` — no rebase. Verify the
1989 overlap exists in A but not EXT (EXT starts 1990 by design).

Naming note: legacy code used `S607-B` for the extension subseries. Renamed
to `S607-EXT` per the project extension-subseries convention (Decision 0003) during
2026-05-23 Stage 5 cohort 2.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S607_net_social_wage import LOADER_A, LOADER_EXT  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S607"


def _annotate(df: pd.DataFrame, subseries_id: str, source: str, stage: str) -> pd.DataFrame:
    df = df.copy()
    df["series_id"]  = subseries_id
    df["stage"]      = stage
    df["provenance"] = source
    return df[["series_id", "year", "value", "units", "stage", "provenance"]]


def run():
    df_a_raw   = LOADER_A.load()
    df_ext_raw = LOADER_EXT.load()
    df_ext_raw = df_ext_raw[df_ext_raw["year"] >= 1990].copy()

    df_a   = _annotate(df_a_raw,   "S607-A",   "Table6_3_NetSocialWage.csv:nsw", "book_period")
    df_ext = _annotate(df_ext_raw, "S607-EXT", "Table6_3_Extended.csv:nsw",      "extension")

    # COMBINED concatenation
    combined_raw = pd.concat([df_a_raw, df_ext_raw], ignore_index=True).sort_values("year").reset_index(drop=True)
    df_combined = _annotate(combined_raw, "S607-COMBINED", "splice(S607-A through 1989, S607-EXT from 1990)", "")
    df_combined["stage"] = df_combined.apply(
        lambda r: "book_period" if r["year"] <= 1989 else "extension", axis=1
    )

    final = pd.concat([df_a, df_ext, df_combined], ignore_index=True)
    write_series_csv(final, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(final, SERIES_ID, stage="final")

    first_pos = combined_raw[combined_raw["value"] > 0]["year"].min()
    print(f"    [P02_S607] {len(final)} rows ({len(df_a)} A + {len(df_ext)} EXT + {len(df_combined)} COMBINED); "
          f"COMBINED span {df_combined['year'].min()}-{df_combined['year'].max()}; "
          f"NSW first POSITIVE year: {int(first_pos) if not pd.isna(first_pos) else 'none'}")
    return final


if __name__ == "__main__":
    run()

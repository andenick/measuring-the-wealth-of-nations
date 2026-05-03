#!/usr/bin/env python3
"""L09 - Load Net Social Wage: T607, T608, T609.

Inputs:
  - ch06/Table6_3_NetSocialWage.csv (Format C, 1952-1989)
  - ch06/Table6_3_Extended.csv (Format C, 1952-2025) — if available
Column map: T607←nsw (÷1000), T609←nsw_ni_share
Note:    T608 (NSW/V*) is derived in P11, not loaded here.
Outputs: parsed-raw/T607_parsed.csv, T609_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T607", "T608", "T609"]


def load():
    """Load NSW data, converting millions→billions for T607."""
    ensure_dirs()
    outputs = []

    # Try extended first, fall back to book
    ext_src = ST_CHOPPED / "ch06" / "Table6_3_Extended.csv"
    book_src = ST_CHOPPED / "ch06" / "Table6_3_NetSocialWage.csv"

    source = ext_src if ext_src.exists() else book_src
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source, columns=["nsw", "nsw_ni_share"])

    # T607: NSW in billions
    if "nsw" in df.columns:
        out = df[["nsw"]].rename(columns={"nsw": "value"}).dropna()
        out["value"] = out["value"] / 1000.0  # millions → billions
        out_path = PARSED_RAW / "T607_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L09] T607: {len(out)} rows (NSW ÷1000 → billions)")

    # T609: NSW/NI share (already a ratio)
    if "nsw_ni_share" in df.columns:
        out = df[["nsw_ni_share"]].rename(columns={"nsw_ni_share": "value"}).dropna()
        out_path = PARSED_RAW / "T609_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L09] T609: {len(out)} rows (NSW/NI share)")

    # T608 (NSW/V*) will be computed in P11, not loaded here
    print("    [L09] T608: derived in P11 (NSW/V*)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"NSW | {len(outputs)} files loaded, T608 deferred to P11",
        "outputs": outputs,
    }

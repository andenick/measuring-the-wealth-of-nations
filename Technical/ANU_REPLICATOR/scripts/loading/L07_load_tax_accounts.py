#!/usr/bin/env python3
"""L07 - Load Tax Accounts: T601, T602, T603, T604.

Input:   ch06/Table6_1_TaxAccounts.csv (Format C, 1952-1989)
Column map: T601←personal_income_tax_workers, T602←social_insurance_workers,
            T603←property_tax_workers, T604←total_tax_workers
Units:   All values ÷1000 for billions.
Outputs: parsed-raw/T601_parsed.csv .. T604_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from lib.data_io import load_chopped_direct

SERIES_IDS = ["T601", "T602", "T603", "T604"]

COLUMN_MAP = {
    "T601": "personal_income_tax_workers",
    "T602": "social_insurance_workers",
    "T603": "property_tax_workers",
    "T604": "total_tax_workers",
}


def load():
    """Load tax accounts, converting millions→billions."""
    ensure_dirs()

    source = ST_CHOPPED / "ch06" / "Table6_1_TaxAccounts.csv"
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source, columns=list(COLUMN_MAP.values()))
    outputs = []

    for sid, col in COLUMN_MAP.items():
        if col not in df.columns:
            print(f"    [L07] {sid}: column {col} not found")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        out["value"] = out["value"] / 1000.0  # millions → billions
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L07] {sid}: {len(out)} rows (÷1000 → billions)")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Tax accounts | {len(outputs)} series, 1952-1989",
        "outputs": outputs,
    }

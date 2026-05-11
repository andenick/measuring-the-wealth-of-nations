#!/usr/bin/env python3
"""L08 - Load Benefits: T605, T606.

Book period:  ch06/Table6_2_BenefitAccounts.csv (Format C, 1952-1989)
Extension:    BEA NIPA 2.1 (social benefits) and 3.1 (govt consumption)

Column map: T605←total_benefits (÷1000), T606←govt_services_workers (÷1000)
Outputs: parsed-raw/T605_parsed.csv, T606_parsed.csv,
         parsed-raw/T605_ext_parsed.csv, T606_ext_parsed.csv
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.paths import ST_CHOPPED, PARSED_RAW, API_DATA, ensure_dirs
from lib.data_io import load_chopped_direct
from lib.api_data_io import load_bea_nipa

import pandas as pd

SERIES_IDS = ["T605", "T606"]

COLUMN_MAP = {
    "T605": "total_benefits",
    "T606": "govt_services_workers",
}


def load():
    """Load benefit accounts (book + BEA extension), converting millions->billions."""
    ensure_dirs()

    # --- Book period (1952-1989) ---
    source = ST_CHOPPED / "ch06" / "Table6_2_BenefitAccounts.csv"
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source, columns=list(COLUMN_MAP.values()))
    outputs = []

    for sid, col in COLUMN_MAP.items():
        if col not in df.columns:
            print(f"    [L08] {sid}: column {col} not found")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        out["value"] = out["value"] / 1000.0  # millions -> billions
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L08] {sid}: {len(out)} rows (book, ÷1000 -> billions)")

    # --- Extension period (1990-2025) from BEA NIPA ---

    # T605 extension: NIPA 2.1 "Government social benefits to persons"
    # This line matches T605 exactly at 1989 (521.070 billion)
    nipa_2_1_path = API_DATA / "BEA" / "nipa_2_1_personal_income.csv"
    if nipa_2_1_path.exists():
        benefits = load_bea_nipa(nipa_2_1_path,
                                 line_filter="Government social benefits to persons")
        benefits_s = benefits.iloc[:, 0] / 1e9  # scale to billions
        ext_605 = benefits_s[benefits_s.index > 1989].copy()
        ext_605.name = "value"
        ext_out = pd.DataFrame({"value": ext_605})
        ext_out.index.name = "year"
        ext_path = PARSED_RAW / "T605_ext_parsed.csv"
        ext_out.to_csv(ext_path)
        outputs.append(str(ext_path))
        print(f"    [L08] T605 ext: {len(ext_605)} rows (1990-{ext_605.index.max()}, NIPA 2.1)")
    else:
        print("    [L08] T605 ext: NIPA 2.1 not found, skipping extension")

    # T606 extension: NIPA 3.1 "Consumption expenditures" × worker allocation ratio
    # Worker allocation ratio: T606_book[1989] / NIPA_3.1[1989] = 494.803 / 881.429 = 0.5614
    nipa_3_1_path = API_DATA / "BEA" / "nipa_3_1_govt_receipts_expenditures.csv"
    if nipa_3_1_path.exists():
        govt_cons = load_bea_nipa(nipa_3_1_path,
                                  line_filter="Consumption expenditures")
        govt_s = govt_cons.iloc[:, 0] / 1e9  # scale to billions

        # Compute worker allocation ratio from 1989 splice point
        book_606 = df[["govt_services_workers"]].dropna()
        book_606["value"] = book_606["govt_services_workers"] / 1000.0
        if 1989 in book_606.index and 1989 in govt_s.index:
            worker_ratio = book_606.loc[1989, "value"] / govt_s[1989]
            ext_606 = (govt_s[govt_s.index > 1989] * worker_ratio).copy()
            ext_606.name = "value"
            ext_out = pd.DataFrame({"value": ext_606})
            ext_out.index.name = "year"
            ext_path = PARSED_RAW / "T606_ext_parsed.csv"
            ext_out.to_csv(ext_path)
            outputs.append(str(ext_path))
            print(f"    [L08] T606 ext: {len(ext_606)} rows (worker ratio={worker_ratio:.4f}, NIPA 3.1)")
        else:
            print("    [L08] T606 ext: cannot compute worker ratio (1989 missing)")
    else:
        print("    [L08] T606 ext: NIPA 3.1 not found, skipping extension")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Benefits | {len(outputs)} files, book + extension",
        "outputs": outputs,
    }

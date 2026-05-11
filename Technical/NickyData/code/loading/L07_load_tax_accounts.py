#!/usr/bin/env python3
"""L07 - Load Tax Accounts: T601, T602, T603, T604.

Input:   ch06/Table6_1_TaxAccounts.csv (Format C, 1952-1989)
         BEA NIPA 3.1 for extension (1990-2025)
Column map: T601←personal_income_tax_workers, T602←social_insurance_workers,
            T603←sales_excise_tax_workers+property_tax_workers, T604←total_tax_workers
Extension: T601←NIPA personal taxes × (EC/PI), T602←NIPA social insurance,
           T603←NIPA taxes on production × worker_ratio, T604←sum
Units:   All values ÷1000 for billions.
Outputs: parsed-raw/T601-T604_parsed.csv + T601-T604_ext_parsed.csv
Dependencies: None (extension uses NIPA 3.1 + 2.1)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import ST_CHOPPED, PARSED_RAW, API_DATA, ensure_dirs
from utils.data_io import load_chopped_direct
from utils.api_data_io import load_bea_nipa

SERIES_IDS = ["T601", "T602", "T603", "T604"]

COLUMN_MAP = {
    "T601": "personal_income_tax_workers",
    "T602": "social_insurance_workers",
    "T604": "total_tax_workers",
}

# T603 = indirect taxes = sales_excise + property (both components)
T603_COLUMNS = ["sales_excise_tax_workers", "property_tax_workers"]


def load():
    """Load tax accounts, converting millions->billions."""
    ensure_dirs()

    source = ST_CHOPPED / "ch06" / "Table6_1_TaxAccounts.csv"
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    all_cols = list(COLUMN_MAP.values()) + T603_COLUMNS
    df = load_chopped_direct(source, columns=all_cols)
    outputs = []

    for sid, col in COLUMN_MAP.items():
        if col not in df.columns:
            print(f"    [L07] {sid}: column {col} not found")
            continue
        out = df[[col]].rename(columns={col: "value"}).dropna()
        out["value"] = out["value"] / 1000.0  # millions -> billions
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L07] {sid}: {len(out)} rows (÷1000 -> billions)")

    # T603: indirect taxes = sales_excise + property (sum of two components)
    if all(c in df.columns for c in T603_COLUMNS):
        t603_val = df[T603_COLUMNS].sum(axis=1).dropna()
        out = t603_val.to_frame(name="value")
        out["value"] = out["value"] / 1000.0  # millions -> billions
        out_path = PARSED_RAW / "T603_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L07] T603: {len(out)} rows (sales_excise + property, ÷1000 -> billions)")

    # --- Extension via NIPA 3.1 (1990-2025) ---
    nipa_31_path = API_DATA / "BEA" / "nipa_3_1_govt_receipts_expenditures.csv"
    nipa_21_path = API_DATA / "BEA" / "nipa_2_1_personal_income.csv"

    if nipa_31_path.exists() and nipa_21_path.exists():
        # Load NIPA components
        personal_taxes = load_bea_nipa(nipa_31_path, line_filter="Personal current taxes")
        social_ins = load_bea_nipa(nipa_31_path, line_filter="Contributions for government social insurance")
        indirect_taxes = load_bea_nipa(nipa_31_path, line_filter="Taxes on production and imports")

        pt = personal_taxes.iloc[:, 0] / 1e9  # dollars -> billions
        si = social_ins.iloc[:, 0] / 1e9
        it = indirect_taxes.iloc[:, 0] / 1e9

        # Worker allocation: EC/PI from NIPA 2.1
        ec_df = load_bea_nipa(nipa_21_path, line_filter="Compensation of employees")
        pi_df = load_bea_nipa(nipa_21_path, line_filter="Personal income")
        ec = ec_df.iloc[:, 0] / 1e9 if len(ec_df.columns) > 0 else None
        pi = pi_df.iloc[:, 0] / 1e9 if len(pi_df.columns) > 0 else None

        ext_years_idx = pt.index[pt.index > 1989]

        if ec is not None and pi is not None:
            labor_share = ec / pi  # EC/PI ≈ 0.55-0.65

            # T601 ext: personal taxes × labor share
            common_601 = ext_years_idx.intersection(labor_share.index)
            t601_ext = pt[common_601] * labor_share[common_601]
            ext_out = pd.DataFrame({"value": t601_ext})
            ext_out.index.name = "year"
            ext_out.to_csv(PARSED_RAW / "T601_ext_parsed.csv")
            outputs.append(str(PARSED_RAW / "T601_ext_parsed.csv"))
            print(f"    [L07] T601 ext: {len(t601_ext)} rows (NIPA personal taxes × EC/PI)")

        # T602 ext: social insurance (directly attributable to workers)
        t602_ext = si[ext_years_idx]
        ext_out = pd.DataFrame({"value": t602_ext})
        ext_out.index.name = "year"
        ext_out.to_csv(PARSED_RAW / "T602_ext_parsed.csv")
        outputs.append(str(PARSED_RAW / "T602_ext_parsed.csv"))
        print(f"    [L07] T602 ext: {len(t602_ext)} rows (NIPA social insurance)")

        # T603 ext: indirect taxes × worker consumption share (frozen at 1989 book ratio)
        t603_book = pd.read_csv(PARSED_RAW / "T603_parsed.csv", index_col=0)["value"] if (PARSED_RAW / "T603_parsed.csv").exists() else None
        t604_book = pd.read_csv(PARSED_RAW / "T604_parsed.csv", index_col=0)["value"] if (PARSED_RAW / "T604_parsed.csv").exists() else None
        if t603_book is not None and t604_book is not None and 1989 in t603_book.index and 1989 in t604_book.index:
            indirect_share = t603_book[1989] / t604_book[1989]  # ~0.31 at 1989
            t603_ext = it[ext_years_idx] * indirect_share
            ext_out = pd.DataFrame({"value": t603_ext})
            ext_out.index.name = "year"
            ext_out.to_csv(PARSED_RAW / "T603_ext_parsed.csv")
            outputs.append(str(PARSED_RAW / "T603_ext_parsed.csv"))
            print(f"    [L07] T603 ext: {len(t603_ext)} rows (NIPA indirect × {indirect_share:.3f})")

            # T604 ext: T601 + T602 + T603 (identity by construction)
            if ec is not None and pi is not None:
                common_all = t601_ext.index.intersection(t602_ext.index).intersection(t603_ext.index)
                t604_ext = t601_ext[common_all] + t602_ext[common_all] + t603_ext[common_all]
                ext_out = pd.DataFrame({"value": t604_ext})
                ext_out.index.name = "year"
                ext_out.to_csv(PARSED_RAW / "T604_ext_parsed.csv")
                outputs.append(str(PARSED_RAW / "T604_ext_parsed.csv"))
                print(f"    [L07] T604 ext: {len(t604_ext)} rows (sum of components)")
    else:
        print("    [L07] Tax extension: NIPA 3.1/2.1 not found, book only")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Tax accounts | {len(outputs)} files, 1952-2025",
        "outputs": outputs,
    }

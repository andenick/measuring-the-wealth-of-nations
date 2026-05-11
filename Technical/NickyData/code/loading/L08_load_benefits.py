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

from utils.paths import ST_CHOPPED, PARSED_RAW, API_DATA, ensure_dirs
from utils.data_io import load_chopped_direct
from utils.api_data_io import load_bea_nipa

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

    # T606 extension: Appendix N 3-group methodology (Step 4, KB deep dive)
    # Group I (100% to workers): income_security
    # Group II (x labor_share): education, health, transportation
    # Group III (0%): national_defense, public_order_safety
    # Labor share = EC/PI from NIPA 2.1 (varies annually)
    govt_func_path = PARSED_RAW / "moos_govt_consumption.csv"
    nipa_2_1_path = API_DATA / "BEA" / "nipa_2_1_personal_income.csv"

    if govt_func_path.exists() and nipa_2_1_path.exists():
        gf = pd.read_csv(govt_func_path, index_col="year")

        ec_df = load_bea_nipa(nipa_2_1_path, line_filter="Compensation of employees")
        pi_df = load_bea_nipa(nipa_2_1_path, line_filter="Personal income")
        ec = ec_df.iloc[:, 0] / 1e9 if len(ec_df.columns) > 0 else pd.Series(dtype=float)
        pi = pi_df.iloc[:, 0] / 1e9 if len(pi_df.columns) > 0 else pd.Series(dtype=float)

        common_ls = ec.index.intersection(pi.index)
        labor_share = ec[common_ls] / pi[common_ls]

        ext_yrs = gf.index[gf.index > 1989]
        if len(ext_yrs) > 0:
            ext_606 = pd.Series(0.0, index=ext_yrs)
            for yr in ext_yrs:
                ls = labor_share.get(yr, 0.60)
                # Group I: 100% (income_security)
                g1 = gf.loc[yr, "income_security"] / 1e9 if "income_security" in gf.columns else 0
                # Group II: education + health + transportation, x labor_share
                g2 = 0.0
                for col in ["education", "health", "transportation"]:
                    if col in gf.columns:
                        g2 += gf.loc[yr, col] / 1e9
                g2 *= ls
                # Group III: 0% (defense, public_order_safety) - excluded
                ext_606[yr] = g1 + g2

            ext_606.name = "value"
            ext_out = pd.DataFrame({"value": ext_606})
            ext_out.index.name = "year"
            ext_path = PARSED_RAW / "T606_ext_parsed.csv"
            ext_out.to_csv(ext_path)
            outputs.append(str(ext_path))
            mean_ls = labor_share[labor_share.index > 1989].mean()
            print(f"    [L08] T606 ext: {len(ext_606)} rows (Appendix N 3-group, mean labor_share={mean_ls:.3f})")
        else:
            print("    [L08] T606 ext: no years > 1989 in govt function data")
    else:
        # Fallback to old 40% defense exclusion method
        fed_path = API_DATA / "BEA" / "nipa_3_2_federal_govt.csv"
        sl_path = API_DATA / "BEA" / "nipa_3_3_state_local_govt.csv"
        if fed_path.exists() and sl_path.exists():
            fed_cons = load_bea_nipa(fed_path, line_filter="Consumption expenditures")
            fed_s = fed_cons.iloc[:, 0] / 1e9
            sl_cons = load_bea_nipa(sl_path, line_filter="Consumption expenditures")
            sl_s = sl_cons.iloc[:, 0] / 1e9
            common_yrs = fed_s.index.intersection(sl_s.index)
            ext_yrs = common_yrs[common_yrs > 1989]
            if len(ext_yrs) > 0:
                ext_606 = 0.6 * fed_s[ext_yrs] + sl_s[ext_yrs]
                ext_606.name = "value"
                ext_out = pd.DataFrame({"value": ext_606})
                ext_out.index.name = "year"
                ext_path = PARSED_RAW / "T606_ext_parsed.csv"
                ext_out.to_csv(ext_path)
                outputs.append(str(ext_path))
                print(f"    [L08] T606 ext: {len(ext_606)} rows (FALLBACK: 40% defense exclusion)")
        else:
            print("    [L08] T606 ext: no NIPA data available")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Benefits | {len(outputs)} files, book + extension",
        "outputs": outputs,
    }

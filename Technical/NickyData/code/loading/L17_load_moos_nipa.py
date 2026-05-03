#!/usr/bin/env python3
"""L17 - Load BEA NIPA tables for independent Moos (2017) NSW derivation.

Parses the BEA NIPA CSV files downloaded from the API into structured
series that P21 can use to compute NSW independently.

Inputs:  Inputs/ExternalSources/Moos/bea_nipa_T*.csv
Outputs: data/raw-data/parsed/moos_*.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import PARSED_RAW, INPUTS, ensure_dirs

MOOS_DIR = INPUTS / "ExternalSources" / "Moos"


def _load_nipa_table(filename: str, lines: dict[str, int]) -> pd.DataFrame:
    """Load a BEA NIPA CSV and extract specific line numbers as named columns."""
    path = MOOS_DIR / filename
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["LineNumber"] = df["LineNumber"].astype(str).str.strip()
    df["TimePeriod"] = df["TimePeriod"].astype(int)
    df["DataValue"] = pd.to_numeric(
        df["DataValue"].astype(str).str.replace(",", ""), errors="coerce"
    )

    result = pd.DataFrame()
    for col_name, line_num in lines.items():
        mask = df["LineNumber"] == str(line_num)
        subset = df[mask].set_index("TimePeriod")["DataValue"].sort_index()
        result[col_name] = subset

    return result


def load():
    ensure_dirs()
    steps = []
    outputs = []

    # T20100 (Table 2.1): Personal Income and Its Disposition
    t21 = _load_nipa_table("bea_nipa_T20100_personal_income.csv", {
        "personal_income": 1,
        "employee_compensation": 2,
    })
    if not t21.empty:
        t21.index.name = "year"
        out = PARSED_RAW / "moos_personal_income.csv"
        t21.to_csv(out)
        outputs.append(str(out))
        steps.append(f"T2.1: {len(t21)} years (personal income, employee comp)")
        print(f"    [L17] T2.1: {len(t21)} years")

    # T10105 (Table 1.1.5): GDP
    t115 = _load_nipa_table("bea_nipa_T10105_gdp.csv", {
        "gdp": 1,
    })
    if not t115.empty:
        t115.index.name = "year"
        out = PARSED_RAW / "moos_gdp.csv"
        t115.to_csv(out)
        outputs.append(str(out))
        steps.append(f"T1.1.5: {len(t115)} years (GDP)")
        print(f"    [L17] T1.1.5: {len(t115)} years")

    # T31200 (Table 3.12): Government Social Benefits to Persons
    t312 = _load_nipa_table("bea_nipa_T31200_social_benefits.csv", {
        "total_social_benefits": 1,
        "social_security": 3,
        "medicare": 9,
        "medicaid": 10,
        "unemployment_insurance": 15,
        "other_social_benefits": 18,
    })
    if not t312.empty:
        t312.index.name = "year"
        out = PARSED_RAW / "moos_social_benefits.csv"
        t312.to_csv(out)
        outputs.append(str(out))
        steps.append(f"T3.12: {len(t312)} years (social benefits)")
        print(f"    [L17] T3.12: {len(t312)} years")

    # T31600 (Table 3.16): Govt Consumption Expenditures by Function
    t316 = _load_nipa_table("bea_nipa_T31600_govt_consumption_by_function.csv", {
        "total_govt_consumption": 1,
        "national_defense": 2,
        "education": 15,
        "health": 21,
        "income_security": 25,
        "transportation": 29,
        "public_order_safety": 33,
    })
    if not t316.empty:
        t316.index.name = "year"
        out = PARSED_RAW / "moos_govt_consumption.csv"
        t316.to_csv(out)
        outputs.append(str(out))
        steps.append(f"T3.16: {len(t316)} years (govt consumption by function)")
        print(f"    [L17] T3.16: {len(t316)} years")

    # T30700 (Table 3.7): Contributions for Government Social Insurance
    t37 = _load_nipa_table("bea_nipa_T30700_social_insurance_contributions.csv", {
        "total_social_insurance": 1,
        "federal_social_insurance": 2,
        "state_local_social_insurance": 11,
    })
    if not t37.empty:
        t37.index.name = "year"
        out = PARSED_RAW / "moos_social_insurance.csv"
        t37.to_csv(out)
        outputs.append(str(out))
        steps.append(f"T3.7: {len(t37)} years (social insurance contributions)")
        print(f"    [L17] T3.7: {len(t37)} years")

    # T30100 (Table 3.1): Govt Current Receipts and Expenditures
    t31 = _load_nipa_table("bea_nipa_T30100_govt_receipts_expenditures.csv", {
        "total_receipts": 1,
        "personal_current_taxes": 3,
        "total_expenditures": 19,
        "current_transfer_payments": 22,
        "social_benefits_to_persons": 23,
    })
    if not t31.empty:
        t31.index.name = "year"
        out = PARSED_RAW / "moos_govt_accounts.csv"
        t31.to_csv(out)
        outputs.append(str(out))
        steps.append(f"T3.1: {len(t31)} years (govt receipts & expenditures)")
        print(f"    [L17] T3.1: {len(t31)} years")

    return {
        "series_id": "L17",
        "status": "ok" if outputs else "fail",
        "steps": steps,
        "outputs": outputs,
    }

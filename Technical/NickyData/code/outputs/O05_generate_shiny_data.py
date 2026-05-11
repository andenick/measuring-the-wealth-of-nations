#!/usr/bin/env python3
"""O05 - Generate Shiny-compatible CSVs from NickyData final-data.

Bridges the NickyData pipeline to the R Shiny app by reading series CSVs
and writing data files with the column names the app expects.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
import shutil
import numpy as np
import pandas as pd
from utils.paths import (
    SERIES_OUT, STUDIES_OUT, CONFIG, TECHNICAL, ensure_dirs,
)

SHINY_DATA = TECHNICAL / "ShinyApp" / "data"

EXPLOITATION_RENAME = {
    "T506": "exploitation_rate",
    "T507": "surplus_ratio",
    "T510": "value_composition",
}


def _read_series(sid: str, is_study: bool = False) -> pd.Series | None:
    out_dir = STUDIES_OUT if is_study else SERIES_OUT
    csv_path = out_dir / f"{sid}.csv"
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path, index_col=0)
    if "combined" in df.columns:
        return df["combined"]
    if "book" in df.columns:
        return df["book"]
    return df.iloc[:, 0] if len(df.columns) > 0 else None


def generate():
    ensure_dirs()
    SHINY_DATA.mkdir(parents=True, exist_ok=True)
    outputs = []

    # --- Exploitation & Composition (1948-2024) ---
    merged = pd.DataFrame()
    for sid in ["T501", "T502", "T503", "T504", "T505", "T506",
                "T507", "T508", "T509", "T510", "T511", "T512",
                "T513", "T514", "T515", "T516"]:
        s = _read_series(sid)
        if s is not None:
            col_name = EXPLOITATION_RENAME.get(sid, sid)
            merged[col_name] = s
    if not merged.empty:
        # Compute derived columns the legacy app expects
        if "T505" in merged.columns and "T503" in merged.columns:
            merged["S_Y"] = merged["T505"] / merged["T503"]
        if "T504" in merged.columns and "T503" in merged.columns:
            merged["V_Y"] = merged["T504"] / merged["T503"]
        if "T502" in merged.columns and "T503" in merged.columns:
            merged["C_Y"] = merged["T502"] / merged["T503"]
        if "T502" in merged.columns and "T504" in merged.columns:
            merged["materialized_composition"] = merged["T502"] / merged["T504"]
        merged.index.name = "year"
        merged.to_csv(SHINY_DATA / "exploitation_composition_1948_2024.csv")
        outputs.append("exploitation_composition_1948_2024.csv")

    # --- NSW (1952-2025) ---
    merged = pd.DataFrame()
    for sid in ["T601", "T602", "T603", "T604", "T605", "T606",
                "T607", "T608", "T609"]:
        s = _read_series(sid)
        if s is not None:
            merged[sid] = s
    if not merged.empty:
        merged.index.name = "year"
        merged.to_csv(SHINY_DATA / "nsw_1952_2025.csv")
        outputs.append("nsw_1952_2025.csv")

    # --- Summary Indicators (1948-2024) ---
    merged = pd.DataFrame()
    for sid in ["T506", "T511", "T512", "T513", "T514"]:
        s = _read_series(sid)
        if s is not None:
            merged[sid] = s
    if not merged.empty:
        merged.index.name = "year"
        merged.to_csv(SHINY_DATA / "summary_indicators_1948_2024.csv")
        outputs.append("summary_indicators_1948_2024.csv")

    # --- Employment (1948-2024) with legacy column names ---
    emp = pd.DataFrame()
    for sid, col_name in [("T515", "Lp_productive"), ("T516", "Lu_unproductive")]:
        s = _read_series(sid)
        if s is not None:
            emp[col_name] = s
    if not emp.empty:
        emp["L_total"] = emp.get("Lp_productive", 0) + emp.get("Lu_unproductive", 0)
        if emp["L_total"].sum() > 0:
            emp["Lp_L_ratio"] = emp["Lp_productive"] / emp["L_total"]
            emp["Lu_L_ratio"] = emp["Lu_unproductive"] / emp["L_total"]
        emp.index.name = "year"
        emp.to_csv(SHINY_DATA / "employment_1948_2024.csv")
        outputs.append("employment_1948_2024.csv")

    # --- Profit Rates (1948-2024) with legacy column names ---
    _write_profit_rates_csv(outputs)

    # --- Study CSVs ---
    for series_ids, filename in [
        (["N1301", "N1302", "N1304", "N1305"], "moos_nsw_comparison.csv"),
        (["N1401", "N1402", "N1403", "N1404"], "mohun_comparison.csv"),
        (["N1601", "N1602", "N1701"], "international_nsw.csv"),
    ]:
        merged = pd.DataFrame()
        for sid in series_ids:
            s = _read_series(sid, is_study=True)
            if s is not None:
                merged[sid] = s
        if not merged.empty:
            merged.index.name = "year"
            merged.to_csv(SHINY_DATA / filename)
            outputs.append(filename)

    # --- Labor value scatter (if exported by P14) ---
    _write_labor_scatter_csv(outputs)

    summary = f"{len(outputs)} Shiny data files generated"
    print(f"    [O05] {summary}")
    return {"status": "ok", "summary": summary, "outputs": outputs}


def _write_profit_rates_csv(outputs: list):
    """Write profit_rates_1948_2024.csv with legacy column names."""
    legacy_file = SHINY_DATA / "profit_rates_1948_1989.csv"
    legacy = pd.DataFrame()
    if legacy_file.exists():
        legacy = pd.read_csv(legacy_file)

    merged = pd.DataFrame()

    t513 = _read_series("T513")
    if t513 is not None:
        merged["r_star_pct"] = t513

    t514 = _read_series("T514")
    if t514 is not None:
        merged["r_star_adj_pct"] = t514

    if not merged.empty:
        merged.index.name = "year"
        for extra_col in ["r_nipa_pct", "r_nipa_adj_pct", "capacity_utilization",
                          "S_star", "K", "GDP"]:
            if extra_col in legacy.columns:
                legacy_indexed = legacy.set_index("year")[extra_col]
                merged[extra_col] = legacy_indexed.reindex(merged.index)

        merged.to_csv(SHINY_DATA / "profit_rates_1948_2024.csv")
        outputs.append("profit_rates_1948_2024.csv")


def _write_labor_scatter_csv(outputs: list):
    """Copy labor value scatter data to Shiny if it exists."""
    from utils.paths import SHINY_OUT
    scatter_path = SHINY_OUT / "T701_scatter.csv"
    if scatter_path.exists():
        out_path = SHINY_DATA / "labor_value_scatter.csv"
        shutil.copy2(scatter_path, out_path)
        outputs.append("labor_value_scatter.csv")

#!/usr/bin/env python3
"""O02 - Generate Master Database: single file with all series for all years.

Creates a wide-format CSV with one row per year and one column per series.
Includes unit metadata in Row 1.

Output: Outputs/Data/COMPLETE_DATABASE/as2_master_1948_2024.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT
from utils.units import SERIES_UNITS, get_unit

# All series: Book (T-series) + Studies (N-series)
BOOK_SERIES = [
    "T501", "T502", "T503", "T504", "T505", "T506", "T507", "T508", "T509", "T510",
    "T511", "T512", "T513", "T514", "T515", "T516",
    "T601", "T602", "T603", "T604", "T605", "T606", "T607", "T608", "T609",
    "T901",
]
STUDY_SERIES = [
    "N1001", "N1002",  # Tonak 1984
    "N1101", "N1102", "N1103",  # ST 1987
    "N1201", "N1202",  # ST 2002
    "N1301", "N1302", "N1304", "N1305",  # Moos 2017
    "N1401", "N1402", "N1403", "N1404",  # Mohun 2005
    "N1501", "N1502", "N1503", "N1504",  # Mohun 2013
    "N1601", "N1602",  # Turkey 2022
    "N1701",  # Cronin NZ
]
MASTER_SERIES = BOOK_SERIES + STUDY_SERIES

OUTPUT_DIR = Path(__file__).resolve().parents[3] / "Outputs" / "Data/COMPLETE_DATABASE")


def generate():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_data = {}
    units_row = {}

    for sid in MASTER_SERIES:
        # Check both book and studies directories
        csv_path = SERIES_OUT / f"{sid}.csv"
        if not csv_path.exists():
            from utils.paths import STUDIES_OUT
            csv_path = STUDIES_OUT / f"{sid}.csv"
        if not csv_path.exists():
            continue

        df = pd.read_csv(csv_path, index_col=0)
        col = "combined" if "combined" in df.columns else df.columns[-1]
        series = df[col]
        all_data[sid] = series
        units_row[sid] = get_unit(sid)

    # Also add NAICS aggregates if available
    naics_path = SERIES_OUT / "NAICS_marxian_aggregates.csv"
    if naics_path.exists():
        naics = pd.read_csv(naics_path, index_col=0)
        for col in ["TV_star", "GO_productive", "GO_trading"]:
            if col in naics.columns:
                all_data[col] = naics[col]
                units_row[col] = "billions"

    # Build master DataFrame
    master = pd.DataFrame(all_data)
    master.index.name = "year"
    master = master.sort_index()

    # Save CSV
    out_path = OUTPUT_DIR / "as2_master_1948_2024.csv"

    # Write unit metadata as comment, then data
    with open(out_path, "w", encoding="utf-8") as f:
        # Row 0: unit metadata
        f.write("# Units: " + ", ".join(f"{k}={v}" for k, v in units_row.items()) + "\n")
        master.to_csv(f)

    # Also save clean XLSX
    xlsx_path = OUTPUT_DIR / "as2_master_1948_2024.xlsx"
    try:
        master.to_excel(xlsx_path, sheet_name="Data")
        print(f"  XLSX: {xlsx_path}")
    except Exception:
        pass  # openpyxl may not be available

    n_years = len(master)
    n_series = len(master.columns)
    core_complete = master.loc[1948:1989].notna().all(axis=1).sum()

    print(f"  Master database: {n_years} years x {n_series} series")
    print(f"  Core period (1948-1989): {core_complete}/42 years fully complete")
    print(f"  CSV: {out_path}")

    return {"status": "ok", "rows": n_years, "cols": n_series, "path": str(out_path)}


if __name__ == "__main__":
    generate()

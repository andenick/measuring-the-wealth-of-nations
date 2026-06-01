"""P02_ES1504 — Compute Lu/Lp burden ratio (Mohun 2013).

ES1504 = Mohun's Lu (ES1503) / Mohun's Lp (from mohun_employment_annual_1948_1989.csv).
The "unproductive burden" — how many unproductive workers per productive worker.

Book finding: burden ratio rises from ~0.77 (1948) to higher in later years.
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.io import read_book_table, write_series_csv
from utils.paths import DATA_FINAL, EXTERNAL_STUDIES

SERIES_ID = "ES1504"
SUBSERIES = "ES1504-A"

def compute() -> pd.DataFrame:
    es1503 = pd.read_csv(DATA_FINAL / "ES1503.csv")
    es1503 = es1503[es1503["series_id"] == "ES1503-A"][["year", "value"]].rename(columns={"value": "Lu"})
    # Get Lp from Mohun employment annual
    mohun_emp = read_book_table(EXTERNAL_STUDIES / "Mohun_mohun_employment_annual_1948_1989.csv")
    lp = mohun_emp[["year", "Lp_mohun"]].rename(columns={"Lp_mohun": "Lp"})
    merged = es1503.merge(lp, on="year").sort_values("year").reset_index(drop=True)
    merged["value"] = merged["Lu"] / merged["Lp"]
    merged["series_id"] = SUBSERIES
    merged["units"] = "share"
    merged["stage"] = "analytical_derivation"
    merged["provenance"] = "ES1503 / Mohun Lp_mohun"
    return merged[["series_id", "year", "value", "units", "stage", "provenance"]]

def run():
    df = compute()
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_ES1504] {len(df)} rows; first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}; wrote {final_path.name}")
    return df

if __name__ == "__main__":
    run()

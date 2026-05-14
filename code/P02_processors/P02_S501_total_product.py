"""P02_S501 — Process Total Product (TP*) into the published series.

For the book period (1948-1989), the processor is a pass-through from the loader:
the digitized Appendix H.1 values ARE the canonical published values; no
transformation is applied. The extension (S501-B, 1997-2024) and combined splice
(S501-COMBINED) are added when the BEA loader is wired up — until then, the
final CSV holds book-period values only, with status='book_period_only'.

This explicit pass-through preserves the provenance chain: any value in
data/intermediate/S501.csv or data/final/S501.csv traces directly to one row
of book_tableH1_1948_1989.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.io import write_series_csv
from L01_loaders.L01_S501_total_product import run as load_S501  # noqa: E402


SERIES_ID = "S501"


def process(book_df: pd.DataFrame) -> pd.DataFrame:
    """Pass-through for book period; future extension stages will append S501-B/COMBINED rows."""
    out = book_df.copy()
    out["stage"] = "book_period"
    out["provenance"] = "book_tableH1_1948_1989.csv:TP_star"
    return out[["series_id", "year", "value", "units", "stage", "provenance"]]


def run() -> pd.DataFrame:
    book_df = load_S501()
    final = process(book_df)
    inter_path = write_series_csv(final, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(final, SERIES_ID, stage="final")
    print(f"    [P02_{SERIES_ID}] {len(final)} rows; intermediate={inter_path.name}; final={final_path.name}")
    return final


if __name__ == "__main__":
    run()

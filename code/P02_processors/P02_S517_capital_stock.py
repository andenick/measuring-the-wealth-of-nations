"""P02_S517 — Process K* pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S517_capital_stock import load as load_S517  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S517"


def run():
    df = load_S517()
    df["stage"]      = "book_period_and_extension"
    df["provenance"] = "BEA Fixed Assets 4.1 Line 1 (Private nonresidential)"
    df = df[["series_id", "year", "value", "units", "stage", "provenance"]]
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S517] {len(df)} rows; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

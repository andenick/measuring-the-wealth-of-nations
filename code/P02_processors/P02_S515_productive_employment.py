"""P02_S515 — Process Productive Employment (Lp); pass-through, 1948-1961."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S515_productive_employment import load as load_S515  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


def run():
    df = load_S515()
    df["stage"]      = "book_period"
    df["provenance"] = "TableE3_LaborStatistics.csv:Lp_total"
    df = df[["series_id", "year", "value", "units", "stage", "provenance"]]
    write_series_csv(df, "S515", stage="intermediate")
    final_path = write_series_csv(df, "S515", stage="final")
    print(f"    [P02_S515] {len(df)} rows; first={df.iloc[0]['value']:.0f}; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

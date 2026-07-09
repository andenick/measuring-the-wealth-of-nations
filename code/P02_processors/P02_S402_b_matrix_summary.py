"""P02_S402 — Leontief inverse summary pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S402_b_matrix_summary import load as load_S402  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


def run():
    df = load_S402()
    df["stage"] = "benchmark_only"
    df["provenance"] = ("REBUILT Leontief inverse (io_matrices_rebuilt; workpackage C 2026-07): "
                        "value = mean total-requirements column multiplier over live columns "
                        "(SIC: (I-A)^-1 of A=Z/gross-output-X; NAICS: BEA published Total "
                        "Requirements IxI summary)")
    df = df[["series_id", "year", "value", "units", "stage", "provenance",
             "n_sectors", "n_live_columns", "b_colsum_mean", "b_colsum_max",
             "max_b_element", "b_trace", "b_frobenius_norm"]]
    write_series_csv(df, "S402", stage="intermediate")
    final_path = write_series_csv(df, "S402", stage="final")
    print(f"    [P02_S402] {len(df)} rows; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

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
    df["provenance"] = "BEA Benchmark IO via io_matrix.b_matrix_summary"
    df = df[["series_id", "year", "value", "units", "stage", "provenance",
             "n_sectors", "max_b_element", "b_column_sum_max", "b_trace", "b_frobenius_norm"]]
    write_series_csv(df, "S402", stage="intermediate")
    final_path = write_series_csv(df, "S402", stage="final")
    print(f"    [P02_S402] {len(df)} rows; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

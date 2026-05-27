"""P02_S401 — A-matrix summary, pass-through emitting full summary columns."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S401_a_matrix_summary import load as load_S401  # noqa: E402
from utils.io import write_series_csv  # noqa: E402


SERIES_ID = "S401"


def run():
    df = load_S401()
    df["stage"]      = "benchmark_only"
    df["provenance"] = "BEA Benchmark IO matrices (SIC + NAICS) via io_matrix.a_matrix_summary"
    df = df[["series_id", "year", "value", "units", "stage", "provenance",
             "n_sectors", "sparsity", "max_eigenvalue", "condition_number", "leontief_max_dev"]]
    write_series_csv(df, SERIES_ID, stage="intermediate")
    final_path = write_series_csv(df, SERIES_ID, stage="final")
    print(f"    [P02_S401] {len(df)} benchmark years; wrote {final_path.name}")
    return df


if __name__ == "__main__":
    run()

"""P02_XS1704 — Process NZ Total Value (Cronin 2001); pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_XS1704_nz_total_value_cronin2001 import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Cronin2001_cronin_table1_nzsna_classical_1972_1995.csv:total_value_mNZD")
    print(f"    [P02_XS1704] wrote {final_path.name}")


if __name__ == "__main__":
    run()

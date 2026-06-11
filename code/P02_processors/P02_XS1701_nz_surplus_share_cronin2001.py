"""P02_XS1701 — Process NZ Surplus Share of Total Value (Cronin 2001); pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_XS1701_nz_surplus_share_cronin2001 import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Cronin2001_cronin_table2_ratios_1972_1995.csv:surplus_share_of_total_value_pct")
    print(f"    [P02_XS1701] wrote {final_path.name}")


if __name__ == "__main__":
    run()

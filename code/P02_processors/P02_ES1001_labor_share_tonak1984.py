"""P02_ES1001 — Process Labor Share of National Taxes (Tonak 1984); pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_ES1001_labor_share_tonak1984 import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Tonak1984_table_V_taxes_labor_nonlabor_1952_1980.csv:labor_taxes")
    print(f"    [P02_ES1001] wrote {final_path.name}")


if __name__ == "__main__":
    run()

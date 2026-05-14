"""P02_S508 — Process Productive Consumption (CON*); pass-through, 1948-1961."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S508_productive_consumption import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "TableE2_RevenueAccounts_1948_1961.csv:CON_star")
    print(f"    [P02_{LOADER.series_id}] wrote {final_path.name}")


if __name__ == "__main__":
    run()

"""P02_ES1402 — Process Productive Labor Share — Mohun Classification (Mohun 2005); pass-through."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_ES1402_productive_labor_share_mohun2005 import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Mohun_mohun_employment_annual_1948_1989.csv:Lp_mohun_L_ratio")
    print(f"    [P02_ES1402] wrote {final_path.name}")


if __name__ == "__main__":
    run()

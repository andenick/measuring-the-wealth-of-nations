"""P02_S605 — Process Government Benefits to Workers (B_w); pass-through for book period."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S605_benefits_workers import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Table6_2_BenefitAccounts.csv:total_benefits")
    print(f"    [P02_S605] wrote {final_path.name}")


if __name__ == "__main__":
    run()

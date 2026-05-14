"""P02_S607 — Process Net Social Wage (NSW = B_w + G_w - T_w); pass-through for book period."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S607_net_social_wage import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Table6_3_NetSocialWage.csv:nsw")
    print(f"    [P02_S607] wrote {final_path.name}")


if __name__ == "__main__":
    run()

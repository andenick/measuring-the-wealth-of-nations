"""P02_S511 — Process Productive Labor Share (Lp/L); pass-through for book period."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S511_productive_labor_share import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Table5_7_KeyRatios.csv:T511A")
    print(f"    [P02_{LOADER.series_id}] wrote {final_path.name}")


if __name__ == "__main__":
    run()

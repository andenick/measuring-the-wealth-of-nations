"""P02_S503 — Process GFP; pass-through for book period."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S503_gross_final_product import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "book_tableH1_1948_1989.csv:GFP_star")
    print(f"    [P02_{LOADER.series_id}] wrote {final_path.name}")


if __name__ == "__main__":
    run()

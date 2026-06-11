"""P02_XS1501 — Working Class Unproductive Labor (Mohun 2013) pass-through."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_XS1501_working_class_unproductive_mohun2013 import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402

def run():
    final_path = run_pipeline_for_series(LOADER, "Mohun_unproductive_decomposition_1948_1989.csv:Luw_mohun")
    print(f"    [P02_XS1501] wrote {final_path.name}")

if __name__ == "__main__":
    run()

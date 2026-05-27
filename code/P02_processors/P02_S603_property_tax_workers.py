"""P02_S603 — Process Property Tax Workers; pass-through for book period."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from L01_loaders.L01_S603_property_tax_workers import LOADER  # noqa: E402
from utils.series import run_pipeline_for_series  # noqa: E402


def run():
    final_path = run_pipeline_for_series(LOADER, "Table6_1_TaxAccounts.csv:property_tax_workers")
    print(f"    [P02_S603] wrote {final_path.name}")


if __name__ == "__main__":
    run()

#!/usr/bin/env python3
"""S02 - Generate ANU_LEDGER.json by scanning file system for artifacts.

Produces a per-series artifact coverage report conforming to Anu Ledger v2.0.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
from utils.paths import (
    SERIES_OUT, STUDIES_OUT, CHOPPED_OUT, EXTENBOOKS,
    STUDIES_CHOPPED, STUDIES_EXTENBOOKS, CONFIG, TECHNICAL, ensure_dirs,
)

DOCS_SERIES = TECHNICAL / "docs" / "series"
DOCS_STUDIES = TECHNICAL / "docs" / "studies"
DOCS_FIGURES = TECHNICAL / "docs" / "figures"


def run():
    ensure_dirs()

    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        registry = json.load(f)

    ledger = {"version": "2.0", "generated_by": "S02_generate_ledger.py", "series": {}}

    for sid, config in sorted(registry["series"].items()):
        is_study = sid.startswith("N")
        series_dir = STUDIES_OUT if is_study else SERIES_OUT
        chopped_dir = STUDIES_CHOPPED if is_study else CHOPPED_OUT
        extenbook_dir = STUDIES_EXTENBOOKS if is_study else EXTENBOOKS
        docs_dir = DOCS_STUDIES if is_study else DOCS_SERIES

        has_ext = config.get("extension") is not None

        figures = config.get("figures", [])
        fpr_found = []
        for fig in figures:
            fpr_path = DOCS_FIGURES / f"{fig}_FPR.md"
            if fpr_path.exists():
                fpr_found.append(fig)

        ledger["series"][sid] = {
            "csv": (series_dir / f"{sid}.csv").exists(),
            "chopped": (chopped_dir / f"{sid}_chopped.csv").exists(),
            "extenbook": (extenbook_dir / f"{sid}_extenbook.xlsx").exists(),
            "dpr": (docs_dir / f"{sid}_DPR.md").exists(),
            "epr": (docs_dir / f"{sid}_EPR.md").exists() if has_ext or _is_synthetic(config) else "n/a",
            "decomposition": (docs_dir / f"{sid}_DECOMPOSITION.md").exists() or (
                is_study and (DOCS_STUDIES / "STUDY_DECOMPOSITIONS.md").exists()
            ),
            "figure_fprs": fpr_found if figures else "n/a",
        }

    out_path = CONFIG / "ANU_LEDGER.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)

    total = len(ledger["series"])
    complete = sum(
        1 for s in ledger["series"].values()
        if s["csv"] and s["dpr"] and s["chopped"]
    )

    summary = f"Ledger: {complete}/{total} series have csv+dpr+chopped"
    print(f"    [S02] {summary}")
    return {"status": "ok", "summary": summary}


def _is_synthetic(config: dict) -> bool:
    return config.get("data_quality") == "estimated_from_benchmarks"

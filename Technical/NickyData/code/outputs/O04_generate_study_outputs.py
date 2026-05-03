#!/usr/bin/env python3
"""O04 - Generate Chopped CSVs and Extenbooks for N-series (external studies).

Reads from studies/series/ and series_registry.json, produces:
- studies/chopped/N####_chopped.csv
- studies/extenbooks/N####_extenbook.xlsx
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
import pandas as pd
from utils.paths import (
    STUDIES_OUT, STUDIES_CHOPPED, STUDIES_EXTENBOOKS,
    CONFIG, ensure_dirs,
)
from utils.formats.chopped_writer import write_chopped
from utils.formats.extenbook_writer import write_extenbook


def generate():
    ensure_dirs()

    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        registry = json.load(f)

    n_series = [k for k in registry["series"] if k.startswith("N")]
    generated_chopped = 0
    generated_extenbook = 0

    for sid in sorted(n_series):
        csv_path = STUDIES_OUT / f"{sid}.csv"
        if not csv_path.exists():
            print(f"    [O04] {sid}: CSV not found, skipping")
            continue

        df = pd.read_csv(csv_path, index_col=0)
        series_config = registry["series"][sid]
        subseries_defs = series_config.get("subseries", {})

        data_dict: dict[str, pd.Series] = {}
        for sub_id in subseries_defs:
            col_map = {
                f"{sid}-A": "book",
                f"{sid}-COMBINED": "combined",
            }
            col = col_map.get(sub_id)
            if col and col in df.columns:
                data_dict[sub_id] = df[col].dropna()
            elif "combined" in df.columns:
                data_dict[sub_id] = df["combined"].dropna()

        if not data_dict:
            print(f"    [O04] {sid}: no data mapped, skipping")
            continue

        try:
            write_chopped(data_dict, registry, sid, STUDIES_CHOPPED)
            generated_chopped += 1
        except Exception as e:
            print(f"    [O04] {sid} chopped FAIL: {e}")

        try:
            write_extenbook(data_dict, registry, None, sid, STUDIES_EXTENBOOKS)
            generated_extenbook += 1
        except Exception as e:
            print(f"    [O04] {sid} extenbook FAIL: {e}")

    summary = f"{generated_chopped} chopped + {generated_extenbook} extenbooks from {len(n_series)} N-series"
    print(f"    [O04] {summary}")
    return {
        "status": "ok",
        "summary": summary,
        "chopped": generated_chopped,
        "extenbooks": generated_extenbook,
    }

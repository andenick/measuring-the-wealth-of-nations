#!/usr/bin/env python3
"""O06 - Regenerate T-series Chopped CSVs using Anu Chopped Standard format.

Replaces legacy-format chopped files in book/chopped/ with standard format:
Row 1: "Year" + metadata labels
Row 2: "" + subseries IDs
Row 3+: data
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
import pandas as pd
from utils.paths import SERIES_OUT, CHOPPED_OUT, CONFIG, ensure_dirs
from utils.formats.chopped_writer import write_chopped


def generate():
    ensure_dirs()

    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        registry = json.load(f)

    t_series = [k for k in registry["series"] if k.startswith("T")]
    generated = 0

    for sid in sorted(t_series):
        csv_path = SERIES_OUT / f"{sid}.csv"
        if not csv_path.exists():
            continue

        series_config = registry["series"][sid]
        subseries_defs = series_config.get("subseries", {})
        if not subseries_defs:
            continue

        df = pd.read_csv(csv_path, index_col=0)
        data_dict: dict[str, pd.Series] = {}

        for sub_id in subseries_defs:
            if sub_id.endswith("-A") and "book" in df.columns:
                data_dict[sub_id] = df["book"].dropna()
            elif sub_id.endswith("-EXT") and "ext" in df.columns:
                data_dict[sub_id] = df["ext"].dropna()
            elif sub_id.endswith("-COMBINED") and "combined" in df.columns:
                data_dict[sub_id] = df["combined"].dropna()

        if not data_dict:
            continue

        try:
            write_chopped(data_dict, registry, sid, CHOPPED_OUT)
            generated += 1
        except Exception as e:
            print(f"    [O06] {sid} FAIL: {e}")

    summary = f"{generated} T-series chopped CSVs regenerated (Anu Standard format)"
    print(f"    [O06] {summary}")
    return {"status": "ok", "summary": summary, "generated": generated}

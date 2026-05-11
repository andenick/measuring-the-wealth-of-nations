#!/usr/bin/env python3
"""M99 - Promote Adjustments: copy adjusted data into main series files.

Reads adjusted CSVs from data/adjusted-final-data/ and overwrites the
'combined' column in the corresponding data/final-data/series/ file.
The 'book' column is NEVER modified.

This makes M01 (ADJ-002) and M02 (ADJ-001) adjustments visible in the
main pipeline output, chopped CSVs, and extenbooks.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, ADJUSTED, ensure_dirs

ADJUSTMENT_MAP = {
    # M02 (DIV-001): K→K* profit rate adjustment
    "T513_adjusted.csv": {
        "target": "T513.csv",
        "source_col": "k_star_adjusted",
        "description": "K→K* profit rate (DIV-001)",
    },
    "T514_adjusted.csv": {
        "target": "T514.csv",
        "source_col": "k_star_adjusted",
        "description": "K→K* capacity-adjusted profit rate (DIV-001)",
    },
    # M01 (DIV-002): year-varying ec_u/ec_p adjustment
    "T504_adjusted.csv": {
        "target": "T504.csv",
        "source_col": "combined",
        "description": "V* with ec_u/ec_p adjustment (DIV-002)",
    },
    "T505_adjusted.csv": {
        "target": "T505.csv",
        "source_col": "combined",
        "description": "S* = e × V* recomputed (DIV-002)",
    },
    "T506_adjusted.csv": {
        "target": "T506.csv",
        "source_col": "combined",
        "description": "e with ec_u/ec_p adjustment (DIV-002)",
    },
}


def adjust(series_filter=None):
    """Promote adjusted data to main series files."""
    ensure_dirs()
    steps = []
    outputs = []

    for adj_file, config in ADJUSTMENT_MAP.items():
        adj_path = ADJUSTED / adj_file
        if not adj_path.exists():
            steps.append(f"SKIP: {adj_file} not found")
            continue

        target_path = SERIES_OUT / config["target"]
        if not target_path.exists():
            steps.append(f"SKIP: target {config['target']} not found")
            continue

        # Read adjusted and target
        adj_df = pd.read_csv(adj_path, index_col=0)
        target_df = pd.read_csv(target_path, index_col=0)

        source_col = config["source_col"]
        if source_col not in adj_df.columns:
            steps.append(f"SKIP: column '{source_col}' not in {adj_file}")
            continue

        adj_values = adj_df[source_col].dropna()

        # Compute delta
        original = target_df["combined"]
        common = original.index.intersection(adj_values.index)
        if len(common) == 0:
            steps.append(f"SKIP: no overlapping years for {config['target']}")
            continue

        delta = (adj_values[common] - original[common]).abs()
        max_delta = float(delta.max())
        mean_delta = float(delta.mean())

        # Promote: overwrite combined column with adjusted values (including new years)
        for yr in adj_values.index:
            if yr in target_df.index:
                target_df.loc[yr, "combined"] = adj_values[yr]
            else:
                target_df.loc[yr, "combined"] = adj_values[yr]
        target_df = target_df.sort_index()

        target_df.to_csv(target_path)
        outputs.append(str(target_path))
        steps.append(
            f"PROMOTED: {config['target']} ← {adj_file} ({config['description']})"
            f" | {len(adj_values)} years, max_delta={max_delta:.4f}, mean_delta={mean_delta:.4f}"
        )
        print(f"    [M99] {config['target']}: promoted {len(adj_values)} years from {adj_file}")

    return {
        "script": "M99_promote_adjustments",
        "status": "ok",
        "steps": steps,
        "outputs": outputs,
    }


if __name__ == "__main__":
    result = adjust()
    for s in result["steps"]:
        print(f"  {s}")

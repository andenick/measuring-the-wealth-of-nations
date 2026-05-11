#!/usr/bin/env python3
"""Generate Shiny subsource catalog from the series registry.

Reads series_registry.json and produces SHINY_SUBSOURCES.json with
per-column subsource metadata (color, period, source) for the Shiny app.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.config_loader import load_registry
from lib.paths import SHINY_OUT


def generate_subsources(registry: dict) -> dict:
    """Build a subsource catalog from the registry."""
    subsources = {}

    for sid, entry in registry.get("series", {}).items():
        for sub_id, sub_def in entry.get("subseries", {}).items():
            shiny_col = sub_def.get("shiny_column")
            if not shiny_col:
                continue
            subsources[shiny_col] = {
                "series_id": sid,
                "subseries_id": sub_id,
                "name": sub_def.get("name", sub_id),
                "source": sub_def.get("source", ""),
                "period": sub_def.get("period", []),
                "color": sub_def.get("color", "#333333"),
                "units": sub_def.get("units", ""),
            }

    return {
        "generated_by": "anu_replicator_shiny_subsources_as2",
        "subsources": subsources,
    }


def main():
    registry = load_registry()
    catalog = generate_subsources(registry)

    out_dir = SHINY_OUT / "catalogs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "SHINY_SUBSOURCES.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"  [shiny-subsources] {len(catalog['subsources'])} subsources written to {out_path}")


if __name__ == "__main__":
    main()

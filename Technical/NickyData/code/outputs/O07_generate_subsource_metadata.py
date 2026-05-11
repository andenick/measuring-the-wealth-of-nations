#!/usr/bin/env python3
"""O07 - Generate SUBSOURCE_METADATA.json from series_registry.json.

Maps each chopped CSV column ID to its source, period, role, and construction text
for use by visualization apps and D7/D10 validation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
from utils.paths import CONFIG, SHINY_OUT, ensure_dirs


def run():
    ensure_dirs()

    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        registry = json.load(f)

    metadata = {}

    for sid, config in sorted(registry["series"].items()):
        name = config.get("name", "")
        chapter = config.get("chapter")
        has_ext = config.get("extension") is not None

        for sub_id, sub in config.get("subseries", {}).items():
            source = sub.get("source", "unknown")
            period = sub.get("period", [])
            units = sub.get("units", "")

            is_ext = "EXT" in sub_id
            is_combined = "COMBINED" in sub_id

            if is_combined:
                role = "final_series"
            elif is_ext:
                role = "extension"
            else:
                role = "book_replication"

            construction = config.get("construction", [])
            construction_steps = []
            for step in construction:
                op = step.get("op", "")
                formula = step.get("formula", "")
                if formula:
                    construction_steps.append(f"{op}: {formula}")
                elif op:
                    construction_steps.append(op)

            construction_text = f"{name}. " + "; ".join(construction_steps) if construction_steps else name

            entry = {
                "series_id": sid,
                "subseries_id": sub_id,
                "series_name": name,
                "source_name": source,
                "period_start": period[0] if period else None,
                "period_end": period[1] if len(period) > 1 else None,
                "units": units,
                "role": role,
                "is_extension": is_ext,
                "is_component": False,
                "construction_text": construction_text,
            }

            if chapter:
                entry["chapter"] = chapter

            metadata[sub_id] = entry

    out_path = SHINY_OUT / "SUBSOURCE_METADATA.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    summary = f"Subsource metadata: {len(metadata)} entries for {len(registry['series'])} series"
    print(f"    [O07] {summary}")
    return {"status": "ok", "summary": summary}

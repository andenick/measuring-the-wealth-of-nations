#!/usr/bin/env python3
"""S04 - Generate provenance_index.json from series_registry.json.

Builds three indexes: by_series, by_source, by_api for Anu Review D0 gate.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
from collections import defaultdict
from utils.paths import CONFIG


def run():
    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        registry = json.load(f)

    by_series = {}
    by_source = defaultdict(list)
    by_api = defaultdict(list)

    for sid, config in sorted(registry["series"].items()):
        sources = []
        apis = []

        for sub_id, sub in config.get("subseries", {}).items():
            source = sub.get("source", "unknown")
            sources.append({
                "subseries": sub_id,
                "source": source,
                "period": sub.get("period", []),
                "units": sub.get("units", ""),
            })
            by_source[source].append(sid)

            if any(kw in source.lower() for kw in ("bea", "bls", "fred", "api")):
                apis.append(source)
                by_api[source].append(sid)

        construction = config.get("construction", [])
        ext = config.get("extension")

        by_series[sid] = {
            "name": config.get("name", ""),
            "chapter": config.get("chapter"),
            "sources": sources,
            "apis": list(set(apis)),
            "extension": {
                "method": ext.get("splice_method") if ext else None,
                "splice_year": ext.get("splice_year") if ext else None,
                "depends_on": ext.get("depends_on", []) if ext else [],
            } if ext else None,
            "construction_steps": len(construction),
            "loader": config.get("loader", ""),
            "processor": config.get("processor", ""),
        }

    # Deduplicate by_source and by_api
    by_source_clean = {k: sorted(set(v)) for k, v in by_source.items()}
    by_api_clean = {k: sorted(set(v)) for k, v in by_api.items()}

    index = {
        "version": "1.0",
        "generated_by": "S04_generate_provenance_index.py",
        "by_series": by_series,
        "by_source": by_source_clean,
        "by_api": by_api_clean,
    }

    out_path = CONFIG / "provenance_index.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    summary = f"Provenance index: {len(by_series)} series, {len(by_source_clean)} sources, {len(by_api_clean)} APIs"
    print(f"    [S04] {summary}")
    return {"status": "ok", "summary": summary}

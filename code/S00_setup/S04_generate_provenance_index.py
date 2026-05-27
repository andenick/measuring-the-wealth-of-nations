"""S04 - Generate PROVENANCE_INDEX.json.

For each series, lists every artifact path that participates in its provenance
chain (research JSON, DPR, source CSV, loader, processor, validator, intermediate
output, final CSV). Used by /anu-review D13 (data authenticity) to trace any
value back to its source.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "series_registry.json"
INDEX = ROOT / "PROVENANCE_INDEX.json"


def relpath(p: Path) -> str | None:
    if not p.exists():
        return None
    return p.relative_to(ROOT).as_posix()


def first_script_match(stage_dir: str, sid: str) -> str | None:
    d = ROOT / "code" / stage_dir
    if not d.is_dir():
        return None
    for f in sorted(d.glob("*.py")):
        if sid in f.name:
            return f.relative_to(ROOT).as_posix()
    return None


def build_entry(sid: str, entry: dict) -> dict:
    sources: list[str] = []
    if entry.get("source_file"):
        candidate = ROOT / "data" / "source" / "book_tables" / entry["source_file"]
        if candidate.exists():
            sources.append(candidate.relative_to(ROOT).as_posix())
    return {
        "research":     relpath(ROOT / "research"   / f"{sid}_research.json"),
        "dpr":          relpath(ROOT / "docs/series" / f"{sid}_DPR.md"),
        "epr":          relpath(ROOT / "docs/series" / f"{sid}_EPR.md"),
        "loader":       first_script_match("L01_loaders",     sid),
        "processor":    first_script_match("P02_processors",  sid),
        "validator":    first_script_match("V03_validators",  sid),
        "manual":       first_script_match("M04_manual",      sid),
        "intermediate": relpath(ROOT / "data/intermediate" / f"{sid}.csv"),
        "final":        relpath(ROOT / "data/final" / f"{sid}.csv"),
        "chopped":      relpath(ROOT / "chopped" / f"{sid}.csv"),
        "extenbook":    relpath(ROOT / "extenbooks" / f"{sid}.xlsx"),
        "source_files": sources,
    }


def run() -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    series = reg.get("series", {})
    index: dict[str, dict] = {sid: build_entry(sid, entry) for sid, entry in series.items()}

    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_version": reg.get("version"),
        "series": index,
    }
    INDEX.write_text(json.dumps(out, indent=2), encoding="utf-8")
    found_any = sum(1 for v in index.values() if any(v.values()))
    print(f"    [S04] Provenance index: {len(index)} series; {found_any} with at least one artifact")
    return out


if __name__ == "__main__":
    run()

"""O01 — Generate Anu Chopped CSVs for all implemented series.

The Anu Chopped Standard v2.0 specifies a 3-row CSV structure:
  Row 1: Metadata (per-column source descriptions, units, methodology notes)
  Row 2: Column IDs (Year, S###-A, S###-EXT, S###-F, S###-COMBINED, ...)
  Row 3+: Data

For the current Wave 1 partial build, each Ch5 series has at most one subseries
(S###-A, the book period). Extension subseries (S###-EXT, -F, -COMBINED) are
added later when API access is provisioned. The chopped CSV reflects the
current state honestly — no fabricated extension columns.
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import CHOPPED_DIR, DATA_FINAL, REGISTRY  # noqa: E402


def chopped_for_series(sid: str, entry: dict) -> tuple[list[str], list[str], pd.DataFrame] | None:
    """Build (row1_metadata, row2_ids, data) for one series, or None if no data."""
    final_csv = DATA_FINAL / f"{sid}.csv"
    if not final_csv.exists():
        return None
    df = pd.read_csv(final_csv)
    # Pivot subseries into columns
    pivot = df.pivot_table(index="year", columns="series_id", values="value", aggfunc="first")
    pivot = pivot.reset_index().sort_values("year")

    subseries = entry.get("subseries", {})
    units = entry.get("units", "")
    name = entry.get("name", "")
    status = entry.get("status", "")

    ids = ["Year"]
    metadata = [""]
    for col in [c for c in pivot.columns if c != "year"]:
        ids.append(col)
        ss_entry = subseries.get(col, {})
        source = ss_entry.get("source", "")
        period = ss_entry.get("period", "")
        meta = f"{name} — {source}; {units}; period={period}; series_status={status}"
        metadata.append(meta)

    return metadata, ids, pivot


def run() -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    CHOPPED_DIR.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    skipped: list[str] = []
    for sid, entry in reg["series"].items():
        result = chopped_for_series(sid, entry)
        if result is None:
            skipped.append(sid)
            continue
        metadata, ids, pivot = result
        out_path = CHOPPED_DIR / f"{sid}.csv"
        with out_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(metadata)
            w.writerow(ids)
            for _, row in pivot.iterrows():
                w.writerow([int(row["year"])] + [row[c] for c in pivot.columns if c != "year"])
        written.append(sid)

    print(f"    [O01] Chopped CSVs: wrote {len(written)} ({', '.join(written[:5])}{'...' if len(written) > 5 else ''}); skipped {len(skipped)}")
    return {"written": written, "skipped": skipped}


def generate_subsource_metadata(reg: dict) -> Path:
    """Generate SUBSOURCE_METADATA.json from the registry (v2.0 chopped requirement)."""
    metadata = {}
    for sid, entry in reg["series"].items():
        for ss_id, ss in entry.get("subseries", {}).items():
            metadata[ss_id] = {
                "series_id":    sid,
                "subseries_id": ss_id,
                "name":         ss.get("name", ""),
                "source":       ss.get("source", ""),
                "period":       ss.get("period", []),
                "units":        ss.get("units", entry.get("units", "")),
                "color":        ss.get("color", "#888888"),
                "is_component": False,
                "kind":         "subseries",
            }
    out = Path(__file__).resolve().parents[2] / "SUBSOURCE_METADATA.json"
    out.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_version": reg.get("version"),
        "entries": metadata,
    }, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    run()
    out = generate_subsource_metadata(reg)
    print(f"    [O01] SUBSOURCE_METADATA.json: {len(json.loads(out.read_text(encoding='utf-8'))['entries'])} entries")

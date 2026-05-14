"""S05 - Update PIPELINE_STATE.json.

Refreshes the timestamp and recomputes coverage-derived wave status from
ANU_LEDGER.json. Sets a wave's status to 'complete' iff every series in that
wave's frontier has all artifact types present.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "PIPELINE_STATE.json"
LEDGER = ROOT / "ANU_LEDGER.json"

ARTIFACT_KINDS = ("research", "dpr", "loader", "processor", "validator", "chopped", "extenbook")


def wave_status(frontier: list[str], artifacts: dict[str, dict[str, bool]]) -> str:
    if not frontier:
        return "not_applicable"
    covered = 0
    for sid in frontier:
        a = artifacts.get(sid, {})
        if all(a.get(k, False) for k in ARTIFACT_KINDS):
            covered += 1
    if covered == 0:
        return "not_started"
    if covered < len(frontier):
        return "in_progress"
    return "complete"


def run() -> dict:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if not LEDGER.exists():
        print("    [S05] WARN: ANU_LEDGER.json missing — run S02 first")
        return state
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    artifacts = ledger.get("artifacts", {})

    progress: dict[str, str] = {}
    for wave_key, wave_entry in state.get("wave_status", {}).items():
        if not isinstance(wave_entry, dict):
            continue
        frontier = wave_entry.get("frontier_series", [])
        if not frontier:
            progress[wave_key] = wave_entry.get("status", "not_started")
            continue
        new_status = wave_status(frontier, artifacts)
        old_status = wave_entry.get("status", "not_started")
        if new_status != old_status and old_status != "complete":
            wave_entry["status"] = new_status
        progress[wave_key] = wave_entry["status"]

    state["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"    [S05] Pipeline state refreshed. Wave statuses:")
    for k, v in progress.items():
        print(f"        {k}: {v}")
    return state


if __name__ == "__main__":
    run()

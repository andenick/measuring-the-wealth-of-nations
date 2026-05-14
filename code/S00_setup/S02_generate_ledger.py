"""S02 - Generate ANU_LEDGER.json.

Scans the Technical/ tree and reports per-series artifact coverage:
- research JSON (Technical/research/)
- DPR markdown (Technical/docs/series/)
- L## loader script (Technical/code/L01_loaders/)
- P## processor script (Technical/code/P02_processors/)
- V## validator script (Technical/code/V03_validators/)
- chopped CSV (Technical/chopped/)
- extenbook xlsx (Technical/extenbooks/)
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "series_registry.json"
LEDGER = ROOT / "ANU_LEDGER.json"


def has_research(sid: str) -> bool:
    return (ROOT / "research" / f"{sid}_research.json").exists()


def has_dpr(sid: str) -> bool:
    return (ROOT / "docs" / "series" / f"{sid}_DPR.md").exists()


def has_script(stage_dir: str, sid: str) -> bool:
    d = ROOT / "code" / stage_dir
    if not d.is_dir():
        return False
    return any(sid in p.name for p in d.glob("*.py"))


def has_chopped(sid: str) -> bool:
    return any((ROOT / "chopped").glob(f"{sid}*.csv"))


def has_extenbook(sid: str) -> bool:
    return any((ROOT / "extenbooks").glob(f"{sid}*.xlsx"))


def run() -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    series = reg.get("series", {})

    artifacts: dict[str, dict[str, bool]] = {}
    for sid in series:
        artifacts[sid] = {
            "research": has_research(sid),
            "dpr": has_dpr(sid),
            "loader": has_script("L01_loaders", sid),
            "processor": has_script("P02_processors", sid),
            "validator": has_script("V03_validators", sid),
            "chopped": has_chopped(sid),
            "extenbook": has_extenbook(sid),
        }

    coverage = {
        kind: sum(1 for a in artifacts.values() if a[kind])
        for kind in ("research", "dpr", "loader", "processor", "validator", "chopped", "extenbook")
    }
    n = len(series)
    ledger = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_version": reg.get("version"),
        "series_count": n,
        "coverage_counts": coverage,
        "coverage_pct": {k: round(100 * v / n, 1) if n else 0 for k, v in coverage.items()},
        "artifacts": artifacts,
    }
    LEDGER.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    print(f"    [S02] Ledger: {n} series; coverage = {ledger['coverage_pct']}")
    return ledger


if __name__ == "__main__":
    run()

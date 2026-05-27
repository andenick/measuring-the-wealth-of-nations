"""
RMWND Visualization -- Documentation Cascade Writer
Implements anu-visualize v6.0 cascade writes:
  - STEP_LOG.jsonl: action log entries
  - NARRATIVE.md: human-readable summary
  - ANU_LEDGER.json: visualization_coverage patch
  - PIPELINE_STATE.json: stage_7 block update

All paths are relative to Technical/ (one level above viz/).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

VIZ_DIR = Path(__file__).resolve().parent
TECHNICAL_DIR = VIZ_DIR.parent

STEP_LOG_PATH = TECHNICAL_DIR / "Build" / "STEP_LOG.jsonl"
NARRATIVE_PATH = TECHNICAL_DIR / "Build" / "BUILD_NARRATIVE.md"
LEDGER_PATH = TECHNICAL_DIR / "ANU_LEDGER.json"
PIPELINE_STATE_PATH = TECHNICAL_DIR / "PIPELINE_STATE.json"


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def append_step_log(action: str, details: dict = None):
    entry = {
        "timestamp": _now_iso(),
        "stage": 7,
        "stage_label": "VISUALIZATION",
        "action": action,
        "project": "measuring-wealth-of-nations-replication",
    }
    if details:
        entry.update(details)

    STEP_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STEP_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def write_visualization_narrative(gate: str, quality_results: dict):
    now = _now_iso()
    passed = sum(1 for r in quality_results.values() if r.get("passed"))
    total = len(quality_results)

    checklist_lines = []
    for qid in sorted(quality_results.keys(), key=lambda x: int(x[1:])):
        r = quality_results[qid]
        mark = "x" if r["passed"] else " "
        checklist_lines.append(f"- [{mark}] **{qid}**: {r['description']} — {r.get('detail', '')}")

    section = f"""
## Stage 7 — VISUALIZATION ({now})

**Gate:** {gate}
**Quality Score:** {passed}/{total}

### Quality Checklist
{chr(10).join(checklist_lines)}

"""
    narrative_path = TECHNICAL_DIR / "Build" / "BUILD_NARRATIVE.md"
    narrative_path.parent.mkdir(parents=True, exist_ok=True)

    if narrative_path.exists():
        existing = narrative_path.read_text(encoding="utf-8")
        if "## Stage 7" in existing:
            before = existing[:existing.index("## Stage 7")]
            after_idx = existing.find("\n## Stage ", existing.index("## Stage 7") + 10)
            after = existing[after_idx:] if after_idx > 0 else ""
            narrative_path.write_text(before + section + after, encoding="utf-8")
        else:
            with open(narrative_path, "a", encoding="utf-8") as f:
                f.write(section)
    else:
        narrative_path.write_text(f"# RMWND Build Narrative\n{section}", encoding="utf-8")


def patch_ledger(gate: str, quality_score: str):
    if not LEDGER_PATH.exists():
        return

    with open(LEDGER_PATH, encoding="utf-8") as f:
        ledger = json.load(f)

    if "project_summary" not in ledger:
        ledger["project_summary"] = {}

    ledger["project_summary"]["visualization_coverage"] = {
        "gate": gate,
        "quality_score": quality_score,
        "last_checked": _now_iso(),
        "frameworks": ["r-shiny", "plotly-dash"],
        "app_paths": ["Technical/viz/shiny/", "Technical/viz/dash/"],
    }

    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_pipeline_state(gate: str, quality_score: str):
    if not PIPELINE_STATE_PATH.exists():
        return

    with open(PIPELINE_STATE_PATH, encoding="utf-8") as f:
        state = json.load(f)

    now = _now_iso()
    stages = state.get("stages", {})
    stage_7 = stages.get("stage_7", {})

    stage_7["status"] = "complete" if gate in ("LAUNCH-READY", "DRAFT") else "in_progress"
    if not stage_7.get("started_at"):
        stage_7["started_at"] = now
    if gate in ("LAUNCH-READY", "DRAFT"):
        stage_7["completed_at"] = now
        stage_7["gate_passed"] = gate == "LAUNCH-READY"
    stage_7["quality_gate"] = gate
    stage_7["quality_score"] = quality_score
    stage_7["last_checked"] = now

    stages["stage_7"] = stage_7
    state["stages"] = stages

    with open(PIPELINE_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_full_cascade(action: str, gate: str, quality_results: dict):
    """Execute the complete documentation cascade for a viz action."""
    passed = sum(1 for r in quality_results.values() if r.get("passed"))
    total = len(quality_results)
    quality_score = f"{passed}/{total}"

    append_step_log(action, {
        "quality_gate": gate,
        "quality_score": quality_score,
        "checklist_passed": passed,
        "checklist_total": total,
    })

    write_visualization_narrative(gate, quality_results)
    patch_ledger(gate, quality_score)
    update_pipeline_state(gate, quality_score)

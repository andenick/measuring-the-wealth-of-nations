"""RMWND build orchestrator (Anu Framework v12.0).

A single-file CLI that wraps the 9-stage anu-build pipeline for the Measuring
the Wealth of Nations replication. Subcommands:

    status       Print PIPELINE_STATE stage table (gate marks, completion).
    advance      Identify and describe the next pipeline action (no execution).
    validate     Invoke anu-doctor project mode or run a manual audit.
    chopped      Regenerate Anu Chopped CSVs (delegates to O06_output/O01_*).
    extenbooks   Regenerate Anu Extenbook workbooks (delegates to O06_output/O02_*).
    ledger       Regenerate ANU_LEDGER.json (mimic S00_setup/S02_generate_ledger).
    viz          Run viz quality checker (delegates to viz/check_quality.py).
    review       Summarise latest Handoffs/ANU_REVIEW_*.md.
    help         Print this help.

State-changing subcommands (advance, chopped, extenbooks, ledger) append a
STEP_LOG entry to Build/STEP_LOG.jsonl. Read-only subcommands do not.

Run with:
    python build.py <subcommand>
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TECHNICAL = Path(__file__).resolve().parent
PROJECT_ROOT = TECHNICAL.parent
PIPELINE_STATE_PATH = TECHNICAL / "PIPELINE_STATE.json"
STEP_LOG_PATH = TECHNICAL / "Build" / "STEP_LOG.jsonl"
HANDOFFS_DIR = TECHNICAL / "Handoffs"
LEDGER_PATH = TECHNICAL / "ANU_LEDGER.json"
REGISTRY_PATH = TECHNICAL / "series_registry.json"

CHOPPED_SCRIPT = TECHNICAL / "code" / "O06_output" / "O01_generate_chopped.py"
EXTENBOOK_SCRIPT = TECHNICAL / "code" / "O06_output" / "O02_generate_extenbook.py"
VIZ_QUALITY_SCRIPT = TECHNICAL / "viz" / "check_quality.py"
LEDGER_GENERATOR = TECHNICAL / "code" / "S00_setup" / "S02_generate_ledger.py"
ANU_DOCTOR_PATH = Path("<workspace>/anu-doctor/check_project.py")

STAGE_ORDER = [
    "stage_0", "stage_1", "stage_2", "stage_3",
    "stage_4", "stage_5", "stage_6", "stage_7", "stage_8",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def load_pipeline_state() -> dict:
    return json.loads(PIPELINE_STATE_PATH.read_text(encoding="utf-8"))


def append_step_log(step_id: str, action: str, stage: int, inputs: list[str],
                    outputs: list[str], outcome: str, notes: str) -> None:
    STEP_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": utc_now_iso(),
        "step_id": step_id,
        "mode": "execute",
        "stage": stage,
        "cohort": None,
        "series": None,
        "action": action,
        "inputs": inputs,
        "outputs": outputs,
        "doctor_check_ids": [],
        "outcome": outcome,
        "artifacts_emitted": [Path(o).name for o in outputs],
        "notes": notes,
    }
    with STEP_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_python(script: Path, args: list[str] | None = None) -> int:
    """Run a Python script in foreground; return its exit code."""
    args = args or []
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(script.parent),
        env=env,
    )
    return proc.returncode


def gate_mark(stage: dict) -> str:
    status = stage.get("status", "unknown")
    if status == "complete" and stage.get("gate_passed") is True:
        return "PASS"
    if status == "complete_with_waiver":
        return "WAIVER"
    if status == "complete" and stage.get("gate_passed") is False:
        return "WAIVER"
    if status == "in_progress":
        return "WIP"
    if status == "not_started":
        return "-"
    return "FAIL"


# ---------------------------------------------------------------------------
# Subcommand: status
# ---------------------------------------------------------------------------

def cmd_status() -> int:
    state = load_pipeline_state()
    stages = state.get("stages", {})

    print(f"Project          : {state.get('project', '?')}")
    print(f"Schema           : {state.get('schema_version', '?')}")
    print(f"Last updated     : {state.get('last_updated', '?')}")
    print(f"Current stage    : {state.get('current_stage', '?')}")
    print()
    header = f"{'Stage':<10} {'Label':<16} {'Status':<22} {'Gate':<7} {'Done':<8} {'Note'}"
    print(header)
    print("-" * len(header))
    for key in STAGE_ORDER:
        s = stages.get(key, {})
        label = s.get("label", "?")
        status = s.get("status", "?")
        mark = gate_mark(s)
        complete = s.get("series_complete", 0)
        total = s.get("series_total", 0)
        done = f"{complete}/{total}" if total else "-"
        note = (s.get("gate_passed_note") or s.get("waiver") or "")
        note = note.replace("\n", " ")
        if len(note) > 60:
            note = note[:57] + "..."
        print(f"{key:<10} {label:<16} {status:<22} {mark:<7} {done:<8} {note}")
    print()
    # Roll-up
    n_pass = sum(1 for k in STAGE_ORDER if gate_mark(stages.get(k, {})) == "PASS")
    n_waiver = sum(1 for k in STAGE_ORDER if gate_mark(stages.get(k, {})) == "WAIVER")
    n_total = len(STAGE_ORDER)
    print(f"Summary: {n_pass} PASS / {n_waiver} WAIVER / {n_total} total")
    audit = state.get("framework_audit", {})
    if audit:
        print(f"anu-doctor       : {audit.get('anu_doctor_status', '?')} "
              f"({audit.get('anu_doctor_version', '?')}, "
              f"last {audit.get('anu_doctor_last_run', '?')})")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: advance
# ---------------------------------------------------------------------------

def cmd_advance() -> int:
    state = load_pipeline_state()
    stages = state.get("stages", {})

    # Identify next stage not complete (and not complete_with_waiver)
    next_stage_key = None
    for key in STAGE_ORDER:
        s = stages.get(key, {})
        status = s.get("status", "not_started")
        if status not in ("complete", "complete_with_waiver"):
            next_stage_key = key
            break

    if next_stage_key is None:
        print("All 9 stages are complete (or complete_with_waiver).")
        print("Next action: clear waivers (see PIPELINE_STATE waiver notes), then run anu-review")
        print("for strict-gate verification, then publish v1.1.")
        plan_note = "all_stages_complete"
    else:
        s = stages[next_stage_key]
        label = s.get("label", "?")
        status = s.get("status", "?")
        print(f"Next stage   : {next_stage_key} ({label})")
        print(f"Status now   : {status}")
        print()
        print("What would happen next:")
        print(f"  1. Invoke the anu-{label.lower()} skill (or its sub-skills) for {next_stage_key}.")
        print(f"  2. Run the corresponding stage scripts under code/ (search for matching prefix).")
        print(f"  3. Update PIPELINE_STATE.stages.{next_stage_key} on completion.")
        print(f"  4. Append a STEP_LOG entry with stage={next_stage_key[-1]} and outcome=pass.")
        print()
        print("This subcommand does NOT execute the stage. Invoke the skill manually.")
        plan_note = f"next={next_stage_key}/{label}"

    append_step_log(
        step_id=f"build-advance-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        action="advance_plan",
        stage=state.get("current_stage", 0),
        inputs=["Technical/PIPELINE_STATE.json", "Technical/Build/STEP_LOG.jsonl"],
        outputs=[],
        outcome="pass",
        notes=f"build.py advance: {plan_note}",
    )
    return 0


# ---------------------------------------------------------------------------
# Subcommand: validate (anu-doctor or manual audit)
# ---------------------------------------------------------------------------

def cmd_validate() -> int:
    if ANU_DOCTOR_PATH.exists():
        print(f"Invoking anu-doctor at {ANU_DOCTOR_PATH}")
        print(f"Project root: {TECHNICAL}")
        rc = run_python(ANU_DOCTOR_PATH, ["--project", str(TECHNICAL)])
        return rc

    print("anu-doctor check_project.py not found at expected location; running manual audit.")
    print(f"  Expected: {ANU_DOCTOR_PATH}")
    print()
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    series = reg.get("series", {})
    print(f"Registry series count          : {len(series)}")
    print(f"Pipeline state present         : {PIPELINE_STATE_PATH.exists()}")
    print(f"ANU_LEDGER.json present        : {LEDGER_PATH.exists()}")
    print(f"STEP_LOG.jsonl present         : {STEP_LOG_PATH.exists()}")
    print(f"O01_generate_chopped.py present: {CHOPPED_SCRIPT.exists()}")
    print(f"O02_generate_extenbook.py      : {EXTENBOOK_SCRIPT.exists()}")
    print(f"viz/check_quality.py present   : {VIZ_QUALITY_SCRIPT.exists()}")
    missing = [k for k in ("PIPELINE_STATE.json", "ANU_LEDGER.json", "series_registry.json")
               if not (TECHNICAL / k).exists()]
    if missing:
        print(f"MISSING: {missing}")
        return 1
    print()
    print("Manual audit: OK (artifacts present). Install anu-doctor for the full P01-P39 sweep.")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: chopped
# ---------------------------------------------------------------------------

def cmd_chopped() -> int:
    if not CHOPPED_SCRIPT.exists():
        print(f"ERROR: chopped generator missing at {CHOPPED_SCRIPT}", file=sys.stderr)
        return 2
    rc = run_python(CHOPPED_SCRIPT)
    outcome = "pass" if rc == 0 else "fail"
    append_step_log(
        step_id=f"build-chopped-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        action="regenerate_chopped",
        stage=6,
        inputs=["Technical/series_registry.json", "Technical/data/final/"],
        outputs=["Technical/chopped/", "Technical/SUBSOURCE_METADATA.json"],
        outcome=outcome,
        notes=f"build.py chopped wrapper -> O01_generate_chopped.py (rc={rc})",
    )
    return rc


# ---------------------------------------------------------------------------
# Subcommand: extenbooks
# ---------------------------------------------------------------------------

def cmd_extenbooks() -> int:
    if not EXTENBOOK_SCRIPT.exists():
        print(f"ERROR: extenbook generator missing at {EXTENBOOK_SCRIPT}", file=sys.stderr)
        return 2
    rc = run_python(EXTENBOOK_SCRIPT)
    outcome = "pass" if rc == 0 else "fail"
    append_step_log(
        step_id=f"build-extenbooks-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        action="regenerate_extenbooks",
        stage=6,
        inputs=["Technical/series_registry.json", "Technical/data/final/", "Technical/docs/series/"],
        outputs=["Technical/extenbooks/"],
        outcome=outcome,
        notes=f"build.py extenbooks wrapper -> O02_generate_extenbook.py (rc={rc})",
    )
    return rc


# ---------------------------------------------------------------------------
# Subcommand: ledger
# ---------------------------------------------------------------------------

def cmd_ledger() -> int:
    """Regenerate ANU_LEDGER.json, preferring the canonical S02 generator."""
    if LEDGER_GENERATOR.exists():
        rc = run_python(LEDGER_GENERATOR)
        outcome = "pass" if rc == 0 else "fail"
        append_step_log(
            step_id=f"build-ledger-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            action="regenerate_ledger",
            stage=0,
            inputs=["Technical/series_registry.json"],
            outputs=["Technical/ANU_LEDGER.json"],
            outcome=outcome,
            notes=f"build.py ledger wrapper -> S02_generate_ledger.py (rc={rc})",
        )
        return rc

    # Fallback: inline implementation mirroring S02 (iteration 15 logic)
    print(f"S02_generate_ledger.py not found at {LEDGER_GENERATOR}; using inline fallback.")
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    series = reg.get("series", {})

    def _has(p: Path) -> bool:
        return p.exists()

    def _has_script(stage_dir: str, sid: str) -> bool:
        d = TECHNICAL / "code" / stage_dir
        if not d.is_dir():
            return False
        return any(sid in p.name for p in d.glob("*.py"))

    artifacts = {}
    for sid in series:
        artifacts[sid] = {
            "research":  _has(TECHNICAL / "research" / f"{sid}_research.json"),
            "dpr":       _has(TECHNICAL / "docs" / "series" / f"{sid}_DPR.md"),
            "loader":    _has_script("L01_loaders", sid),
            "processor": _has_script("P02_processors", sid),
            "validator": _has_script("V03_validators", sid),
            "chopped":   any((TECHNICAL / "chopped").glob(f"{sid}*.csv")),
            "extenbook": any((TECHNICAL / "extenbooks").glob(f"{sid}*.xlsx")),
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
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    print(f"  ANU_LEDGER.json regenerated: {n} series; coverage = {ledger['coverage_pct']}")

    append_step_log(
        step_id=f"build-ledger-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        action="regenerate_ledger",
        stage=0,
        inputs=["Technical/series_registry.json"],
        outputs=["Technical/ANU_LEDGER.json"],
        outcome="pass",
        notes="build.py ledger inline fallback (S02 generator missing)",
    )
    return 0


# ---------------------------------------------------------------------------
# Subcommand: viz
# ---------------------------------------------------------------------------

def cmd_viz() -> int:
    if not VIZ_QUALITY_SCRIPT.exists():
        print(f"ERROR: viz/check_quality.py missing at {VIZ_QUALITY_SCRIPT}", file=sys.stderr)
        return 2
    rc = run_python(VIZ_QUALITY_SCRIPT, ["--json", "--no-cascade"])
    # Read back PIPELINE_STATE viz block for a one-line summary
    try:
        state = load_pipeline_state()
        s7 = state.get("stages", {}).get("stage_7", {})
        print()
        print(f"quality_gate  : {s7.get('quality_gate', '?')}")
        print(f"quality_score : {s7.get('quality_score', '?')}")
        print(f"last_checked  : {s7.get('last_checked', '?')}")
    except Exception as exc:
        print(f"[WARN] could not read PIPELINE_STATE summary: {exc}")
    return rc


# ---------------------------------------------------------------------------
# Subcommand: review
# ---------------------------------------------------------------------------

def cmd_review() -> int:
    if not HANDOFFS_DIR.is_dir():
        print(f"No Handoffs directory at {HANDOFFS_DIR}")
        return 1
    reviews = sorted(HANDOFFS_DIR.glob("ANU_REVIEW_*.md"))
    if not reviews:
        print("No ANU_REVIEW_*.md handoff documents found.")
        return 1
    latest = reviews[-1]
    print(f"Latest ANU_REVIEW: {latest.name}")
    text = latest.read_text(encoding="utf-8", errors="replace")

    # Extract a handful of structured fields heuristically
    def first_match(pattern: str) -> str:
        m = re.search(pattern, text, re.MULTILINE)
        return m.group(1).strip() if m else "(not found)"

    integration = first_match(r"Integration Score[^*\n]*\*\*\s*=\s*[0-9.+\s]*\*\*([0-9.]+\s*/\s*100)\*\*")
    if integration == "(not found)":
        integration = first_match(r"Integration Score[^\n]*?([0-9]+\.[0-9]+\s*/\s*100)")
    d13 = first_match(r"D13 score:\s*([0-9.]+\s*/\s*100)")
    d14 = first_match(r"D14 score:\s*([0-9.]+\s*/\s*100)")
    verdict = first_match(r"VERDICT\*\*?\s*:\s*\*?\*?([A-Z_\- ]+)")

    print()
    print(f"Integration Score (D1-D12): {integration}")
    print(f"D13 Data Authenticity     : {d13}")
    print(f"D14 Intelligibility       : {d14}")
    print(f"Verdict                   : {verdict}")
    print()
    # Print the first 25 non-empty lines as a quick excerpt
    lines = [ln for ln in text.splitlines() if ln.strip()]
    print("Excerpt (first 25 substantive lines):")
    print("-" * 60)
    for ln in lines[:25]:
        print(ln)
    return 0


# ---------------------------------------------------------------------------
# Subcommand: help
# ---------------------------------------------------------------------------

def cmd_help() -> int:
    print(__doc__)
    print("Subcommands:")
    for name in SUBCOMMANDS:
        print(f"  python build.py {name}")
    return 0


SUBCOMMANDS = {
    "status":     cmd_status,
    "advance":    cmd_advance,
    "validate":   cmd_validate,
    "chopped":    cmd_chopped,
    "extenbooks": cmd_extenbooks,
    "ledger":     cmd_ledger,
    "viz":        cmd_viz,
    "review":     cmd_review,
    "help":       cmd_help,
}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        cmd_help()
        return 1
    sub = argv[1].lower().lstrip("-")
    fn = SUBCOMMANDS.get(sub)
    if fn is None:
        print(f"Unknown subcommand: {sub!r}", file=sys.stderr)
        cmd_help()
        return 2
    try:
        return fn()
    except Exception as exc:
        print(f"ERROR in subcommand {sub!r}: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))

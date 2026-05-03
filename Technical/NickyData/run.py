#!/usr/bin/env python3
"""AS2 NickyData Pipeline v6.0 — Master Orchestrator

8-phase pipeline: Setup → Load → Process → Validate → Manual → Analyze → Output

Usage:
    python run.py                    # Full: S → L → P → V → A → O
    python run.py --setup-only       # Just S##
    python run.py --load-only        # Just L##
    python run.py --from P           # Resume from processing
    python run.py --validate-only    # Just V##
    python run.py --analyze-only     # Just A##
    python run.py --full             # All phases including M (manual)
    python run.py --dry-run          # Show plan
    python run.py --report           # Status from last run
    python run.py --list             # List all scripts
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add NickyData root to path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

VERSION = "6.0.0"

PHASES = [
    ("setup", "S", "Setup"),
    ("loading", "L", "Loading"),
    ("processing", "P", "Processing"),
    ("validation", "V", "Validation"),
    ("manual", "M", "Manual Adjustment"),
    ("analysis", "A", "Analysis"),
    ("outputs", "O", "Output"),
    ("exploration", "E", "Exploration"),
]


def _discover_scripts(phase_dir: str, prefix: str) -> list[Path]:
    """Find all XX## scripts in a phase directory, excluding orchestrators."""
    code_dir = ROOT / "code" / phase_dir
    if not code_dir.exists():
        return []
    pattern = f"{prefix}[0-9][0-9]_*.py"
    scripts = sorted(code_dir.glob(pattern))
    # Exclude orchestrators (XX00_*)
    return [s for s in scripts if not s.name.startswith(f"{prefix}00_")]


def _run_phase(phase_dir: str, prefix: str, phase_name: str) -> list[dict]:
    """Discover and execute all scripts in a phase."""
    scripts = _discover_scripts(phase_dir, prefix)
    if not scripts:
        return []

    print(f"\n  -- {phase_name} Phase ({len(scripts)} scripts) --")
    results = []

    for script in scripts:
        module_name = script.stem
        spec = importlib.util.spec_from_file_location(module_name, script)
        mod = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(mod)
            # Try common entry points
            if hasattr(mod, "validate"):
                result = mod.validate()
            elif hasattr(mod, "process"):
                result = mod.process()
            elif hasattr(mod, "load"):
                result = mod.load()
            elif hasattr(mod, "adjust"):
                result = mod.adjust()
            elif hasattr(mod, "generate"):
                result = mod.generate()
            elif hasattr(mod, "run"):
                result = mod.run()
            else:
                result = {"status": "skip", "message": f"No entry point found in {module_name}"}
        except Exception as exc:
            result = {"status": "fail", "message": f"Error: {exc}"}
            print(f"    {module_name}: FAIL - {exc}")

        # Print result summary
        status = result.get("status", "?") if isinstance(result, dict) else "?"
        summary = result.get("summary", result.get("message", "")) if isinstance(result, dict) else ""
        if status == "fail":
            print(f"    {module_name}: FAIL - {summary}")
        elif summary and prefix in ("V", "A"):
            print(f"    {module_name}: {summary}")

        results.append(result)

    # Print phase summary for validation
    if prefix == "V" and results:
        total_pass = sum(r.get("summary", {}).get("pass", 0) if isinstance(r.get("summary"), dict)
                        else str(r.get("summary", "")).count("PASS")
                        for r in results if isinstance(r, dict))
        total_fail = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "fail")
        print(f"\n  Validation: {len(results)} validators ran, {total_fail} failures")

    return results


def _print_report():
    """Print pipeline status dashboard."""
    import json as _json
    print(f"\n  AS2 NickyData Status Report v{VERSION}")
    print(f"  {'=' * 40}")

    # Count scripts
    total_scripts = sum(len(_discover_scripts(d, p)) for d, p, _ in PHASES)
    print(f"  Scripts: {total_scripts} across {len(PHASES)} phases")

    # Count series
    book_dir = ROOT / "data" / "final-data" / "book" / "series"
    study_dir = ROOT / "data" / "final-data" / "studies" / "series"
    n_book = len(list(book_dir.glob("T*.csv"))) if book_dir.exists() else 0
    n_study = len(list(study_dir.glob("N*.csv"))) if study_dir.exists() else 0
    print(f"  Series: {n_book} book + {n_study} studies = {n_book + n_study} total")

    # Validators
    n_validators = len(_discover_scripts("validation", "V"))
    print(f"  Validators: {n_validators}")

    # Vintage
    vlog = ROOT / "data" / "user-inputs" / "DATA_VINTAGE_LOG.json"
    if vlog.exists():
        with open(vlog) as f:
            v = _json.load(f)
        n_sources = len(v.get("sources", {}))
        print(f"  Data sources: {n_sources} documented")

    # Registry
    reg = ROOT / "project_registry.json"
    if reg.exists():
        with open(reg) as f:
            r = _json.load(f)
        n_ch = len(r.get("book_replication", {}).get("chapters", {}))
        n_st = len(r.get("studies", {}))
        print(f"  Registry: {n_ch} chapters + {n_st} studies")

    print()


def _test_all():
    """Run full pipeline and verify results."""
    print(f"\n  AS2 NickyData Test Suite v{VERSION}")
    print(f"  {'=' * 40}")

    from utils.paths import ensure_dirs, SERIES_OUT, STUDIES_OUT
    ensure_dirs()

    t0 = time.time()
    passes = 0
    fails = 0

    # Run all phases
    for phase_dir, prefix, name in PHASES:
        if prefix == "E":
            continue  # Skip exploration
        results = _run_phase(phase_dir, prefix, name)
        for r in results:
            if isinstance(r, dict) and r.get("status") == "fail":
                fails += 1

    # Check series count
    n_book = len(list(SERIES_OUT.glob("T*.csv")))
    n_study = len(list(STUDIES_OUT.glob("N*.csv")))
    total = n_book + n_study
    if total >= 40:
        passes += 1
        print(f"\n  CHECK: Series count {total} >= 40: PASS")
    else:
        fails += 1
        print(f"\n  CHECK: Series count {total} < 40: FAIL")

    elapsed = time.time() - t0
    status = "PASS" if fails == 0 else f"FAIL ({fails} failures)"
    print(f"\n  TEST RESULT: {status} ({elapsed:.1f}s)")


def main():
    parser = argparse.ArgumentParser(description=f"AS2 NickyData Pipeline v{VERSION}")
    parser.add_argument("--setup-only", action="store_true")
    parser.add_argument("--load-only", action="store_true")
    parser.add_argument("--from", dest="from_phase", metavar="PHASE")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--full", action="store_true", help="Include manual adjustment phase")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--test-all", action="store_true", help="Run full pipeline + verify")
    args = parser.parse_args()

    print(f"\n  AS2 NickyData Pipeline v{VERSION}")
    print(f"  {'=' * 40}")

    if args.report:
        _print_report()
        return

    if args.test_all:
        _test_all()
        return

    if args.list or args.dry_run:
        total = 0
        for phase_dir, prefix, name in PHASES:
            scripts = _discover_scripts(phase_dir, prefix)
            if scripts:
                print(f"\n  {name} ({prefix}##): {len(scripts)} scripts")
                for s in scripts:
                    print(f"    {s.stem}")
                total += len(scripts)
        print(f"\n  Total: {total} scripts across {len(PHASES)} phases")
        return

    # Determine which phases to run
    from utils.paths import ensure_dirs
    ensure_dirs()

    t0 = time.time()

    # Default: S → L → P → V → A → O (skip M and E)
    phase_map = {
        "S": not any([args.load_only, args.validate_only, args.analyze_only]),
        "L": not any([args.setup_only, args.validate_only, args.analyze_only]),
        "P": not any([args.setup_only, args.load_only, args.validate_only, args.analyze_only]),
        "V": not any([args.setup_only, args.load_only, args.analyze_only]),
        "M": args.full,
        "A": not any([args.setup_only, args.load_only, args.validate_only]),
        "O": not any([args.setup_only, args.load_only, args.validate_only, args.analyze_only]),
        "E": False,  # Never auto-run exploration
    }

    # Handle --from
    if args.from_phase:
        started = False
        for _, prefix, _ in PHASES:
            if prefix == args.from_phase.upper():
                started = True
            if not started:
                phase_map[prefix] = False

    # Handle --*-only flags
    if args.setup_only:
        phase_map = {k: (k == "S") for k in phase_map}
    if args.load_only:
        phase_map = {k: (k == "L") for k in phase_map}
    if args.validate_only:
        phase_map = {k: (k == "V") for k in phase_map}
    if args.analyze_only:
        phase_map = {k: (k == "A") for k in phase_map}

    # Run phases
    for phase_dir, prefix, name in PHASES:
        if phase_map.get(prefix, False):
            _run_phase(phase_dir, prefix, name)

    elapsed = time.time() - t0
    print(f"\n  -- Complete ({elapsed:.1f}s) --")


if __name__ == "__main__":
    main()

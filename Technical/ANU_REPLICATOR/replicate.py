#!/usr/bin/env python3
"""
Anu Replicator v3.0 — Master Orchestrator (AS2)

Four-phase pipeline: Loading (L##) → Processing (P##) → Validation (V##) → Manual Adjustment (M##)
Reproduces all data series from *Measuring the Wealth of Nations* (Shaikh & Tonak, 1994).

Usage:
    python replicate.py                   # full pipeline (L + P + V)
    python replicate.py --load-only       # loading phase only
    python replicate.py --process-only    # processing phase only
    python replicate.py --validate-only   # validation phase only (requires prior P run)
    python replicate.py --manual-only     # manual adjustment phase only
    python replicate.py --skip-validation # run L + P, skip V
    python replicate.py --skip-manual     # run L + P + V, skip M (default)
    python replicate.py --full            # all four phases: L + P + V + M
    python replicate.py --series T506 T511
    python replicate.py --chapter 5
    python replicate.py --dry-run         # show plan, don't execute
    python replicate.py --report          # generate report only
    python replicate.py --ledger          # regenerate ANU_LEDGER.json
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load API keys from config/api_keys.env if present
_ENV_FILE = Path(__file__).resolve().parent / "config" / "api_keys.env"
if _ENV_FILE.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_ENV_FILE, override=False)
    except ImportError:
        with open(_ENV_FILE, encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

from lib.paths import ensure_dirs, REGISTRY, REPORTS, SHINY_OUT, FIGURES_OUT, SHINY_CATALOG, SCRIPTS_VALIDATION, SCRIPTS_MANUAL
from lib.config_loader import load_registry, validate_registry
from lib.registry_reader import get_all_series_ids, get_series_for_chapter
from lib.reporting.console_reporter import (
    print_banner,
    print_load_summary,
    print_process_summary,
)
from lib.formats.report_generator import generate_replication_report

VERSION = "3.0.0"


def _read_version() -> str:
    vf = Path(__file__).resolve().parent / "VERSION"
    if vf.exists():
        return vf.read_text(encoding="utf-8").strip()
    return VERSION


def _resolve_series_filter(args, registry):
    """Build a list of series IDs from --series / --chapter, or None for all."""
    if args.series:
        return args.series
    if args.chapter is not None:
        ids = get_series_for_chapter(registry, args.chapter)
        if not ids:
            print(f"  No series found for chapter {args.chapter}.")
            sys.exit(1)
        return ids
    return None


def _dry_run(registry, series_filter, args):
    """Print what would be executed without doing anything."""
    all_ids = series_filter or get_all_series_ids(registry)
    print(f"\n  Dry-run: {len(all_ids)} series would be processed\n")

    # Show pipeline phases
    phases = []
    if not args.validate_only and not args.manual_only:
        if not args.process_only:
            phases.append("Loading (L##)")
        if not args.load_only:
            phases.append("Processing (P##)")
    if not args.load_only and not args.skip_validation:
        phases.append("Validation (V##)")
    if args.full or args.manual_only:
        phases.append("Manual Adjustment (M##)")

    print(f"  Pipeline phases: {' → '.join(phases)}\n")

    # Show V## scripts
    v_scripts = sorted(SCRIPTS_VALIDATION.glob("V[0-9][0-9]_*.py"))
    v_scripts = [s for s in v_scripts if s.name != "V00_validate_all.py"]
    if v_scripts and "Validation" in " ".join(phases):
        print(f"  Validation scripts: {len(v_scripts)}")
        for s in v_scripts:
            print(f"    {s.stem}")
        print()

    # Show M## scripts
    m_scripts = sorted(SCRIPTS_MANUAL.glob("M[0-9][0-9]_*.py"))
    m_scripts = [s for s in m_scripts if s.name != "M00_apply_adjustments.py"]
    if m_scripts and "Manual" in " ".join(phases):
        print(f"  Manual adjustment scripts: {len(m_scripts)}")
        for s in m_scripts:
            print(f"    {s.stem}")
        print()

    for sid in all_ids:
        entry = registry["series"].get(sid, {})
        name = entry.get("name", "?")
        n_sub = len(entry.get("subseries", {}))
        n_steps = len(entry.get("construction", []))
        ext = "yes" if entry.get("extension") else "no"
        print(f"    {sid}  {name}")
        print(f"           {n_sub} subseries, {n_steps} construction steps, extension: {ext}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Anu Replicator v3.0 — reproduce AS2 data series",
    )
    parser.add_argument("--load-only", action="store_true", help="Run loading phase only")
    parser.add_argument("--process-only", action="store_true", help="Run processing phase only")
    parser.add_argument("--validate-only", action="store_true", help="Run validation phase only")
    parser.add_argument("--manual-only", action="store_true", help="Run manual adjustment phase only")
    parser.add_argument("--skip-validation", action="store_true", help="Skip validation phase")
    parser.add_argument("--skip-manual", action="store_true", help="Skip manual adjustment phase (default)")
    parser.add_argument("--full", action="store_true", help="Run all four phases: L + P + V + M")
    parser.add_argument("--series", nargs="+", metavar="ID", help="Process specific series IDs")
    parser.add_argument("--chapter", type=int, help="Process all series for a chapter")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    parser.add_argument("--report", action="store_true", help="Generate report from last run")
    parser.add_argument("--ledger", action="store_true", help="Regenerate ANU_LEDGER.json after pipeline")
    args = parser.parse_args()

    version = _read_version()

    # Load and validate registry
    try:
        registry = load_registry()
    except FileNotFoundError as exc:
        print(f"\n  ERROR: {exc}\n")
        sys.exit(1)

    errors = validate_registry(registry)
    if errors:
        print("\n  Registry validation warnings:")
        for e in errors:
            print(f"    - {e}")
        print()

    print_banner(version, registry)
    series_filter = _resolve_series_filter(args, registry)

    if args.dry_run:
        _dry_run(registry, series_filter, args)
        return

    ensure_dirs()

    # Import phase runners here so paths are resolved after ensure_dirs()
    t0 = time.time()
    load_results = []
    process_results = []
    validation_report = None

    # Determine which phases to run
    run_load = (not args.process_only and not args.validate_only
                and not args.manual_only and not args.report)
    run_process = (not args.load_only and not args.validate_only
                   and not args.manual_only and not args.report)
    run_validate = (not args.load_only and not args.skip_validation
                    and not args.report
                    and (args.validate_only or args.full or run_process))
    run_manual = (args.full or args.manual_only) and not args.report

    # ── Loading phase ─────────────────────────────────────────
    if run_load:
        from scripts.loading.L00_load_all_data import run_all as run_loading
        print("  ── Loading Phase ──────────────────────────────────")
        try:
            load_results = run_loading(series_filter=series_filter)
        except Exception as exc:
            print(f"\n  FATAL during loading: {exc}\n")
            if args.load_only:
                sys.exit(1)
            print("  Attempting processing phase anyway...\n")

    # ── Processing phase ──────────────────────────────────────
    if run_process and not args.load_only:
        from scripts.processing.P00_process_all_data import run_all as run_processing
        print("  ── Processing Phase ───────────────────────────────")
        try:
            process_results = run_processing(series_filter=series_filter)
        except Exception as exc:
            print(f"\n  FATAL during processing: {exc}\n")
            sys.exit(1)

    # ── Shiny export phase ─────────────────────────────────────
    if not args.load_only and process_results:
        from lib.formats.shiny_writer import write_chapter_csv, write_series_catalog, write_figure_column_map

        print("  ── Shiny Export Phase ──────────────────────────────")
        chapters_processed: set[int] = set()
        for r in process_results:
            ch = registry["series"].get(r["series_id"], {}).get("chapter")
            if ch is not None:
                chapters_processed.add(ch)

        for ch in sorted(chapters_processed):
            write_chapter_csv(ch, process_results, registry, SHINY_OUT)

        write_series_catalog(
            registry, process_results, SHINY_OUT,
            existing_catalog_path=SHINY_CATALOG if SHINY_CATALOG.exists() else None,
        )

        if registry.get("figures"):
            write_figure_column_map(registry, SHINY_OUT)

    # ── Figure export phase ────────────────────────────────────
    if not args.load_only and process_results and registry.get("figures"):
        from lib.formats.figure_writer import write_all_figures

        print("  ── Figure Export Phase ─────────────────────────────")
        write_all_figures(registry, process_results, FIGURES_OUT)

    # ── Validation phase ─────────────────────────────────────
    if run_validate:
        print("  ── Validation Phase ───────────────────────────────")
        try:
            from scripts.validation.V00_validate_all import run_validation
            validation_report = run_validation(
                series_filter=series_filter,
                chapter_filter=args.chapter,
            )
        except Exception as exc:
            print(f"\n  Validation error: {exc}\n")
            validation_report = None

    # ── Manual adjustment phase ───────────────────────────────
    if run_manual:
        print("  ── Manual Adjustment Phase ────────────────────────")
        try:
            from scripts.manual.M00_apply_adjustments import run_all as run_adjustments
            run_adjustments(series_filter=series_filter)
        except Exception as exc:
            print(f"\n  Manual adjustment error: {exc}\n")

    # ── Report generation ─────────────────────────────────────
    if args.report or process_results:
        report_path = generate_replication_report(
            process_results,
            REPORTS,
            title="Anu Replication Report — AS2",
            version=version,
        )
        print(f"  Report written to {report_path}")

    # ── Ledger regeneration ──────────────────────────────────
    if args.ledger or (process_results and not args.load_only):
        try:
            from scripts.utils.ledger_generator import generate_ledger, write_ledger
            print("  ── Ledger Update ──────────────────────────────────")
            ledger = generate_ledger()
            ledger_path = write_ledger(ledger)
            health = ledger["project_summary"]["documentation_health"]
            n_items = len(ledger["action_items"])
            print(f"     Health: {health}% | Action items: {n_items}")
            print(f"     Written to {ledger_path}")
        except Exception as exc:
            print(f"     Ledger generation failed: {exc}")

    elapsed = time.time() - t0
    n_load = len(load_results)
    n_proc = len(process_results)
    load_ok = sum(1 for r in load_results if r.get("status") == "ok")
    proc_ok = sum(1 for r in process_results if r.get("status") == "ok")

    print()
    print(f"  ── Complete ({elapsed:.1f}s) ──────────────────────────")
    if load_results:
        print(f"     Loaded:    {load_ok}/{n_load} series")
    if process_results:
        print(f"     Processed: {proc_ok}/{n_proc} series")
    if validation_report:
        vs = validation_report.get("summary", {})
        print(f"     Validated: {vs.get('pass', 0)} PASS, {vs.get('fail', 0)} FAIL, "
              f"{vs.get('warn', 0)} WARN — {vs.get('overall', '?')}")
    print()


if __name__ == "__main__":
    main()

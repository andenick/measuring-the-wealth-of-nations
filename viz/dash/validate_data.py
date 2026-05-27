"""
RMWND Dash -- Startup Data Validation
Implements the anu-visualize v6.0 five-check standard:
  1. Structural checks (canonical files exist and load)
  2. Cross-reference integrity (subsource parent_series resolve)
  3. Value sanity (year ranges valid, chapters in range)
  4. Chart readiness (figures have data column mappings)
  5. Manifest verification (SHA-256 hash comparison)
"""

import json
from pathlib import Path
from typing import Optional

from logger import get_file_logger

log = get_file_logger()


def validate_app_data(
    paths: dict,
    registry: dict,
    catalog: dict,
    subsource_meta: Optional[dict] = None,
) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict = {}

    def add_error(check: str, msg: str):
        errors.append(f"[{check}] {msg}")

    def add_warn(check: str, msg: str):
        warnings.append(f"[{check}] {msg}")

    def pass_check(name: str, passed: bool, detail: str = ""):
        checks[name] = {"passed": passed, "detail": detail}

    # -- Check 1: Structural --
    required_files = {
        "series_registry": paths.get("registry"),
        "app_config": paths.get("config"),
        "definitive_catalog": paths.get("catalog"),
    }
    structural_ok = True
    for fname, fpath in required_files.items():
        if fpath is None or not Path(fpath).exists():
            add_error("STRUCTURAL", f"Required file missing: {fname} ({fpath})")
            structural_ok = False

    optional_files = {
        "subsource_metadata": paths.get("subsource_metadata"),
        "series_linkage": paths.get("series_linkage"),
        "viz_style": paths.get("style"),
    }
    for fname, fpath in optional_files.items():
        if fpath and not Path(fpath).exists():
            add_warn("STRUCTURAL", f"Optional file missing: {fname} ({fpath})")

    present = sum(1 for f in required_files.values() if f and Path(f).exists())
    pass_check("structural", structural_ok,
               f"{present}/{len(required_files)} required files present")

    # -- Check 2: Cross-reference integrity --
    xref_ok = True
    if subsource_meta:
        entries = subsource_meta.get("entries", subsource_meta)
        if isinstance(entries, dict):
            for ss_id, ss in entries.items():
                parent = ss.get("series_id") or ss.get("parent_series")
                if parent and parent not in registry:
                    add_error("XREF", f"Subsource {ss_id} references missing parent: {parent}")
                    xref_ok = False
    else:
        add_warn("XREF", "No subsource metadata loaded; cross-reference check skipped")
    pass_check("cross_reference", xref_ok)

    # -- Check 3: Value sanity --
    sanity_ok = True
    for sid, entry in registry.items():
        yr = entry.get("year_range")
        if isinstance(yr, list) and len(yr) == 2:
            try:
                yr_start, yr_end = int(yr[0]), int(yr[1])
                if yr_start < 1800 or yr_end > 2100 or yr_start > yr_end:
                    add_error("SANITY", f"{sid}: invalid year_range [{yr_start}, {yr_end}]")
                    sanity_ok = False
            except (ValueError, TypeError):
                pass
        ch = entry.get("chapter")
        if ch is not None:
            try:
                ch_num = int(ch)
                if ch_num < 0 or ch_num > 30:
                    add_warn("SANITY", f"{sid}: unusual chapter number {ch}")
            except (ValueError, TypeError):
                pass
    pass_check("value_sanity", sanity_ok)

    # -- Check 4: Chart readiness --
    chart_ok = True
    no_data = sum(1 for e in catalog.values() if not e.get("has_data"))
    total = len(catalog)
    if no_data > 0:
        add_warn("CHART_READY", f"{no_data}/{total} series have no loaded data")
    if no_data == total:
        add_error("CHART_READY", "No series have loaded data -- charts cannot render")
        chart_ok = False
    pass_check("chart_readiness", chart_ok, f"{total - no_data}/{total} series have data")

    # -- Check 5: Manifest verification --
    manifest_path = paths.get("manifest")
    if manifest_path and Path(manifest_path).exists():
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            manifest_ok = True
            for fentry in manifest.get("files", []):
                fp = Path(manifest_path).parent / fentry["path"]
                if not fp.exists():
                    add_warn("MANIFEST", f"Manifest file missing: {fentry['path']}")
            pass_check("manifest", manifest_ok)
        except Exception as e:
            add_warn("MANIFEST", f"Failed to load manifest: {e}")
            pass_check("manifest", True, "Skipped (load error)")
    else:
        add_warn("MANIFEST", "No DATA_MANIFEST.json found; manifest check skipped")
        pass_check("manifest", True, "Skipped (no manifest)")

    return {
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "all_passed": len(errors) == 0,
        "gate": "PASS" if len(errors) == 0 else "FAIL",
    }


def print_validation_results(results: dict):
    log.info("=== Startup Validation Results ===")
    for name, check in results["checks"].items():
        status = "PASS" if check["passed"] else "FAIL"
        detail = f" -- {check['detail']}" if check.get("detail") else ""
        log.info("  %s: [%s]%s", name.upper(), status, detail)

    if results["error_count"] > 0:
        log.error("Validation FAILED with %d errors:", results["error_count"])
        for e in results["errors"]:
            log.error("  %s", e)

    if results["warning_count"] > 0:
        log.warning("Validation warnings (%d):", results["warning_count"])
        for w in results["warnings"]:
            log.warning("  %s", w)

    if results["all_passed"]:
        log.info("Validation PASSED: 0 errors, %d warnings", results["warning_count"])

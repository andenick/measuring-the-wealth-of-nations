"""S01 - Validate Environment.

Checks Python version, required packages, optional API keys, registry presence,
and data-directory scaffold before any data processing runs. Idempotent.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_PACKAGES = ["pandas", "numpy", "openpyxl", "requests"]
REQUIRED_DIRS = ["data/source", "data/raw", "data/intermediate", "data/final", "research", "chopped", "extenbooks", "docs/series"]


def check_python() -> tuple[bool, str]:
    v = sys.version_info
    ok = v.major == 3 and v.minor >= 10
    return ok, f"Python {v.major}.{v.minor}.{v.micro} {'OK' if ok else 'NEED>=3.10'}"


def check_packages() -> list[tuple[bool, str]]:
    results = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
            results.append((True, f"{pkg}: OK"))
        except ImportError:
            results.append((False, f"{pkg}: MISSING"))
    return results


def check_registry() -> tuple[bool, str]:
    p = ROOT / "series_registry.json"
    if not p.exists():
        return False, "series_registry.json: MISSING"
    try:
        r = json.loads(p.read_text(encoding="utf-8"))
        n = len(r.get("series", {}))
        scheme = list(r.get("prefix_scheme", {}).keys())
        return True, f"series_registry.json: OK ({n} series, scheme={scheme})"
    except Exception as e:
        return False, f"series_registry.json: PARSE_ERROR ({e.__class__.__name__})"


def check_api_keys() -> tuple[bool, str]:
    for candidate in ("api_keys.env", "data/user-inputs/api_keys.env", ".env"):
        if (ROOT / candidate).exists():
            return True, f"api_keys: {candidate} found"
    return True, "api_keys: not found (optional — needed only for --test-all)"


def check_dirs() -> list[tuple[bool, str]]:
    results = []
    for d in REQUIRED_DIRS:
        p = ROOT / d
        results.append((p.is_dir(), f"{d}: {'EXISTS' if p.is_dir() else 'MISSING'}"))
    return results


def run() -> dict:
    steps: list[tuple[bool, str]] = []

    ok, msg = check_python()
    steps.append((ok, msg))
    for s in check_packages():
        steps.append(s)
    ok, msg = check_registry()
    steps.append((ok, msg))
    ok, msg = check_api_keys()
    steps.append((ok, msg))
    for s in check_dirs():
        steps.append(s)

    overall_ok = all(s[0] for s in steps)
    for ok, msg in steps:
        print(f"    [S01] {'OK ' if ok else 'FAIL'} {msg}")
    print(f"    [S01] Environment: {'PASS' if overall_ok else 'FAIL'}")
    return {"status": "pass" if overall_ok else "fail", "steps": [m for _, m in steps]}


if __name__ == "__main__":
    result = run()
    sys.exit(0 if result["status"] == "pass" else 1)

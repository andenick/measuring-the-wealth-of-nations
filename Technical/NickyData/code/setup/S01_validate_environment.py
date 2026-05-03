#!/usr/bin/env python3
"""S01 - Validate Environment: check Python, packages, API keys, data dirs.

Runs before any data processing to ensure the environment is correctly configured.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def run():
    steps = []
    ok = True

    # 1. Python version
    v = sys.version_info
    py_ok = v.major == 3 and v.minor >= 10
    steps.append(f"Python {v.major}.{v.minor}.{v.micro}: {'OK' if py_ok else 'NEED >= 3.10'}")
    if not py_ok:
        ok = False
    print(f"    [S01] Python {v.major}.{v.minor}: {'OK' if py_ok else 'FAIL'}")

    # 2. Required packages
    for pkg in ["pandas", "numpy", "openpyxl", "requests"]:
        try:
            __import__(pkg)
            steps.append(f"{pkg}: OK")
        except ImportError:
            steps.append(f"{pkg}: MISSING")
            ok = False
            print(f"    [S01] {pkg}: MISSING")

    # 3. API keys
    from utils.paths import ROOT
    key_path = ROOT / "data" / "user-inputs" / "api_keys.env"
    if not key_path.exists():
        key_path = ROOT / "api_keys.env"  # fallback
    if key_path.exists():
        steps.append(f"API keys: {key_path.name} found")
        print(f"    [S01] API keys: found")
    else:
        steps.append("API keys: NOT FOUND")
        print(f"    [S01] API keys: not found (optional)")

    # 4. Project registry
    reg_path = ROOT / "project_registry.json"
    if reg_path.exists():
        import json
        with open(reg_path) as f:
            reg = json.load(f)
        n_chapters = len(reg.get("book_replication", {}).get("chapters", {}))
        n_studies = len(reg.get("studies", {}))
        steps.append(f"Registry: {n_chapters} chapters, {n_studies} studies")
        print(f"    [S01] Registry: {n_chapters} chapters, {n_studies} studies")
    else:
        steps.append("Registry: NOT FOUND")
        ok = False

    # 5. Data directories
    from utils.paths import SERIES_OUT, STUDIES_OUT, INPUTS
    for name, path in [("Book series", SERIES_OUT), ("Studies", STUDIES_OUT), ("Inputs", INPUTS)]:
        exists = path.exists()
        steps.append(f"{name}: {'EXISTS' if exists else 'MISSING'}")
        if not exists and name == "Inputs":
            ok = False

    status = "ok" if ok else "warn"
    print(f"    [S01] Environment: {status.upper()}")

    return {"status": status, "steps": steps}

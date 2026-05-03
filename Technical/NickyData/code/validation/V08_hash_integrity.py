#!/usr/bin/env python3
"""V08 - Hash Integrity: SHA-256 verification of all input and output files.

On first run, generates baseline hashes and stores in HASH_MANIFEST.json.
On subsequent runs, verifies files match their recorded hashes.

Inputs:
  - data/final-data/series/*.csv
  - data/final-data/chopped/*.csv
  - Inputs/ST_Chopped/**/*.csv (source inputs)
Dependencies: P00 must complete
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import SERIES_OUT, CHOPPED_OUT, ST_CHOPPED, LOGS

VALIDATOR_NAME = "V08_hash_integrity"

MANIFEST_PATH = LOGS / "HASH_MANIFEST.json"


def _hash_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_files():
    """Gather all files to hash."""
    files = {}

    # Output series
    for f in sorted(SERIES_OUT.glob("T*.csv")):
        files[f"series/{f.name}"] = f

    # Output chopped
    for f in sorted(CHOPPED_OUT.glob("T*.csv")):
        files[f"chopped/{f.name}"] = f

    # Input chopped (source files)
    if ST_CHOPPED.exists():
        for f in sorted(ST_CHOPPED.rglob("*.csv")):
            rel = f.relative_to(ST_CHOPPED)
            files[f"inputs/{rel}"] = f

    return files


def validate(series_filter=None, chapter_filter=None):
    files = _collect_files()
    checks = []

    # Load existing manifest if present
    existing = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            manifest = json.load(f)
        existing = manifest.get("hashes", {})

    new_hashes = {}
    is_baseline = len(existing) == 0

    for key, path in files.items():
        if not path.exists():
            continue

        current_hash = _hash_file(path)
        new_hashes[key] = current_hash

        if is_baseline:
            checks.append({
                "file": key,
                "hash": current_hash[:16] + "...",
                "status": "PASS",
                "message": f"{key}: baseline hash recorded",
            })
        elif key in existing:
            if current_hash == existing[key]:
                checks.append({
                    "file": key,
                    "status": "PASS",
                    "message": f"{key}: matches manifest",
                })
            else:
                checks.append({
                    "file": key,
                    "status": "WARN",
                    "message": f"{key}: CHANGED since last validation",
                    "old_hash": existing[key][:16] + "...",
                    "new_hash": current_hash[:16] + "...",
                })
        else:
            checks.append({
                "file": key,
                "hash": current_hash[:16] + "...",
                "status": "PASS",
                "message": f"{key}: new file (added to manifest)",
            })

    # Write updated manifest
    manifest = {
        "version": "1.0.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "is_baseline": is_baseline,
        "file_count": len(new_hashes),
        "hashes": new_hashes,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_warn == 0 else "warn",
        "checks": checks,
        "summary": (
            f"{n_pass} PASS, {n_warn} WARN out of {len(checks)} files "
            f"({'baseline run' if is_baseline else 'verification run'})"
        ),
    }


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))

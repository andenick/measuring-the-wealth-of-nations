#!/usr/bin/env python3
"""V15 - Data Freshness: check data vintage and coverage.

Reads DATA_VINTAGE_LOG.json and flags stale sources.
"""
import sys, json
from pathlib import Path
from datetime import datetime, timedelta
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

VALIDATOR_NAME = "V15_data_freshness"
VINTAGE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "DATA_VINTAGE_LOG.json"
STALE_DAYS = 180  # 6 months


def validate(series_filter=None, chapter_filter=None):
    checks = []

    if not VINTAGE_PATH.exists():
        return {"validator": VALIDATOR_NAME, "status": "skip",
                "checks": [{"status": "SKIP", "message": "DATA_VINTAGE_LOG.json not found"}],
                "summary": "No vintage log"}

    with open(VINTAGE_PATH) as f:
        log = json.load(f)

    now = datetime(2026, 4, 9)  # Current date
    stale_cutoff = now - timedelta(days=STALE_DAYS)

    for name, info in log.get("sources", {}).items():
        pulled = info.get("pulled", "")
        try:
            pull_date = datetime.strptime(pulled, "%Y-%m-%d")
            is_stale = pull_date < stale_cutoff
            days_ago = (now - pull_date).days
        except ValueError:
            is_stale = True
            days_ago = 999

        coverage = info.get("coverage", "unknown")
        checks.append({
            "source": name,
            "pulled": pulled,
            "days_ago": days_ago,
            "coverage": coverage,
            "status": "WARN" if is_stale else "PASS",
            "message": f"{name}: pulled {pulled} ({days_ago}d ago), covers {coverage}",
        })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_warn == 0 else "warn",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_warn} WARN out of {len(checks)} checks",
    }

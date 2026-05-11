#!/usr/bin/env python3
"""S03 - Generate VALIDATION_REPORT.json from V## validator results.

Runs all validators and captures structured results conforming to Anu Review D0 gate.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import importlib.util
import json
from datetime import datetime, timezone


def run():
    code_dir = Path(__file__).resolve().parent.parent / "validation"
    scripts = sorted(code_dir.glob("V[0-9][0-9]_*.py"))

    report = {
        "version": "1.0",
        "generated_by": "S03_generate_validation_report.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "validators": {},
        "summary": {"total": 0, "pass": 0, "fail": 0, "warn": 0, "skip": 0},
    }

    for script in scripts:
        name = script.stem
        spec = importlib.util.spec_from_file_location(name, script)
        mod = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "validate"):
                result = mod.validate()
            elif hasattr(mod, "run"):
                result = mod.run()
            else:
                result = {"status": "skip", "summary": "No entry point"}
        except Exception as exc:
            result = {"status": "fail", "summary": str(exc)}

        status = result.get("status", "ok") if isinstance(result, dict) else "ok"
        summary = result.get("summary", "") if isinstance(result, dict) else str(result)

        report["validators"][name] = {
            "status": status,
            "summary": summary,
        }

        report["summary"]["total"] += 1
        if status == "fail":
            report["summary"]["fail"] += 1
        elif status == "warn":
            report["summary"]["warn"] += 1
        elif status == "skip":
            report["summary"]["skip"] += 1
        else:
            report["summary"]["pass"] += 1

    config_dir = Path(__file__).resolve().parent.parent.parent
    out_path = config_dir / "VALIDATION_REPORT.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)

    s = report["summary"]
    summary = f"Validation report: {s['pass']} pass, {s['fail']} fail, {s['warn']} warn"
    print(f"    [S03] {summary}")
    return {"status": "ok", "summary": summary}

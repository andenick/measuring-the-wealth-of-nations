#!/usr/bin/env python3
"""V14 - Unit Consistency: verify cross-series computations use compatible units.

Uses utils/units.py to check that dollar-denominated series aren't mixed
across different unit bases (billions vs millions).

Known documented mismatches are flagged as WARN (not FAIL).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.units import SERIES_UNITS, get_unit, is_dollar_series

VALIDATOR_NAME = "V14_unit_consistency"

# Known cross-series computations and their unit requirements
CROSS_COMPUTATIONS = [
    {
        "name": "T505 = T501 - T504 (S* = TP* - V*)",
        "series": ["T501", "T504", "T505"],
        "expected_same_unit": True,
        "documented_mismatch": True,
        "note": "T501 in billions (Table E.2), T504/T505 in millions (Table 5.7). Different accounting pathways.",
    },
    {
        "name": "T506 = T505 / T504 (e = S* / V*)",
        "series": ["T504", "T505"],
        "expected_same_unit": True,
        "documented_mismatch": False,
        "note": "Both in millions — ratio is unit-safe.",
    },
    {
        "name": "r* = S* / K (profit rate)",
        "series": ["T505"],
        "external": ["BEA_FIXED_ASSETS"],
        "expected_same_unit": True,
        "documented_mismatch": False,
        "note": "Both in millions — compatible for M02.",
    },
    {
        "name": "NSW/EC (N1302 = T607 / compensation)",
        "series": ["T607"],
        "external": ["BEA_NIPA_6_2D"],
        "expected_same_unit": False,
        "note": "T607 in billions, NIPA compensation in millions. Ratio computed via conversion.",
    },
]


def validate(series_filter=None, chapter_filter=None):
    checks = []

    for comp in CROSS_COMPUTATIONS:
        units_found = {}
        for sid in comp.get("series", []):
            u = get_unit(sid)
            if u != "unknown":
                units_found[sid] = u
        for ext in comp.get("external", []):
            u = get_unit(ext)
            if u != "unknown":
                units_found[ext] = u

        unique_units = set(units_found.values())
        all_same = len(unique_units) <= 1
        is_mismatch = not all_same and comp.get("expected_same_unit", False)
        is_documented = comp.get("documented_mismatch", False)

        if is_mismatch and is_documented:
            status = "WARN"
            msg = f"{comp['name']}: DOCUMENTED unit mismatch ({unique_units})"
        elif is_mismatch:
            status = "FAIL"
            msg = f"{comp['name']}: UNEXPECTED unit mismatch ({unique_units})"
        else:
            status = "PASS"
            msg = f"{comp['name']}: units compatible ({unique_units or 'N/A'})"

        checks.append({
            "computation": comp["name"],
            "units": units_found,
            "status": status,
            "message": msg,
            "note": comp.get("note", ""),
        })

    # Also check all dollar series have documented units
    undocumented = []
    for sid in ["T501", "T502", "T503", "T504", "T505", "T508", "T509",
                "T515", "T516", "T601", "T602", "T603", "T604", "T605", "T606", "T607"]:
        if get_unit(sid) == "unknown":
            undocumented.append(sid)

    if undocumented:
        checks.append({
            "computation": "Unit documentation coverage",
            "status": "WARN",
            "message": f"{len(undocumented)} series without unit documentation: {undocumented}",
        })
    else:
        checks.append({
            "computation": "Unit documentation coverage",
            "status": "PASS",
            "message": "All dollar series have documented units",
        })

    n_pass = sum(1 for c in checks if c["status"] == "PASS")
    n_warn = sum(1 for c in checks if c["status"] == "WARN")
    n_fail = sum(1 for c in checks if c["status"] == "FAIL")

    return {
        "validator": VALIDATOR_NAME,
        "status": "pass" if n_fail == 0 else "fail",
        "checks": checks,
        "summary": f"{n_pass} PASS, {n_warn} WARN, {n_fail} FAIL out of {len(checks)} checks",
    }

import json, re

src_path = "D:/Arcanum/Projects/RMWND/Inputs/ST2/Technical/NickyData/series_registry.json"
out_path = "D:/Arcanum/Projects/RMWND/Technical/series_registry.json"

r = json.load(open(src_path))

ID_RE = re.compile(r"\b(T\d{3}|N\d{4})(-[A-Z0-9]+)?\b")

def remap_id(m):
    core, suffix = m.group(1), m.group(2) or ""
    if core[0] == "T": return "S" + core[1:] + suffix
    if core[0] == "N": return "ES" + core[1:] + suffix
    return m.group(0)

def transform(obj):
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            nk = ID_RE.sub(remap_id, k) if isinstance(k, str) else k
            new[nk] = transform(v)
        return new
    elif isinstance(obj, list):
        return [transform(x) for x in obj]
    elif isinstance(obj, str):
        return ID_RE.sub(remap_id, obj)
    else:
        return obj

new_series = {}
for old_id, entry in r["series"].items():
    new_id = ID_RE.sub(remap_id, old_id)
    new_series[new_id] = transform(entry)

new_figures = transform(r.get("figures", {}))

new = {
    "version": "1.0.0",
    "schema_version": "anu-ingestion-v4.0",
    "project": "measuring-wealth-of-nations-replication",
    "project_name": "Measuring the Wealth of Nations - Replication",
    "project_title": "Replication and Extension of Shaikh & Tonak (1994)",
    "author": "Nick Anderson",
    "original_work": "Shaikh, Anwar and E. Ahmet Tonak (1994). Measuring the Wealth of Nations: The Political Economy of National Accounts. Cambridge University Press.",
    "book": "Shaikh & Tonak (1994) Measuring the Wealth of Nations",
    "core_period": r.get("core_period", [1948, 1989]),
    "extension_period": r.get("extension_period", [1990, 2024]),
    "prefix_scheme": {
        "primary":    {"prefix": "S",  "meaning": "Book series (Shaikh & Tonak 1994)",            "pattern": "S###",   "example": "S506"},
        "external":   {"prefix": "ES", "meaning": "External-study replication",                   "pattern": "ES####", "example": "ES1401"},
        "analytical": {"prefix": "AS", "meaning": "Analytical/Anu-original (framework-derived)",  "pattern": "AS###",  "example": "AS001"}
    },
    "external_study_groups": {
        "10": "Tonak (1984)",
        "11": "Shaikh & Tonak (1987)",
        "12": "Shaikh & Tonak (2002)",
        "13": "Moos (2017)",
        "14": "Mohun (2005)",
        "15": "Mohun (2013)",
        "16": "Karabacak & Tonak (2022) - Turkey",
        "17": "Cronin (2001) - New Zealand"
    },
    "series": new_series,
    "figures": new_figures
}

as_stubs = [
    ("AS001", "Social Burden Rate",            "derived from NSW + exploitation series",     "ratio", "A07_social_burden_rate.py (legacy script)"),
    ("AS002", "Khanjian Cross-Validation",     "cross-check of S506 vs alternative method",  "ratio", "A08_khanjian_crossvalidation.py (legacy script)"),
    ("AS003", "Unproductive Exploitation Rate","S_star / V_u_star (unproductive vc)",        "ratio", "A09_unproductive_exploitation.py (legacy script)"),
    ("AS004", "Marxian Productivity",          "productive output per unit productive labor","index", "A10_marxian_productivity.py (legacy script)")
]
for as_id, name, desc, units, note in as_stubs:
    new_series[as_id] = {
        "name": name,
        "description": desc,
        "source_type": "analytical",
        "year_range": [1948, 2024],
        "subseries": {},
        "construction": [],
        "extension": None,
        "validation": {"reference_values": {}, "expected_range": None, "tolerance": "rate_series"},
        "loader": None,
        "processor": None,
        "wave": 5,
        "status": "stub",
        "units": units,
        "content_type": "derived",
        "notes": note
    }

missing = []
for sid, e in new_series.items():
    if "units" not in e or not e.get("units"):
        missing.append((sid, "units"))
    if "content_type" not in e or not e.get("content_type"):
        missing.append((sid, "content_type"))

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(new, f, indent=2, ensure_ascii=False)

print(f"Wrote registry with {len(new_series)} series to {out_path}")
from collections import Counter
print("By prefix:", Counter([sid[:2] if sid[:2] in ("ES","AS") else sid[0] for sid in new_series]))
if missing:
    print(f"GAPS: {len(missing)} entries missing mandatory units/content_type:")
    for sid, field in missing:
        print(f"  {sid}: missing {field}")
else:
    print("OK: all entries have units + content_type")
print()
print("Sample S506 (head):")
print(json.dumps(new_series["S506"], indent=2)[:600])

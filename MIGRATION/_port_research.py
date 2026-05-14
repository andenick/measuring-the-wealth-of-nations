import json, re, os
from pathlib import Path

src_dir = Path("D:/Arcanum/Projects/RMWND/Inputs/ST2/Technical/research")
out_dir = Path("D:/Arcanum/Projects/RMWND/Technical/research")
out_dir.mkdir(parents=True, exist_ok=True)

ID_RE = re.compile(r"\b(T\d{3}|N\d{4})(-[A-Z0-9]+)?\b")

def remap_id(m):
    core, suffix = m.group(1), m.group(2) or ""
    if core[0] == "T": return "S" + core[1:] + suffix
    if core[0] == "N": return "ES" + core[1:] + suffix
    return m.group(0)

def transform(obj):
    if isinstance(obj, dict):
        return {(ID_RE.sub(remap_id, k) if isinstance(k, str) else k): transform(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [transform(x) for x in obj]
    if isinstance(obj, str):
        return ID_RE.sub(remap_id, obj)
    return obj

src_files = sorted(src_dir.glob("*_research.json"))
print(f"Found {len(src_files)} source research JSONs")

ported = []
for src in src_files:
    old_id = src.stem.replace("_research", "")
    new_id = ID_RE.sub(remap_id, old_id)
    data = json.loads(src.read_text(encoding="utf-8"))
    data = transform(data)
    # Ensure series_id is correct (some files may have stale values)
    data["series_id"] = new_id
    data["ported_from"] = f"ST2/research/{src.name}"
    data["port_date"] = "2026-05-14"
    out_path = out_dir / f"{new_id}_research.json"
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    ported.append((old_id, new_id, out_path.stat().st_size))

# Summary
print(f"\nPorted {len(ported)} research JSONs")
print("\nBy new prefix:")
from collections import Counter
prefixes = Counter([new[:2] if new[:2] in ("ES",) else new[0] for _, new, _ in ported])
print(" ", dict(prefixes))

# Sample S506
sample = out_dir / "S506_research.json"
if sample.exists():
    d = json.loads(sample.read_text(encoding="utf-8"))
    print(f"\nSample S506_research.json:")
    print(f"  series_id: {d.get('series_id')}")
    print(f"  entries: {len(d.get('entries', []))}")
    print(f"  citations: {len(d.get('citations', []))}")
    print(f"  ported_from: {d.get('ported_from')}")

# Quick scan: zero stale T### or N#### in ported files
import glob
stale = 0
for f in out_dir.glob("*.json"):
    txt = f.read_text(encoding="utf-8")
    if re.search(r"\"T\d{3}[\"-]", txt) or re.search(r"\"N\d{4}[\"-]", txt):
        stale += 1
print(f"\nStale T###/N#### references remaining in ported files: {stale}")

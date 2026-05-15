"""Scrub DEC-XXX internal decision codes from research JSONs.

These tokens were inherited from the ST2 port and refer to ST2's internal
decision log, which isn't shipping. Replace each `DEC-XXX` reference with a
neutral `[internal-ST2-decision-log]` marker that preserves the prose
context without leaking the internal coordination scheme.

Also strip the orphaned `NickyData/DECISION_LOG.md` path references — these
point at ST2's internal coordination doc not in our public tree.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("D:/Arcanum/Projects/RMWND/Technical")
RESEARCH = ROOT / "research"


# Replace DEC-NNN (preserve nearby context, just remove the token)
DEC_RE = re.compile(r"DEC-[A-Z0-9]+(?:#[A-Za-z0-9_-]+)?")
# Strip NickyData/DECISION_LOG.md references
NICKYDATA_RE = re.compile(r"NickyData/DECISION_LOG\.md(?:#[A-Za-z0-9_-]+)?|DECISION_LOG\.md(?:#[A-Za-z0-9_-]+)?")


def scrub_value(s: str) -> str:
    s = DEC_RE.sub("[internal-decision-record]", s)
    s = NICKYDATA_RE.sub("[internal-decision-log]", s)
    return s


def scrub_obj(obj):
    if isinstance(obj, dict):
        return {k: scrub_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [scrub_obj(x) for x in obj]
    if isinstance(obj, str):
        return scrub_value(obj)
    return obj


def main():
    files = sorted(RESEARCH.glob("*_research.json"))
    n_changed = 0
    n_subs = 0
    for f in files:
        before = f.read_text(encoding="utf-8")
        if "DEC-" not in before and "DECISION_LOG" not in before:
            continue
        data = json.loads(before)
        scrubbed = scrub_obj(data)
        after = json.dumps(scrubbed, indent=2, ensure_ascii=False)
        if after != before:
            f.write_text(after, encoding="utf-8")
            n_changed += 1
            # Approximate substitution count by counting DEC- before/after
            n_subs += before.count("DEC-") - after.count("DEC-")
    print(f"Scrubbed {n_changed} research JSONs ({n_subs} DEC-XXX tokens replaced)")


if __name__ == "__main__":
    main()

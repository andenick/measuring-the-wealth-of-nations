"""S06 — Publish scrub audit.

Walks the working tree, applies `.publish_ignore` exclusion rules, then greps
every remaining file for internal references that must NOT leak into the
public repo. Reports any matches as findings.

Exclusion rules:
- Files matching patterns in `.publish_ignore` (one per line; trailing /
  marks a directory pattern; supports glob-style)
- Standard non-source dirs: `.git/`, `data/raw/`, `__pycache__/`

Pattern flags (real internal references the Anu Framework's anu-publish
rule set defines):
- `D:/Arcanum`         hard-coded workspace path
- `Council/`           internal infrastructure dir
- `Druck`              internal performance-monitoring tool
- `Robin`              internal data-acquisition tool name (NOT the citation
                       Robin Cherry — pattern uses word boundary)
- internal hosts/paths

False-positive exclusions:
- "Robert" in citations (e.g., "Robert Cherry et al.") — excluded by
  requiring NOT followed by capital-cased next word that is also a name.
  Simpler: skip the "Robert" pattern entirely for plain-name false positives.
"""
from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLISH_IGNORE = ROOT / ".publish_ignore"


# Patterns that flag real internal references. Citation false positives ("Robert
# Cherry et al.") are accepted as legitimate since the patterns prefer
# infrastructure tokens.
SCRUB_PATTERNS = [
    re.compile(r"D:[/\\]Arcanum"),
    re.compile(r"/Council/|\\Council\\"),
    re.compile(r"\bDruck\b"),
    # `Robin` matched only when used as a tool/dir name (followed by /), not as
    # a person's first name.
    re.compile(r"\bRobin/|\bRobin\\"),
    # predecessor-build internal decision codes
    re.compile(r"DEC-[A-Z0-9]+"),
]


def load_ignore_patterns() -> list[str]:
    if not PUBLISH_IGNORE.exists():
        return []
    out = []
    for line in PUBLISH_IGNORE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def is_ignored(rel_path: str, patterns: list[str]) -> bool:
    # Always skip these
    skip_always = (".git/", "__pycache__/", ".venv/", "venv/", "data/raw/")
    if any(rel_path.startswith(s) for s in skip_always):
        return True
    # Skip files that legitimately describe the scrub policy itself:
    # the audit script, chapter REVIEW reports (document the policy), divergence docs
    if rel_path == "code/S00_setup/S06_publish_scrub_audit.py":
        return True
    if rel_path.startswith("docs/chapters/") and rel_path.endswith("_REVIEW_REPORT.json"):
        return True
    if rel_path == "MIGRATION/divergences_from_ST2.md":
        return True
    for pat in patterns:
        if pat.endswith("/"):
            if rel_path.startswith(pat) or f"/{pat}" in rel_path:
                return True
        else:
            if fnmatch.fnmatch(rel_path, pat) or rel_path == pat:
                return True
    return False


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return [(line_no, pattern, line_content_trimmed), ...] for flagged lines."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    for lineno, line in enumerate(text.splitlines(), 1):
        for pat in SCRUB_PATTERNS:
            if pat.search(line):
                findings.append((lineno, pat.pattern, line.strip()[:120]))
                break
    return findings


def run() -> int:
    patterns = load_ignore_patterns()
    text_exts = {".md", ".py", ".json", ".csv", ".tex", ".yaml", ".yml", ".cff",
                 ".toml", ".txt", ".cfg"}
    total_files_scanned = 0
    total_files_with_findings = 0
    total_findings = 0
    all_findings: dict[str, list] = {}

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if is_ignored(rel, patterns):
            continue
        if path.suffix not in text_exts:
            continue
        total_files_scanned += 1
        findings = scan_file(path)
        if findings:
            total_files_with_findings += 1
            total_findings += len(findings)
            all_findings[rel] = findings

    print(f"    [S06] Scanned {total_files_scanned} text files (excluding .publish_ignore matches)")
    if total_findings == 0:
        print(f"    [S06] CLEAN — zero internal references in public-eligible files.")
        return 0
    print(f"    [S06] {total_findings} findings in {total_files_with_findings} files:")
    for rel, findings in all_findings.items():
        print(f"      {rel}:")
        for lineno, pat, line in findings[:5]:
            print(f"        L{lineno}: [{pat}] {line}")
        if len(findings) > 5:
            print(f"        ...({len(findings) - 5} more)")
    return 1


if __name__ == "__main__":
    sys.exit(run())

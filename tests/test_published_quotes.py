"""Hard quote-visibility gate (Tier-A W1a, 2026-07-08).

Every ``publish: true`` series in the registry MUST yield a non-empty,
loader-visible author quote — i.e. its research JSON carries schema-A
``verbatim_quotes[]`` with a non-empty ``text`` that
``Technical/viz/data_loader._load_verbatim_quote`` will surface as
``shaikh_quote`` on the website.

Background: the A4 audit (2026-07-07) found three verbatim-quote schemas
coexisting in ``Technical/research/*.json``; the viz loader reads schema A
only, so 14 published series rendered with an empty author quote while their
quotes physically existed in schema-B entries. The former Q4 quality check
was an always-True soft pass. This test makes the invariant hard.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TECHNICAL_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = TECHNICAL_ROOT / "series_registry.json"
RESEARCH_DIR = TECHNICAL_ROOT / "research"
VIZ_DIR = TECHNICAL_ROOT / "viz"


def _published_series() -> list[str]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        reg = json.load(f)
    series = reg.get("series", reg)
    return sorted(sid for sid, meta in series.items()
                  if isinstance(meta, dict) and meta.get("publish") is True)


def test_every_published_series_has_loader_visible_quote():
    """Uses the real viz loader so the test can never drift from production."""
    sys.path.insert(0, str(VIZ_DIR))
    try:
        from data_loader import _load_verbatim_quote
    finally:
        sys.path.remove(str(VIZ_DIR))

    published = _published_series()
    assert published, "registry yielded no publish:true series"

    missing = []
    for sid in published:
        text, _page, _chapter = _load_verbatim_quote(sid, RESEARCH_DIR)
        if not text or len(text) <= 5:
            missing.append(sid)

    assert not missing, (
        f"{len(missing)}/{len(published)} published series have NO "
        f"loader-visible author quote (schema-A verbatim_quotes[] with "
        f"non-empty text): {missing}"
    )


def test_no_quote_regression_against_b_spine():
    """Schema-A quotes must never exceed honesty: every normalized A quote
    text must exist verbatim among the file's schema-B entry contents
    (zero-invented invariant of the Tier-A W1a normalization)."""
    for fp in sorted(RESEARCH_DIR.glob("*_research.json")):
        with fp.open("r", encoding="utf-8") as f:
            data = json.load(f)
        b_texts = {
            " ".join(((e.get("content") or e.get("verbatim_quote") or "")).split())
            for e in (data.get("entries") or [])
            if isinstance(e, dict) and e.get("entry_type") == "verbatim_quote"
        }
        for q in (data.get("verbatim_quotes") or []):
            if not isinstance(q, dict):
                continue
            if not str(q.get("normalized_from", "")).startswith("schema_B_entries_tiera"):
                continue  # only quotes minted by the W1a normalizer are bound to B
            assert " ".join(str(q.get("text", "")).split()) in b_texts, (
                f"{fp.name}: normalized schema-A quote not found in schema-B "
                f"spine (invented?): {str(q.get('text',''))[:80]!r}"
            )

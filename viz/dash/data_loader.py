"""
RMWND Dash — Data Loader
Loads series_registry.json, chopped CSVs, and builds the series catalog.
Feature-parallel with the R Shiny data_loader.R.
"""

import json
from pathlib import Path
from typing import Optional

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
VIZ_DIR = BASE_DIR.parent  # Technical/viz/
CONFIG_PATH = VIZ_DIR / "config" / "app_config.json"
STYLE_PATH = VIZ_DIR / "viz_style.json"


def load_config() -> dict:
    path = CONFIG_PATH.resolve()
    if not path.exists():
        raise FileNotFoundError(f"app_config.json not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_viz_style() -> dict:
    path = STYLE_PATH.resolve()
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve(relative: str) -> Path:
    """Resolve paths relative to the viz/ directory."""
    return (VIZ_DIR / relative).resolve()


def load_registry(config: dict) -> dict:
    path = _resolve(config["registry_path"])
    with open(path, "r", encoding="utf-8") as f:
        reg = json.load(f)
    return reg.get("series", reg)


def load_chopped_csv(series_id: str, chopped_dir: Path) -> Optional[pd.DataFrame]:
    csv_path = chopped_dir / f"{series_id}.csv"
    if not csv_path.exists():
        for p in sorted(chopped_dir.glob(f"{series_id}[_.]*")):
            csv_path = p
            break
        else:
            return None
    try:
        # Anu chopped format: row 0 = metadata, row 1 = headers, row 2+ = data
        df = pd.read_csv(csv_path, skiprows=1)
        if "Year" in df.columns:
            df = df.rename(columns={"Year": "year"})
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
            df = df.dropna(subset=["year"])
            df["year"] = df["year"].astype(int)
        # Drop unnamed columns from the metadata row leaking through
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
        for col in df.select_dtypes(include=["object"]).columns:
            if col != "year":
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception:
        return None


def _derive_construction_formula(meta: dict) -> str:
    """Render the registry ``construction`` step list as a compact text formula.

    Falls back to an explicit ``construction_formula`` field when present.
    """
    explicit = meta.get("construction_formula")
    if explicit:
        return explicit
    steps = meta.get("construction")
    if not isinstance(steps, list) or not steps:
        return ""
    parts: list[str] = []
    for s in steps:
        if not isinstance(s, dict):
            continue
        op = s.get("op", "")
        if op == "derive" and s.get("formula"):
            parts.append(str(s["formula"]))
        elif op == "splice":
            inputs = s.get("inputs", [])
            at = s.get("at_year", "")
            method = s.get("method", "")
            tail = f" @ {at}" if at else ""
            tail += f" ({method})" if method else ""
            parts.append(f"splice({', '.join(inputs)}){tail}")
        elif op == "load":
            ss = s.get("subseries", [])
            if ss:
                parts.append(f"load({', '.join(ss)})")
        elif op == "extend":
            src = s.get("source", "")
            parts.append(f"extend via {src}" if src else "extend")
    return " ; ".join(parts)


def _load_verbatim_quote(sid: str, research_dir: Path) -> tuple[str, str, str]:
    """Return (text, page, chapter) for the first verbatim quote in the
    series research JSON, or empty strings if none available."""
    fp = research_dir / f"{sid}_research.json"
    if not fp.exists():
        return ("", "", "")
    try:
        j = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return ("", "", "")
    quotes = j.get("verbatim_quotes") or []
    if not isinstance(quotes, list):
        return ("", "", "")
    for q in quotes:
        if isinstance(q, dict) and q.get("text"):
            return (str(q.get("text", "")), str(q.get("page", "")), str(q.get("chapter", "")))
    return ("", "", "")


def _load_viz_disclosure(sid: str, docs_dir: Path) -> str:
    """Extract any "Disclosure footnote" block from the series EPR.

    Looks for a blockquote line beginning with ``> **Disclosure footnote``
    inside ``<sid>_EPR.md`` and returns the joined plain-text body of that
    blockquote. Returns "" if no EPR or no disclosure is present.

    Idempotent: rebuilds from the EPR on every catalog build, so EPR edits
    flow through without any registry changes.
    """
    fp = docs_dir / f"{sid}_EPR.md"
    if not fp.exists():
        return ""
    try:
        text = fp.read_text(encoding="utf-8")
    except Exception:
        return ""
    lines = text.splitlines()
    collected: list[str] = []
    in_block = False
    for ln in lines:
        stripped = ln.strip()
        if not in_block:
            if stripped.startswith("> **Disclosure footnote"):
                in_block = True
                collected.append(stripped.lstrip("> ").strip())
            continue
        if stripped.startswith(">"):
            collected.append(stripped.lstrip("> ").strip())
        elif stripped == "":
            # blank line ends a markdown blockquote
            break
        else:
            break
    return " ".join(p for p in collected if p).strip()


def _derive_extension_status(meta: dict) -> str:
    """Derive display-friendly extension_status from registry status + extension fields."""
    status = meta.get("status", "")
    has_ext = meta.get("extension") is not None

    if "validated_book_and_extension" in status:
        return "extended_2025"
    if has_ext and status == "book_period_validated":
        return "extended_2025"
    if status == "book_period_validated":
        return "verified"
    if "partial" in status:
        return "partial"
    if status == "benchmark_only_matrix_derived":
        return "calculated"
    if status == "data_unavailable":
        return "not_applicable"
    if status.startswith("pending"):
        return "conceptual"
    return "conceptual"


def build_catalog(config: dict) -> dict:
    registry = load_registry(config)
    chopped_dir = _resolve(config["chopped_dir"])
    # research_dir defaults to Technical/research/ relative to viz/
    research_dir = (VIZ_DIR / ".." / "research").resolve()
    docs_dir = (VIZ_DIR / ".." / "docs" / "series").resolve()
    catalog = {}

    for sid, meta in registry.items():
        df = load_chopped_csv(sid, chopped_dir)
        subsources = meta.get("subsources", meta.get("subseries", {})) or {}

        ext_status = _derive_extension_status(meta)
        yr = meta.get("year_range", [])
        tp_start = yr[0] if isinstance(yr, list) and len(yr) >= 1 else meta.get("time_period_start")
        tp_end = yr[1] if isinstance(yr, list) and len(yr) >= 2 else meta.get("time_period_end")

        construction_formula = _derive_construction_formula(meta)
        quote_text, quote_page, quote_chapter = _load_verbatim_quote(sid, research_dir)
        # Prefer explicit registry quote when set, otherwise use research JSON.
        shaikh_quote = meta.get("shaikh_quote") or quote_text
        shaikh_quote_page = meta.get("shaikh_quote_page") or quote_page
        viz_disclosure = _load_viz_disclosure(sid, docs_dir)

        catalog[sid] = {
            "series_id": sid,
            "name": meta.get("name", sid),
            "chapter": meta.get("chapter", ""),
            "units": meta.get("units", ""),
            "time_period_start": tp_start,
            "time_period_end": tp_end,
            "extension_status": ext_status,
            "construction_formula": construction_formula,
            "construction": meta.get("construction", []),
            "shaikh_quote": shaikh_quote,
            "shaikh_quote_page": shaikh_quote_page,
            "shaikh_quote_chapter": quote_chapter,
            "api_sources": meta.get("api_sources", []),
            "subsource_count": len(subsources),
            "subsources": subsources,
            "figure_ids": meta.get("figures", meta.get("figure_ids", [])),
            "methodology_note": meta.get("methodology_note", ""),
            "viz_disclosure": viz_disclosure,
            "has_data": df is not None and len(df) > 0,
            "data": df,
        }
    return catalog


def get_tab_series(catalog: dict, tab_config: dict) -> list[dict]:
    ids = tab_config.get("series_ids", [])
    return [catalog[sid] for sid in ids if sid in catalog]


def get_loaded_count(catalog: dict) -> int:
    return sum(1 for e in catalog.values() if e.get("has_data"))

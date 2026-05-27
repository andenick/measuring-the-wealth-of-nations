"""
Data loader for RMWND chopped CSV files and series registry.

Parses the Anu-chopped CSV format:
  Row 1: metadata (series name, source, units, period, status)
  Row 2: subseries IDs as column headers (Year + subseries IDs)
  Row 3+: data rows (Year in column 1, values in remaining columns)
"""

import json
import os
from pathlib import Path
from typing import Optional

import pandas as pd

_BASE_DIR = Path(__file__).resolve().parent
_CONFIG_PATH = _BASE_DIR / "config" / "app_config.json"


def load_config() -> dict:
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_path(relative: str) -> Path:
    return (_BASE_DIR / relative).resolve()


def load_registry(config: Optional[dict] = None) -> dict:
    config = config or load_config()
    path = _resolve_path(config["registry_path"])
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_chopped_csv(series_id: str, config: Optional[dict] = None) -> Optional[pd.DataFrame]:
    """Load a single chopped CSV and return a DataFrame with Year index."""
    config = config or load_config()
    chopped_dir = _resolve_path(config["chopped_dir"])
    csv_path = chopped_dir / f"{series_id}.csv"
    if not csv_path.exists():
        return None

    df = pd.read_csv(csv_path, skiprows=1, index_col=0)
    df.index.name = "Year"
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _derive_construction_formula(meta: dict) -> str:
    """Render registry ``construction`` step list as compact text formula."""
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
    """Load (text, page, chapter) for first verbatim quote, else empty strings."""
    fp = research_dir / f"{sid}_research.json"
    if not fp.exists():
        return ("", "", "")
    try:
        with open(fp, "r", encoding="utf-8") as f:
            j = json.load(f)
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
    """Extract any "Disclosure footnote" blockquote from the series EPR.

    Idempotent: rebuilds from the EPR on every catalog build. Returns "" if
    no EPR or no disclosure block present.
    """
    fp = docs_dir / f"{sid}_EPR.md"
    if not fp.exists():
        return ""
    try:
        text = fp.read_text(encoding="utf-8")
    except Exception:
        return ""
    collected: list[str] = []
    in_block = False
    for ln in text.splitlines():
        stripped = ln.strip()
        if not in_block:
            if stripped.startswith("> **Disclosure footnote"):
                in_block = True
                collected.append(stripped.lstrip("> ").strip())
            continue
        if stripped.startswith(">"):
            collected.append(stripped.lstrip("> ").strip())
        elif stripped == "":
            break
        else:
            break
    return " ".join(p for p in collected if p).strip()


def build_catalog(config: Optional[dict] = None) -> dict:
    """Build the definitive series catalog from the registry."""
    config = config or load_config()
    registry = load_registry(config)
    series_map = registry.get("series", {})
    research_dir = (_BASE_DIR / ".." / "research").resolve()
    docs_dir = (_BASE_DIR / ".." / "docs" / "series").resolve()
    catalog = {}
    for sid, meta in series_map.items():
        subseries_list = []
        for sub_id, sub_meta in (meta.get("subseries") or {}).items():
            subseries_list.append({
                "id": sub_id,
                "name": sub_meta.get("name", ""),
                "source": sub_meta.get("source", ""),
                "period": sub_meta.get("period"),
                "units": sub_meta.get("units", ""),
                "color": sub_meta.get("color"),
            })
        quote_text, quote_page, quote_chapter = _load_verbatim_quote(sid, research_dir)
        viz_disclosure = _load_viz_disclosure(sid, docs_dir)
        catalog[sid] = {
            "series_id": sid,
            "name": meta.get("name", sid),
            "chapter": meta.get("chapter", meta.get("study", "")),
            "book_table": meta.get("book_table", meta.get("paper_table", "")),
            "year_range": meta.get("year_range"),
            "units": meta.get("units", ""),
            "status": meta.get("status", ""),
            "content_type": meta.get("content_type", "time_series"),
            "subseries": subseries_list,
            "construction": meta.get("construction", []),
            "construction_formula": _derive_construction_formula(meta),
            "shaikh_quote": meta.get("shaikh_quote") or quote_text,
            "shaikh_quote_page": meta.get("shaikh_quote_page") or quote_page,
            "shaikh_quote_chapter": quote_chapter,
            "viz_disclosure": viz_disclosure,
            "figures": meta.get("figures", []),
        }
    return catalog


def write_catalog_json(config: Optional[dict] = None):
    """Write DEFINITIVE_SERIES_CATALOG.json to disk."""
    config = config or load_config()
    catalog = build_catalog(config)
    out_path = _BASE_DIR / "data" / "catalogs" / "DEFINITIVE_SERIES_CATALOG.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    return out_path


def validate_data_availability(config: Optional[dict] = None) -> dict:
    """Check which chopped CSVs actually exist and have loadable data."""
    config = config or load_config()
    catalog = build_catalog(config)
    chopped_dir = _resolve_path(config["chopped_dir"])
    results = {"available": [], "missing": [], "errors": []}
    for sid in catalog:
        csv_path = chopped_dir / f"{sid}.csv"
        if not csv_path.exists():
            results["missing"].append(sid)
            continue
        try:
            df = load_chopped_csv(sid, config)
            if df is not None and len(df) > 0:
                results["available"].append(sid)
            else:
                results["errors"].append(sid)
        except Exception:
            results["errors"].append(sid)
    return results


def get_series_for_tab(tab_id: str, config: Optional[dict] = None) -> list[dict]:
    """Return catalog entries for series belonging to a specific tab."""
    config = config or load_config()
    catalog = build_catalog(config)
    tab_series_ids = config["tabs"].get(tab_id, {}).get("series_ids", [])
    return [catalog[sid] for sid in tab_series_ids if sid in catalog]


if __name__ == "__main__":
    cfg = load_config()
    print("Generating DEFINITIVE_SERIES_CATALOG.json ...")
    out = write_catalog_json(cfg)
    print(f"  Written to {out}")

    print("\nValidating data availability ...")
    results = validate_data_availability(cfg)
    print(f"  Available: {len(results['available'])}")
    print(f"  Missing:   {len(results['missing'])}  {results['missing']}")
    print(f"  Errors:    {len(results['errors'])}  {results['errors']}")

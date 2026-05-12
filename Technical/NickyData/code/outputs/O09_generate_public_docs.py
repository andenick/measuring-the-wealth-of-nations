#!/usr/bin/env python3
"""O09 - Generate public /docs/ folder from DPRs, research JSONs, and registry.

Creates reader-friendly Markdown write-ups for each series, with:
- What the series measures (plain English)
- What Shaikh & Tonak wrote about it (book quotes)
- Mathematical formulas (GitHub LaTeX)
- How we replicated it (code references + data sources)
- Key values and validation results

Output: docs/series/*.md files at the repo root level (public-facing)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import CONFIG, TECHNICAL

PROJECT_ROOT = TECHNICAL.parent
DOCS_OUT = PROJECT_ROOT / "docs" / "series"
DOCS_SERIES = TECHNICAL / "docs" / "series"
DOCS_STUDIES = TECHNICAL / "docs" / "studies"
RESEARCH_DIR = TECHNICAL / "research"


def _load_registry():
    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        return json.load(f)


def _read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def _extract_book_quotes(research_json: dict) -> list[str]:
    quotes = []
    for entry in research_json.get("entries", []):
        if entry.get("entry_type") in ("methodology_description", "benchmark_values", "figure_context"):
            quotes.append(entry.get("content", ""))
    return quotes


def _extract_formula(dpr_text: str) -> str:
    in_formula = False
    formula_lines = []
    for line in dpr_text.split("\n"):
        if "**Formula**" in line or "Formula:" in line:
            in_formula = True
            continue
        if in_formula:
            if line.startswith("```"):
                if formula_lines:
                    in_formula = False
                continue
            if line.startswith("**") and formula_lines:
                break
            if line.strip():
                formula_lines.append(line)
    return "\n".join(formula_lines[:10])


def _generate_series_doc(sid: str, config: dict, registry: dict) -> str:
    name = config.get("name", sid)
    chapter = config.get("chapter")
    book_table = config.get("book_table", "")
    year_range = config.get("year_range", [])
    units = ""
    for sub in config.get("subseries", {}).values():
        units = sub.get("units", "")
        if units:
            break

    # Load DPR
    is_study = sid.startswith("N")
    dpr_dir = DOCS_STUDIES if is_study else DOCS_SERIES
    dpr_text = _read_file(dpr_dir / f"{sid}_DPR.md")
    epr_text = _read_file(dpr_dir / f"{sid}_EPR.md")
    decomp_text = _read_file(dpr_dir / f"{sid}_DECOMPOSITION.md")

    # Load research JSON
    research = {}
    res_path = RESEARCH_DIR / f"{sid}_research.json"
    if res_path.exists():
        with open(res_path, encoding="utf-8") as f:
            research = json.load(f)

    book_quotes = _extract_book_quotes(research)
    formula = _extract_formula(dpr_text)

    # Build construction steps
    construction = config.get("construction", [])
    construction_text = ""
    if construction:
        steps = []
        for i, step in enumerate(construction, 1):
            op = step.get("op", "")
            formula_str = step.get("formula", "")
            inputs = step.get("inputs", [])
            output = step.get("output", "")
            if formula_str:
                steps.append(f"{i}. **{op}**: `{formula_str}`")
            elif inputs:
                steps.append(f"{i}. **{op}**: {', '.join(inputs)} → {output}")
            else:
                steps.append(f"{i}. **{op}**")
        construction_text = "\n".join(steps)

    # Build subsources table
    subsources = config.get("subseries", {})
    sub_rows = []
    for sub_id, sub in subsources.items():
        source = sub.get("source", "")
        period = sub.get("period", [])
        period_str = f"{period[0]}–{period[1]}" if len(period) == 2 else ""
        sub_rows.append(f"| `{sub_id}` | {source} | {period_str} | {sub.get('units', '')} |")

    # Build validation
    validation = config.get("validation", {})
    ref_vals = validation.get("reference_values", {})
    ref_text = ""
    if ref_vals:
        ref_items = [f"- **{yr}**: {val}" for yr, val in sorted(ref_vals.items())]
        ref_text = "\n".join(ref_items)

    # Extension info
    ext = config.get("extension")
    ext_text = ""
    if ext:
        ext_text = f"Extended from {ext.get('splice_year', '?')} using {ext.get('splice_method', '?')} method."
        deps = ext.get("depends_on", [])
        if deps:
            ext_text += f" Depends on: {', '.join(deps)}."

    # Loader and processor
    loader = config.get("loader", "")
    processor = config.get("processor", "")
    code_text = ""
    if loader or processor:
        code_text = f"Loading: `code/loading/{loader}_*.py`"
        if processor:
            code_text += f" | Processing: `code/processing/{processor}_*.py`"

    # --- Build the document ---
    lines = [
        f"# {sid}: {name}",
        "",
    ]

    if chapter:
        lines.append(f"**Chapter {chapter}** | Book Table {book_table} | {units}")
    elif config.get("study"):
        lines.append(f"**External Study** | {config.get('study', '')}")

    if year_range:
        lines.append(f"**Period**: {year_range[0]}–{year_range[-1]}")
    lines.append("")

    # Description from DPR context
    if dpr_text:
        # Extract the Context section
        in_context = False
        context_lines = []
        for line in dpr_text.split("\n"):
            if "## Context" in line:
                in_context = True
                continue
            if in_context:
                if line.startswith("## ") and context_lines:
                    break
                if line.strip():
                    context_lines.append(line)
        if context_lines:
            lines.append("## What This Measures")
            lines.append("")
            # Strip internal references
            cleaned = [
                l.replace("AS2", "this replication").replace("in AS2", "here")
                .replace("Anu Standard", "data quality standard")
                .replace("NickyData", "the pipeline")
                for l in context_lines[:8]
            ]
            lines.extend(cleaned)
            lines.append("")

    # Book quotes
    if book_quotes:
        lines.append("## From the Book")
        lines.append("")
        for q in book_quotes[:3]:
            lines.append(f"> {q}")
            lines.append("")

    # Formula
    if formula:
        lines.append("## Formula")
        lines.append("")
        lines.append("```")
        lines.append(formula)
        lines.append("```")
        lines.append("")

    # Construction
    if construction_text:
        lines.append("## How We Compute It")
        lines.append("")
        lines.append(construction_text)
        lines.append("")

    # Subsources
    if sub_rows:
        lines.append("## Data Sources")
        lines.append("")
        lines.append("| Component | Source | Period | Units |")
        lines.append("|-----------|--------|--------|-------|")
        lines.extend(sub_rows)
        lines.append("")

    # Extension
    if ext_text:
        lines.append("## Extension (Post-1989)")
        lines.append("")
        lines.append(ext_text)
        lines.append("")

    # Validation
    if ref_text:
        lines.append("## Book Benchmark Values")
        lines.append("")
        lines.append(ref_text)
        lines.append("")

    # Code reference
    if code_text:
        lines.append("## Code")
        lines.append("")
        lines.append(code_text)
        lines.append("")

    lines.append("---")
    lines.append(f"*Part of the [Measuring the Wealth of Nations](https://github.com/andenick/measuring-the-wealth-of-nations) replication package.*")
    lines.append("")

    return "\n".join(lines)


def generate():
    DOCS_OUT.mkdir(parents=True, exist_ok=True)

    registry = _load_registry()
    outputs = []

    for sid, config in sorted(registry["series"].items()):
        doc = _generate_series_doc(sid, config, registry)
        out_path = DOCS_OUT / f"{sid}.md"
        out_path.write_text(doc, encoding="utf-8")
        outputs.append(sid)

    # Generate index
    index_lines = [
        "# Series Documentation",
        "",
        "Complete documentation for all 59 data series in this replication package.",
        "",
        "## Book Series (Chapters 2–9)",
        "",
        "| Series | Name | Chapter | Period |",
        "|--------|------|---------|--------|",
    ]

    for sid, config in sorted(registry["series"].items()):
        if sid.startswith("T"):
            ch = config.get("chapter", "")
            yr = config.get("year_range", [])
            period = f"{yr[0]}–{yr[-1]}" if yr else ""
            index_lines.append(f"| [{sid}](series/{sid}.md) | {config.get('name', '')} | {ch} | {period} |")

    index_lines.extend([
        "",
        "## External Study Series",
        "",
        "| Series | Name | Study | Period |",
        "|--------|------|-------|--------|",
    ])

    for sid, config in sorted(registry["series"].items()):
        if sid.startswith("N"):
            study = config.get("study", "")
            yr = config.get("year_range", [])
            period = f"{yr[0]}–{yr[-1]}" if yr else ""
            index_lines.append(f"| [{sid}](series/{sid}.md) | {config.get('name', '')} | {study} | {period} |")

    index_path = PROJECT_ROOT / "docs" / "README.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")

    summary = f"Public docs: {len(outputs)} series write-ups + index"
    print(f"    [O09] {summary}")
    return {"status": "ok", "summary": summary, "outputs": outputs}

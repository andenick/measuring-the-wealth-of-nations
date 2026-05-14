"""Generate per-series DECOMPOSITION.md (Mermaid + step-by-step flow)
and EPR.md (extension provenance) for Ch5 series.

Both are produced from the registry + research JSON + DPR. Mechanical
generation - the registry already contains all needed metadata."""
import json
from pathlib import Path

REG  = json.loads(Path("D:/Arcanum/Projects/RMWND/Technical/series_registry.json").read_text(encoding="utf-8"))
RES  = Path("D:/Arcanum/Projects/RMWND/Technical/research")
OUT  = Path("D:/Arcanum/Projects/RMWND/Technical/docs/series")

CH5_IDS = [sid for sid, e in REG["series"].items() if e.get("chapter") == 5]
EXTENDABLE = [sid for sid in CH5_IDS if REG["series"][sid].get("extension")]

written_decomp = []
written_epr    = []

# Subseries colors (defaults)
ORIG  = "#FFF2CC"
EXT   = "#E6F2FF"
FINAL = "#E6FFE6"

for sid in sorted(CH5_IDS):
    entry = REG["series"][sid]
    subs  = entry.get("subseries", {})
    construction = entry.get("construction", [])
    ext_block    = entry.get("extension")
    name         = entry.get("name", "")

    # ===== DECOMPOSITION.md =====
    lines = [f"# {sid} — Decomposition", "", f"**Series**: {name}", "",
             "## Construction Flow", "", "```mermaid", "flowchart TD"]

    # Node for each subseries
    for ss in subs:
        lines.append(f'    {ss.replace("-", "_")}["{ss}<br/>{subs[ss].get("source","")}"]')
    # Node for each construction step's output
    for s in construction:
        op  = s.get("op", "")
        inp = ", ".join(s.get("inputs", []) or s.get("subseries", []) or [])
        out = s.get("output", "")
        formula = s.get("formula", "")
        label = f'{op}{": " + formula if formula else ""}'
        if out:
            node_id = out.replace("-", "_")
            lines.append(f'    {node_id}["{out}<br/>{label}"]')
            if inp:
                for i in [x.strip() for x in inp.split(",") if x.strip()]:
                    lines.append(f'    {i.replace("-", "_")} --> {node_id}')
    lines += ["```", "", "## Step-by-step construction", ""]
    for s in construction:
        step_num = s.get("step", "?")
        op       = s.get("op", "")
        inputs   = s.get("inputs", []) or s.get("subseries", []) or []
        out      = s.get("output", "")
        formula  = s.get("formula", "")
        at_year  = s.get("at_year", "")
        method   = s.get("method", "")
        lines.append(f"**Step {step_num}** — {op}")
        if inputs: lines.append(f"  - Inputs: {', '.join(inputs)}")
        if out:    lines.append(f"  - Output: `{out}`")
        if formula:lines.append(f"  - Formula: `{formula}`")
        if at_year:lines.append(f"  - At year: {at_year}")
        if method: lines.append(f"  - Method: {method}")
        lines.append("")

    if ext_block:
        lines += ["## Extension", "",
                  f"- Splice year: {ext_block.get('splice_year','?')}",
                  f"- Splice method: {ext_block.get('splice_method','?')}",
                  f"- Depends on: {', '.join(ext_block.get('depends_on', []) or ['(none)'])}",
                  ""]
    else:
        lines += ["## Extension", "", "Not extended — series is `book_period_only` "
                  "or marked `pending_capital_stock_data`. See DPR.", ""]

    lines += ["## Provenance",
              "",
              "See [`" + sid + "_DPR.md`](" + sid + "_DPR.md) for the canonical "
              "Data Provenance Record, including source-file citations, validation "
              "benchmarks, and known caveats.",
              ""]
    (OUT / f"{sid}_DECOMPOSITION.md").write_text("\n".join(lines), encoding="utf-8")
    written_decomp.append(sid)

# ===== EPRs (only for extendable series) =====
for sid in sorted(EXTENDABLE):
    entry  = REG["series"][sid]
    ext    = entry["extension"]
    subs   = entry.get("subseries", {})
    name   = entry.get("name", "")
    units  = entry.get("units", "")
    splice = ext.get("splice_year", "?")
    method = ext.get("splice_method", "?")
    deps   = ext.get("depends_on", [])

    ext_subseries = [s for s in subs if "EXT" in s or "COMBINED" in s]

    lines = [
        f"# {sid} — Extension Provenance Record",
        "",
        f"**Series**: {name}",
        f"**Units**: {units}",
        f"**Book period**: 1948–1989 (canonical, in `data/final/{sid}.csv`)",
        f"**Extension target**: 1990–2024 (post-book)",
        f"**Status**: extension_methodology_documented (data fetch pending API keys)",
        "",
        "## Splice methodology",
        "",
        f"- **Splice year**: {splice}",
        f"- **Splice method**: `{method}`",
        f"- **Dependencies on other series**: {', '.join(deps) if deps else '(none)'}",
        "",
    ]
    if method == "growth_rate":
        lines += [
            "**Growth-rate splice**: the extension subseries (`S###-B` or `-EXT`) "
            "is rebased so its value at the splice year matches the book series' "
            "implied splice-year value; subsequent years carry forward by the "
            "extension source's year-on-year growth. This is the appropriate "
            "method when both eras directly observe the same construct under "
            "different industrial classifications (e.g., SIC vs NAICS), per the "
            "Anu Extension Standard.", ""]
    elif method == "derive":
        lines += [
            "**Derived extension**: the extension is computed from already-extended "
            "upstream series via a closed-form relation. No external API is "
            "fetched directly; the extension faithfulness inherits from the "
            "dependencies listed above.", ""]

    lines += ["## Extension data source(s)", ""]
    for ss in ext_subseries:
        ss_entry = subs[ss]
        lines.append(f"- `{ss}` — {ss_entry.get('source','')} (period "
                     f"{ss_entry.get('period','?')}, units "
                     f"{ss_entry.get('units', units)})")
    if not ext_subseries:
        lines.append("- (no -EXT subseries declared in registry; extension is "
                     "derived purely from upstream dependencies)")
    lines += ["", "## Activation criteria",
              "",
              "Before the extension is fetched and spliced into `data/final/" + sid + ".csv`:",
              "",
              "- [ ] `data/user-inputs/api_keys.env` provisioned (BEA, BLS, or FRED as required)",
              "- [ ] L## loader extended to fetch the extension subsource and write it to "
              "`data/raw/`",
              "- [ ] P## processor extended to perform the splice and emit `S###-COMBINED`",
              "- [ ] V## validator extended with transition-quality checks (V06/V07 per the "
              "Anu Extension Standard): connection ratio in [0.95, 1.05], overlap correlation "
              "≥ 0.95, no SIGN-flip across the splice point",
              "- [ ] EPR updated with the actual API series IDs, agency URLs, and faithfulness "
              "rating (per Anu Extension Standard rubric)",
              "",
              "## Faithfulness considerations",
              "",
              "Per the Anu Extension Standard (no proxies, no lazy splices on derived "
              "quantities): the extension MUST use the agency/table the book originally drew "
              "from, or document any substitution explicitly. For " + sid + ", the canonical "
              "BEA/BLS/FRED endpoint is recorded in the registry under "
              "`subseries[S###-B].source`. Any divergence requires a Concept Match Justification "
              "in this EPR.",
              ""]

    (OUT / f"{sid}_EPR.md").write_text("\n".join(lines), encoding="utf-8")
    written_epr.append(sid)

print(f"DECOMPOSITION.md: wrote {len(written_decomp)} for Ch5 series")
print(f"EPR.md         : wrote {len(written_epr)} for extendable Ch5 series ({', '.join(written_epr)})")

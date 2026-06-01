"""Build the RMWND citation graph from research JSONs.

Nodes:
  - Series nodes (S###, ES####, AS###) — color-coded by prefix
  - External-paper nodes — derived from the `citations[].id` field across all
    research JSONs (e.g., Tonak_1984, ST_1987, Mohun_2005, Cronin_2001)

Edges (directed, citing -> cited):
  - Series A -> Series B if A's research JSON lists B in `cross_references`
  - Series A -> Paper P if A's research JSON lists P in `citations`

Outputs:
  - Technical/viz/exports/citation_graph.dot   (Graphviz DOT)
  - Technical/viz/exports/citation_graph.svg   (rendered if `dot` is on PATH)
  - Technical/viz/exports/citation_graph.html  (interactive D3 force layout)

Read-only with respect to series_registry.json / PIPELINE_STATE / LEDGER /
MANIFEST / SUBSERIES_PLAN.json.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "research"
OUT_DIR = ROOT / "viz" / "exports"

# Color scheme by prefix
COLORS = {
    "S":  "#1f77b4",   # blue
    "ES": "#ff7f0e",   # orange
    "AS": "#2ca02c",   # green
    "P":  "#cccccc",   # paper outline
}


def _series_prefix(sid: str) -> str:
    for p in ("ES", "AS", "S"):
        if sid.startswith(p):
            return p
    return "?"


def is_series_id(s: str) -> bool:
    if not s:
        return False
    p = _series_prefix(s)
    if p == "?":
        return False
    body = s[len(p):]
    return body.isdigit() or (len(body) >= 2 and body[:-1].isdigit() and body[-1].isalpha())


def load_research() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(RESEARCH_DIR.glob("*_research.json")):
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"  skip {p.name}: {e}", file=sys.stderr)
            continue
        sid = data.get("series_id") or p.stem.replace("_research", "")
        out[sid] = data
    return out


def build_graph(research: dict[str, dict]) -> tuple[dict, list[tuple[str, str]]]:
    """Returns (nodes_dict, edges_list).

    nodes_dict[node_id] = {"type": "series"|"paper", "prefix": str, "label": str}
    edges_list = [(src, dst), ...] de-duplicated.
    """
    nodes: dict[str, dict] = {}
    edges: set[tuple[str, str]] = set()

    # 1) Seed series nodes from research files (this ensures every research'd series appears)
    for sid in research:
        nodes[sid] = {
            "type": "series",
            "prefix": _series_prefix(sid),
            "label": sid,
        }

    # 2) Edges + paper nodes
    for sid, data in research.items():
        # 2a) cross_references -> other series
        xrefs = data.get("cross_references") or []
        if isinstance(xrefs, list):
            for tgt in xrefs:
                tgt = (tgt or "").strip()
                if not tgt or tgt == sid:
                    continue
                if is_series_id(tgt):
                    if tgt not in nodes:
                        nodes[tgt] = {
                            "type": "series",
                            "prefix": _series_prefix(tgt),
                            "label": tgt,
                        }
                    edges.add((sid, tgt))
                else:
                    # Treat free-text cross_ref as a paper-ish node
                    pid = "P:" + tgt
                    nodes.setdefault(pid, {
                        "type": "paper",
                        "prefix": "P",
                        "label": tgt,
                    })
                    edges.add((sid, pid))

        # 2b) citations -> paper nodes
        cits = data.get("citations") or []
        if isinstance(cits, list):
            for c in cits:
                if isinstance(c, dict):
                    pid_raw = (c.get("id") or "").strip()
                    if not pid_raw:
                        continue
                    label = pid_raw.replace("_", " ")
                elif isinstance(c, str):
                    pid_raw = c.strip()
                    label = pid_raw
                else:
                    continue
                if not pid_raw:
                    continue
                pid = "P:" + pid_raw
                nodes.setdefault(pid, {
                    "type": "paper",
                    "prefix": "P",
                    "label": label,
                })
                edges.add((sid, pid))

    return nodes, sorted(edges)


# ----------------------- DOT renderer -----------------------

def _safe_id(s: str) -> str:
    return '"' + s.replace('"', '\\"') + '"'


def render_dot(nodes: dict, edges: list[tuple[str, str]]) -> str:
    lines = [
        'digraph RMWND_citations {',
        '  graph [rankdir=LR, splines=true, overlap=false, '
        'fontname="Helvetica", labelloc="t", '
        'label="RMWND citation graph (series -> series + series -> paper)"];',
        '  node  [fontname="Helvetica", fontsize=10, style=filled];',
        '  edge  [color="#888888", arrowsize=0.6];',
        '',
    ]
    # Cluster series by prefix for readability
    by_prefix: dict[str, list[str]] = {"S": [], "ES": [], "AS": []}
    papers: list[str] = []
    for nid, attrs in nodes.items():
        if attrs["type"] == "paper":
            papers.append(nid)
        else:
            by_prefix.setdefault(attrs["prefix"], []).append(nid)

    cluster_titles = {"S": "Book series (S)", "ES": "External-study series (ES)", "AS": "Analytical series (AS)"}
    for prefix in ("S", "ES", "AS"):
        bucket = sorted(by_prefix.get(prefix, []))
        if not bucket:
            continue
        color = COLORS[prefix]
        lines.append(f'  subgraph cluster_{prefix} {{')
        lines.append(f'    label="{cluster_titles[prefix]}"; color="{color}"; style="rounded";')
        for nid in bucket:
            label = nodes[nid]["label"]
            lines.append(f'    {_safe_id(nid)} [label="{label}", '
                         f'shape=ellipse, fillcolor="{color}", fontcolor="white"];')
        lines.append('  }')

    if papers:
        lines.append('  subgraph cluster_papers {')
        lines.append('    label="External papers"; color="#666666"; style="rounded,dashed";')
        for nid in sorted(papers):
            label = nodes[nid]["label"]
            lines.append(f'    {_safe_id(nid)} [label="{label}", '
                         f'shape=note, fillcolor="white", color="#666666"];')
        lines.append('  }')

    lines.append('')
    for src, dst in edges:
        lines.append(f'  {_safe_id(src)} -> {_safe_id(dst)};')
    lines.append('}')
    return "\n".join(lines) + "\n"


# ----------------------- HTML (D3) renderer -----------------------

HTML_TEMPLATE = """<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<title>RMWND citation graph</title>
<style>
  body {{ font-family: Helvetica, Arial, sans-serif; margin: 0; background: #f7f7f7; }}
  header {{ padding: 10px 16px; background: #1f2933; color: #fff; }}
  header h1 {{ margin: 0; font-size: 18px; }}
  header p {{ margin: 4px 0 0 0; font-size: 12px; color: #cbd2d9; }}
  #legend {{ position: absolute; right: 12px; top: 70px; background: rgba(255,255,255,0.9);
             border: 1px solid #ccc; padding: 6px 10px; font-size: 12px; border-radius: 4px; }}
  .legend-item {{ display: flex; align-items: center; margin: 2px 0; }}
  .legend-swatch {{ width: 14px; height: 14px; margin-right: 6px; border-radius: 50%; }}
  svg {{ width: 100vw; height: calc(100vh - 60px); }}
  .node circle, .node rect {{ stroke: #333; stroke-width: 1px; }}
  .node text {{ font-size: 10px; pointer-events: none; }}
  .link {{ stroke: #888; stroke-opacity: 0.5; fill: none; }}
</style>
</head>
<body>
<header>
  <h1>RMWND citation graph</h1>
  <p>{n_nodes} nodes ({n_series} series + {n_papers} papers), {n_edges} directed citations.</p>
</header>
<div id=\"legend\">
  <div class=\"legend-item\"><div class=\"legend-swatch\" style=\"background:{c_s}\"></div>S — book series</div>
  <div class=\"legend-item\"><div class=\"legend-swatch\" style=\"background:{c_es}\"></div>ES — external-study series</div>
  <div class=\"legend-item\"><div class=\"legend-swatch\" style=\"background:{c_as}\"></div>AS — analytical series</div>
  <div class=\"legend-item\"><div class=\"legend-swatch\" style=\"background:#fff;border:1px solid #666\"></div>Paper</div>
</div>
<svg></svg>
<script src=\"https://d3js.org/d3.v7.min.js\"></script>
<script>
const DATA = {data_json};

const svg = d3.select(\"svg\");
const width  = window.innerWidth;
const height = window.innerHeight - 60;
const g = svg.append(\"g\");

svg.call(d3.zoom().on(\"zoom\", (e) => g.attr(\"transform\", e.transform)));

const color = (p) => ({{
  \"S\":  \"{c_s}\",
  \"ES\": \"{c_es}\",
  \"AS\": \"{c_as}\",
  \"P\":  \"#ffffff\"
}})[p] || \"#999\";

const sim = d3.forceSimulation(DATA.nodes)
  .force(\"link\", d3.forceLink(DATA.links).id(d => d.id).distance(60).strength(0.4))
  .force(\"charge\", d3.forceManyBody().strength(-120))
  .force(\"center\", d3.forceCenter(width/2, height/2))
  .force(\"collide\", d3.forceCollide().radius(18));

const link = g.append(\"g\").selectAll(\"line\")
  .data(DATA.links).join(\"line\")
  .attr(\"class\", \"link\");

const node = g.append(\"g\").selectAll(\"g\")
  .data(DATA.nodes).join(\"g\")
  .attr(\"class\", \"node\")
  .call(d3.drag()
    .on(\"start\", (e,d)=>{{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}})
    .on(\"drag\",  (e,d)=>{{d.fx=e.x;d.fy=e.y;}})
    .on(\"end\",   (e,d)=>{{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}));

node.each(function(d) {{
  const sel = d3.select(this);
  if (d.type === \"paper\") {{
    sel.append(\"rect\").attr(\"x\",-8).attr(\"y\",-6).attr(\"width\",16).attr(\"height\",12)
       .attr(\"fill\",color(d.prefix)).attr(\"stroke\",\"#666\");
  }} else {{
    sel.append(\"circle\").attr(\"r\",8).attr(\"fill\",color(d.prefix));
  }}
}});

node.append(\"title\").text(d => d.label);
node.append(\"text\").attr(\"x\",10).attr(\"y\",3).text(d => d.label);

sim.on(\"tick\", () => {{
  link.attr(\"x1\", d=>d.source.x).attr(\"y1\", d=>d.source.y)
      .attr(\"x2\", d=>d.target.x).attr(\"y2\", d=>d.target.y);
  node.attr(\"transform\", d => `translate(${{d.x}}, ${{d.y}})`);
}});
</script>
</body>
</html>
"""


def render_html(nodes: dict, edges: list[tuple[str, str]]) -> str:
    nodes_arr = [
        {"id": nid, "label": attrs["label"], "type": attrs["type"], "prefix": attrs["prefix"]}
        for nid, attrs in nodes.items()
    ]
    links_arr = [{"source": s, "target": t} for s, t in edges]
    data = {"nodes": nodes_arr, "links": links_arr}
    n_series = sum(1 for n in nodes.values() if n["type"] == "series")
    n_papers = sum(1 for n in nodes.values() if n["type"] == "paper")
    return HTML_TEMPLATE.format(
        n_nodes=len(nodes),
        n_series=n_series,
        n_papers=n_papers,
        n_edges=len(edges),
        c_s=COLORS["S"], c_es=COLORS["ES"], c_as=COLORS["AS"],
        data_json=json.dumps(data),
    )


def try_render_svg(dot_path: Path, svg_path: Path) -> bool:
    dot_exe = shutil.which("dot")
    if not dot_exe:
        return False
    try:
        subprocess.run(
            [dot_exe, "-Tsvg", str(dot_path), "-o", str(svg_path)],
            check=True, capture_output=True, text=True, timeout=60,
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"  graphviz failed: {e}", file=sys.stderr)
        return False


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    research = load_research()
    print(f"Loaded {len(research)} research JSONs")

    nodes, edges = build_graph(research)
    n_series = sum(1 for n in nodes.values() if n["type"] == "series")
    n_papers = sum(1 for n in nodes.values() if n["type"] == "paper")
    print(f"Graph: {len(nodes)} nodes ({n_series} series + {n_papers} papers), {len(edges)} edges")

    dot_text = render_dot(nodes, edges)
    dot_path = OUT_DIR / "citation_graph.dot"
    dot_path.write_text(dot_text, encoding="utf-8")
    print(f"Wrote {dot_path}")

    svg_path = OUT_DIR / "citation_graph.svg"
    if try_render_svg(dot_path, svg_path):
        print(f"Wrote {svg_path}")
    else:
        # Write a tiny SVG placeholder pointing to the DOT, so the export exists
        placeholder = (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"720\" height=\"180\">\n"
            "  <rect width=\"100%\" height=\"100%\" fill=\"#f7f7f7\" stroke=\"#cccccc\"/>\n"
            "  <text x=\"24\" y=\"40\" font-family=\"Helvetica\" font-size=\"16\" fill=\"#333\">"
            "RMWND citation graph (SVG placeholder)</text>\n"
            "  <text x=\"24\" y=\"72\" font-family=\"Helvetica\" font-size=\"12\" fill=\"#555\">"
            f"{len(nodes)} nodes, {len(edges)} edges</text>\n"
            "  <text x=\"24\" y=\"96\" font-family=\"Helvetica\" font-size=\"12\" fill=\"#555\">"
            "Graphviz `dot` not on PATH; render with: dot -Tsvg citation_graph.dot -o citation_graph.svg</text>\n"
            "  <text x=\"24\" y=\"120\" font-family=\"Helvetica\" font-size=\"12\" fill=\"#555\">"
            "Or open citation_graph.html for an interactive D3 view.</text>\n"
            "</svg>\n"
        )
        svg_path.write_text(placeholder, encoding="utf-8")
        print(f"Wrote {svg_path} (placeholder — install graphviz for real rendering)")

    html_path = OUT_DIR / "citation_graph.html"
    html_path.write_text(render_html(nodes, edges), encoding="utf-8")
    print(f"Wrote {html_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

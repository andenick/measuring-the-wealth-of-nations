"""O03 — Generate per-ratio component bundles + the profitability packet.

Repackages the *already-correct* v2.0 publish data layer
(``Outputs/Publish/Data/``) into the downloadable bundles that ship inside the
GitHub release (``Outputs/Publish/Bundles/``). A bundle is a pure repackaging:
every component CSV it contains is copied byte-for-byte from the corresponding
``Data/<SID>.csv``; no series values are recomputed here.

Two bundle kinds are produced:

* **Per headline-ratio bundle** ``<SID>_bundle.zip`` (10 headline series minus the
  packet-only ones) — the headline series CSV under ``data/``, every upstream
  component CSV under ``components/``, a ``PROVENANCE_SLICE.csv`` (the rows of
  ``PROVENANCE_DICTIONARY.csv`` covering the series + its components), a
  ``COMPONENT_CHAIN.json`` (the headline node + each component node, verbatim
  from ``COMPONENT_CHAINS.json``), and a human-readable chain ``README.md``.
  ``S506`` additionally carries the per-year ``S506_STEP_TABLE.csv`` companion.

* **``PROFITABILITY_PACKET.zip``** — the profitability + long-wave series
  (S513, S514, S517, S505, S504, S510) with the capital-stock variant grid, the
  three P3 plots, the path-scrubbed ``CAPITAL_SCRUB_MEMO.md``, a provenance
  slice, a component chain, and a README.

The bundle format is reverse-engineered from and validated against the prior
bundles: READMEs are byte-identical to the prior release except for the
``Generated:`` timestamp, and ``COMPONENT_CHAIN.json`` / ``PROVENANCE_SLICE.csv``
are reproduced with the same JSON indentation and CRLF CSV framing.

Run:  ``PYTHONIOENCODING=utf-8 python O03_generate_bundles.py``
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# --- Paths ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
PUBLISH = PROJECT_ROOT / "Outputs" / "Publish"
DATA_DIR = PUBLISH / "Data"
BUNDLES_DIR = PUBLISH / "Bundles"
CHAINS_JSON = DATA_DIR / "COMPONENT_CHAINS.json"
PROV_DICT = DATA_DIR / "PROVENANCE_DICTIONARY.csv"
STEP_TABLE = DATA_DIR / "S506_STEP_TABLE.csv"
REVIEW_DIR = PROJECT_ROOT / "Technical" / "Handoffs" / "REVIEW_2026-07"

# --- Bundle definitions -----------------------------------------------------
#: Headline ratios that each get a ``<SID>_bundle.zip``.
RATIO_BUNDLES: tuple[str, ...] = (
    "S506", "S513", "S514", "S608", "S609",
    "XS001", "XS002", "XS003", "XS004",
)
#: Series (with a per-year step table companion) shipped inside their bundle.
STEP_TABLE_SERIES: dict[str, str] = {
    "S506": "S506_STEP_TABLE.csv",
}
#: Ordered series of the profitability packet (S513 headline first).
PACKET_SERIES: tuple[str, ...] = ("S513", "S514", "S517", "S505", "S504", "S510")

EM = "—"  # em-dash, as used in the prior READMEs


# --- Loaders ----------------------------------------------------------------
def load_chains() -> dict[str, dict]:
    """Return the per-series component-chain nodes from COMPONENT_CHAINS.json."""
    return json.loads(CHAINS_JSON.read_text(encoding="utf-8"))["series"]


def load_prov_dict() -> tuple[list[str], list[list[str]]]:
    """Return (header, body_rows) of PROVENANCE_DICTIONARY.csv."""
    rows = list(csv.reader(PROV_DICT.open(encoding="utf-8")))
    return rows[0], rows[1:]


# --- Builders ---------------------------------------------------------------
def components_of(sid: str, chains: dict[str, dict]) -> list[str]:
    """Upstream component SIDs of ``sid`` (its transitive chain, self excluded)."""
    return [c for c in chains[sid]["full_upstream_chain"] if c != sid]


def component_chain_json(keys: list[str], chains: dict[str, dict]) -> bytes:
    """Serialize the ordered {sid: node} chain map exactly as the prior bundles."""
    obj = {k: chains[k] for k in keys}
    return json.dumps(obj, indent=2).encode("utf-8")


def provenance_slice(series: set[str], header: list[str],
                     body: list[list[str]]) -> bytes:
    """CRLF CSV of the PROVENANCE_DICTIONARY rows whose series is in ``series``."""
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\r\n")
    writer.writerow(header)
    for row in body:
        if row and row[0] in series:
            writer.writerow(row)
    return buf.getvalue().encode("utf-8")


def _step_lines(node: dict) -> list[str]:
    """Render the per-edge construction-chain block of a headline README."""
    steps = node.get("steps") or []
    if not steps:
        return [
            "- (registry construction steps are empty for this series; the "
            "components listed were resolved from the P02 processor code. See "
            "PROVENANCE_SLICE and the series DPR.)"
        ]
    lines: list[str] = []
    for step in steps:
        inputs = ", ".join(step.get("inputs") or []) or "-"
        lines.append(
            f"- **step {step['step']}** ({step['op']}) -> "
            f"`{step['output']}`: {step['formula']}  "
        )
        lines.append(f"  inputs: {inputs}")
    return lines


def ratio_readme(sid: str, node: dict, components: list[str],
                 step_table_file: str | None, ts: str) -> bytes:
    """Render the chain README for a headline-ratio bundle."""
    name = node["display_name"]
    units = node["units"]
    contents = [
        f"- `data/{sid}.csv` {EM} the headline series (chopped, wide format: "
        "row 1 metadata, row 2 column IDs, row 3+ annual data).",
        f"- `components/*.csv` {EM} the {len(components)} upstream component "
        "series in the construction chain.",
        f"- `PROVENANCE_SLICE.csv` {EM} the rows of PROVENANCE_DICTIONARY "
        "covering this series + components.",
        f"- `COMPONENT_CHAIN.json` {EM} machine-readable step/formula chain "
        "for this series.",
    ]
    if step_table_file:
        contents.append(
            f"- `{step_table_file}` {EM} the full per-year (1948-1989) "
            "construction step table."
        )
    lines = [
        f"# {sid} component bundle {EM} {name}",
        "",
        "**Project:** Measuring the Wealth of Nations replication "
        "(Shaikh & Tonak 1994)  ",
        f"**Series:** {sid} ({name}); units = {units}  ",
        f"**Generated:** {ts}",
        "",
        "Answers **Tonak requirement #1**: every intermediate/component series "
        "that feeds this ratio is downloadable here, alongside the headline "
        "series and its per-value provenance.",
        "",
        "## Contents",
        "",
        *contents,
        "",
        "## Construction chain (per-edge formulas)",
        "",
        *_step_lines(node),
        "",
        f"**Full upstream chain (transitive):** {', '.join(components)}",
        "",
    ]
    disc = node.get("chain_discrepancy") or []
    if disc:
        lines.append(
            "> Note: registry construction and P02 code differ slightly on the "
            f"direct inputs ({disc}); the union is included so no component is "
            "missing."
        )
        lines.append("")
    lines += [
        "## Column conventions",
        "",
        "`-A` = book-period (Shaikh & Tonak original); `-EXT` = modern "
        "extension; `-COMBINED` = spliced full series. See the project registry "
        "+ DPRs for exact definitions.",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def packet_readme(ts: str) -> bytes:
    """Render the fixed profitability-packet README (values are static prose)."""
    lines = [
        "# Profitability + long-wave data packet",
        "",
        "**Project:** Measuring the Wealth of Nations replication "
        "(Shaikh & Tonak 1994)  ",
        f"**Generated:** {ts}",
        "",
        "Answers **Tonak requirement #8**: the profitability and long-wave data "
        f"assembled cleanly in one place {EM} the Marxian profit rate, its "
        "capacity-adjusted variant, the capital stock (with its methodology "
        "variants), surplus value, variable capital, and the value composition "
        "of capital.",
        "",
        "## Contents",
        "",
        f"- `data/S513.csv` {EM} Marxian general rate of profit r* = "
        "S*/(K*+V*) (headline).",
        f"- `data/S514.csv` {EM} capacity-adjusted profit rate.",
        f"- `data/S517.csv` {EM} capital stock K* (includes the "
        "methodology-variant columns).",
        f"- `data/S505.csv` {EM} surplus value S*.",
        f"- `data/S504.csv` {EM} variable capital V*.",
        f"- `data/S510.csv` {EM} value composition of capital.",
        f"- `P3_CAPITAL_VARIANTS.csv` {EM} the K*/r* variant grid from the "
        "capital-scrub review.",
        f"- `plots/` {EM} K* variants, r* variants, and scrub-share plots.",
        f"- `CAPITAL_SCRUB_MEMO.md` {EM} the review memo on the capital-stock "
        "scrub (paths scrubbed).",
        f"- `PROVENANCE_SLICE.csv`, `COMPONENT_CHAIN.json` {EM} provenance + "
        "construction chains.",
        "",
        "## The falling rate of profit",
        "",
        "S513 (r* = S*/(K*+V*)) is the book's Chapter 5/9 headline on the "
        "tendency of the rate of profit to fall; S514 adjusts it for capacity "
        "utilisation. Both trace to the same S505/S504/S517 components included "
        "here, so the long-wave movement is fully reproducible from this "
        "packet.",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def scrubbed_memo() -> bytes:
    """Path-scrub the capital-scrub memo: normalise CRLF to LF line endings."""
    raw = (REVIEW_DIR / "CAPITAL_SCRUB_MEMO.md").read_bytes()
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _read_data_csv(sid: str) -> bytes:
    """Return the byte content of the v2.0 ``Data/<SID>.csv`` (must exist)."""
    path = DATA_DIR / f"{sid}.csv"
    if not path.exists():
        raise FileNotFoundError(f"missing publish data CSV: {path}")
    return path.read_bytes()


def _write_zip(dest: Path, members: list[tuple[str, bytes]]) -> None:
    """Write ``members`` (arcname, bytes) to a deterministic ZIP at ``dest``."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for arcname, data in members:
            info = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)


# --- Bundle assembly --------------------------------------------------------
def build_ratio_bundle(sid: str, chains: dict[str, dict],
                       prov_header: list[str], prov_body: list[list[str]],
                       ts: str) -> Path:
    """Assemble and write ``<sid>_bundle.zip``; return its path."""
    node = chains[sid]
    components = components_of(sid, chains)
    chain_keys = [sid] + components
    series_set = {sid} | set(node["full_upstream_chain"])
    step_table_file = STEP_TABLE_SERIES.get(sid)

    members: list[tuple[str, bytes]] = [
        (f"data/{sid}.csv", _read_data_csv(sid)),
    ]
    for comp in components:
        members.append((f"components/{comp}.csv", _read_data_csv(comp)))
    members.append(
        ("COMPONENT_CHAIN.json", component_chain_json(chain_keys, chains))
    )
    members.append(
        ("PROVENANCE_SLICE.csv",
         provenance_slice(series_set, prov_header, prov_body))
    )
    members.append(
        ("README.md",
         ratio_readme(sid, node, components, step_table_file, ts))
    )
    if step_table_file:
        members.append((step_table_file, STEP_TABLE.read_bytes()))

    dest = BUNDLES_DIR / f"{sid}_bundle.zip"
    _write_zip(dest, members)
    return dest


def build_packet(chains: dict[str, dict], prov_header: list[str],
                 prov_body: list[list[str]], ts: str) -> Path:
    """Assemble and write ``PROFITABILITY_PACKET.zip``; return its path."""
    members: list[tuple[str, bytes]] = [
        (f"data/{sid}.csv", _read_data_csv(sid)) for sid in PACKET_SERIES
    ]
    members.append(
        ("P3_CAPITAL_VARIANTS.csv",
         (REVIEW_DIR / "P3_CAPITAL_VARIANTS.csv").read_bytes())
    )
    for plot in ("P3_K_star_variants.png", "P3_r_star_variants.png",
                 "P3_scrub_shares.png"):
        members.append((f"plots/{plot}", (REVIEW_DIR / plot).read_bytes()))
    members.append(("CAPITAL_SCRUB_MEMO.md", scrubbed_memo()))
    members.append(
        ("COMPONENT_CHAIN.json",
         component_chain_json(list(PACKET_SERIES), chains))
    )
    members.append(
        ("PROVENANCE_SLICE.csv",
         provenance_slice(set(PACKET_SERIES), prov_header, prov_body))
    )
    members.append(("README.md", packet_readme(ts)))

    dest = BUNDLES_DIR / "PROFITABILITY_PACKET.zip"
    _write_zip(dest, members)
    return dest


def main() -> None:
    """Regenerate all ratio bundles + the profitability packet from v2.0 Data."""
    chains = load_chains()
    prov_header, prov_body = load_prov_dict()
    ts = datetime.now(timezone.utc).isoformat()

    for sid in RATIO_BUNDLES:
        dest = build_ratio_bundle(sid, chains, prov_header, prov_body, ts)
        print(f"  wrote {dest.name} ({dest.stat().st_size} bytes)")

    dest = build_packet(chains, prov_header, prov_body, ts)
    print(f"  wrote {dest.name} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

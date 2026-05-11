"""Centralised path resolution for the AS2 Anu Replicator package.

Every module that needs to locate a file imports the constant it needs from
here.  All paths are resolved relative to the package root (one level above
this file) so the layout stays relocatable.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── data layer ───────────────────────────────────────────────
USER_INPUTS = ROOT / "data" / "user-inputs"
RAW_DATA = ROOT / "data" / "raw-data"
FINAL_DATA = ROOT / "data" / "final-data"

CHOPPED_IN = USER_INPUTS / "chopped"
PROVENANCE = USER_INPUTS / "provenance"
RESEARCH = USER_INPUTS / "research"

API_RAW = RAW_DATA / "api"
PARSED_RAW = RAW_DATA / "parsed"

SERIES_OUT = FINAL_DATA / "series"
CHOPPED_OUT = FINAL_DATA / "chopped"
EXTENBOOKS = FINAL_DATA / "extenbooks"
SHINY_OUT = FINAL_DATA / "shiny"
FIGURES_OUT = FINAL_DATA / "figures"
REPORTS = FINAL_DATA / "reports"
LOGS = FINAL_DATA / "logs"

# ── external references (ST2 project layout) ─────────────────
TECHNICAL = ROOT.parent
PROJECT = TECHNICAL.parent

INPUTS = PROJECT / "Inputs"
ST_CHOPPED = INPUTS / "ST_Chopped"
API_DATA = INPUTS / "API_Data"
IO_MATRICES = INPUTS / "IO_Matrices"
NIPA_DATA = INPUTS / "NIPA"
KB = TECHNICAL / "Knowledge_Base"

SHINY_CATALOG = (
    TECHNICAL / "ShinyApp" / "data" / "catalogs"
    / "DEFINITIVE_SERIES_CATALOG.json"
)

# ── validation & adjustment layer ───────────────────────────
ADJUSTED = ROOT / "data" / "adjusted-final-data"
VALIDATION_LOGS = LOGS / "validation"
SCRATCH = ROOT / "data" / "scratch"

# ── config / scripts ────────────────────────────────────────
CONFIG = ROOT / "config"

# Canonical registry lives one level above the Replicator package,
# in Technical/series_registry.json.  Fall back to the local copy.
_CANONICAL_REGISTRY = ROOT.parent / "series_registry.json"
REGISTRY = _CANONICAL_REGISTRY if _CANONICAL_REGISTRY.exists() else CONFIG / "series_registry.json"
SCRIPTS_LOADING = ROOT / "scripts" / "loading"
SCRIPTS_PROCESSING = ROOT / "scripts" / "processing"
SCRIPTS_VALIDATION = ROOT / "scripts" / "validation"
SCRIPTS_MANUAL = ROOT / "scripts" / "manual"
SCRIPTS_EXPLORATION = ROOT / "scripts" / "exploration"


def ensure_dirs() -> None:
    """Create every output directory that the pipeline may write to."""
    for d in [
        API_RAW, PARSED_RAW, SERIES_OUT, CHOPPED_OUT,
        EXTENBOOKS, SHINY_OUT, FIGURES_OUT, REPORTS, LOGS,
        ADJUSTED, VALIDATION_LOGS, SCRATCH,
    ]:
        d.mkdir(parents=True, exist_ok=True)


def chopped_path(chapter: int, filename: str) -> Path:
    """Return the input path for a chopped chapter file in Inputs/ST_Chopped/."""
    return ST_CHOPPED / f"ch{chapter:02d}" / filename


def api_path(api_name: str, series_id: str, date_str: str) -> Path:
    """Return the raw-data path for an API response cache file."""
    return API_RAW / f"{api_name}_{series_id}_{date_str}.json"


def parsed_path(series_id: str) -> Path:
    """Return the raw-data path for a parsed CSV file."""
    return PARSED_RAW / f"{series_id}_parsed.csv"

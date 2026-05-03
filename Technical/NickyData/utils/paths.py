"""Centralised path resolution for the AS2 NickyData package.

Every module that needs to locate a file imports the constant it needs from
here. All paths are resolved relative to the package root (NickyData/).
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

# Book replication output (T-series)
BOOK_DATA = FINAL_DATA / "book"
SERIES_OUT = BOOK_DATA / "series"
CHOPPED_OUT = BOOK_DATA / "chopped"
EXTENBOOKS = BOOK_DATA / "extenbooks"

# External study output (N-series)
STUDIES_DATA = FINAL_DATA / "studies"
STUDIES_OUT = STUDIES_DATA / "series"
STUDIES_CHOPPED = STUDIES_DATA / "chopped"
STUDIES_EXTENBOOKS = STUDIES_DATA / "extenbooks"

# Shared output locations
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

# ── config / code ────────────────────────────────────────────
CONFIG = ROOT  # NickyData root contains config files directly

# Registry: project_registry.json in NickyData root
# Fall back to series_registry.json for backward compatibility
_PROJECT_REGISTRY = ROOT / "project_registry.json"
_SERIES_REGISTRY = ROOT / "series_registry.json"
REGISTRY = _PROJECT_REGISTRY if _PROJECT_REGISTRY.exists() else _SERIES_REGISTRY

# Code phase directories (NickyData convention: code/ not scripts/)
SCRIPTS_LOADING = ROOT / "code" / "loading"
SCRIPTS_PROCESSING = ROOT / "code" / "processing"
SCRIPTS_VALIDATION = ROOT / "code" / "validation"
SCRIPTS_MANUAL = ROOT / "code" / "manual"
SCRIPTS_EXPLORATION = ROOT / "code" / "exploration"
SCRIPTS_ANALYSIS = ROOT / "code" / "analysis"
SCRIPTS_OUTPUTS = ROOT / "code" / "outputs"
SCRIPTS_SETUP = ROOT / "code" / "setup"

# Output directories
OUTPUTS = ROOT / "outputs"
ANALYSIS_OUT = OUTPUTS / "analysis"
DELIVERABLES = OUTPUTS / "deliverables"
MASTER_DB = OUTPUTS / "master_database"


def ensure_dirs() -> None:
    """Create every output directory that the pipeline may write to."""
    for d in [
        API_RAW, PARSED_RAW,
        SERIES_OUT, CHOPPED_OUT, EXTENBOOKS,
        STUDIES_OUT, STUDIES_CHOPPED, STUDIES_EXTENBOOKS,
        SHINY_OUT, FIGURES_OUT, REPORTS, LOGS,
        ADJUSTED, VALIDATION_LOGS, SCRATCH,
        ANALYSIS_OUT, DELIVERABLES, MASTER_DB,
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

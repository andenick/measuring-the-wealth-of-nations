"""Centralized path resolution for v7.0 pipeline.

All paths relative to NickyData root. Reuses the same data directories as v6.0
so both pipelines can coexist during migration.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # NickyData/

# Config
CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

# Data layer (shared with v6.0)
USER_INPUTS = ROOT / "data" / "user-inputs"
RAW_DATA = ROOT / "data" / "raw-data"
FINAL_DATA = ROOT / "data" / "final-data"

API_RAW = RAW_DATA / "api"
PARSED_RAW = RAW_DATA / "parsed"

BOOK_SERIES = FINAL_DATA / "book" / "series"
BOOK_CHOPPED = FINAL_DATA / "book" / "chopped"
BOOK_EXTENBOOKS = FINAL_DATA / "book" / "extenbooks"

STUDIES_SERIES = FINAL_DATA / "studies" / "series"
STUDIES_CHOPPED = FINAL_DATA / "studies" / "chopped"

LOGS = FINAL_DATA / "logs"
OUTPUTS = ROOT / "outputs"
ANALYSIS_OUT = OUTPUTS / "analysis"

# External project references
PROJECT = ROOT.parent.parent  # ST2/
INPUTS = PROJECT / "Inputs"
ST_CHOPPED = INPUTS / "ST_Chopped"
API_DATA = INPUTS / "API_Data"
IO_MATRICES = INPUTS / "IO_Matrices"


def ensure_dirs():
    for d in [API_RAW, PARSED_RAW, BOOK_SERIES, BOOK_CHOPPED, BOOK_EXTENBOOKS,
              STUDIES_SERIES, STUDIES_CHOPPED, LOGS, ANALYSIS_OUT, OUTPUTS]:
        d.mkdir(parents=True, exist_ok=True)

"""Central path resolution for the replication pipeline."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Data tiers
DATA_SOURCE       = ROOT / "data" / "source"
DATA_RAW          = ROOT / "data" / "raw"
DATA_INTERMEDIATE = ROOT / "data" / "intermediate"
DATA_FINAL        = ROOT / "data" / "final"

# Source data subdirs
BOOK_TABLES       = DATA_SOURCE / "book_tables"
EXTERNAL_STUDIES  = DATA_SOURCE / "external_studies"
CONCORDANCES      = DATA_SOURCE / "concordances"

# Alias for backward compatibility / Wave 4 imports
EXTERNAL_STUDIES_DIR = EXTERNAL_STUDIES

# Validation outputs
VALIDATION_DIR    = DATA_INTERMEDIATE / "validation"

# Top-level artifacts
REGISTRY          = ROOT / "series_registry.json"
LEDGER            = ROOT / "ANU_LEDGER.json"
PIPELINE_STATE    = ROOT / "PIPELINE_STATE.json"

# Research and docs
RESEARCH_DIR      = ROOT / "research"
DOCS_SERIES       = ROOT / "docs" / "series"

# Output directories
CHOPPED_DIR       = ROOT / "chopped"
EXTENBOOKS_DIR    = ROOT / "extenbooks"

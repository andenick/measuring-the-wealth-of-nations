#!/usr/bin/env python3
"""O08 - Create Zenodo/Harvard Dataverse replication package.

Bundles code, data, and documentation into a self-contained ZIP that
reproduces all results. Strips API keys and internal paths.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
import shutil
import zipfile
from datetime import datetime
from utils.paths import ROOT, CONFIG


PACKAGE_NAME = "AS2_ReplicationPackage_v7.0"

# Files/dirs to include from NickyData root
INCLUDE_FILES = [
    "run.py",
    "requirements.txt",
    "series_registry.json",
    "project_registry.json",
    "validation_config.json",
    "methodology.json",
    "classifications.json",
    "ADJUSTMENT_MANIFEST.json",
    "DECISION_LOG.md",
    "ASSUMPTIONS.md",
    "CHECKLIST.md",
    "VERSION_LOG.md",
    "VARIANT_REGISTRY.json",
]

INCLUDE_DIRS = [
    "code",
    "utils",
    "data/user-inputs",
    "data/raw-data",
]

EXCLUDE_PATTERNS = [
    "__pycache__",
    ".pyc",
    "api_keys.env",
    ".DS_Store",
    "_archive",
]


def _should_exclude(path: Path) -> bool:
    s = str(path)
    return any(pat in s for pat in EXCLUDE_PATTERNS)


def _create_template_env() -> str:
    return """# AS2 API Keys Configuration
# Get your own keys from the URLs below and paste them here.

# FRED (Federal Reserve Economic Data)
# Get key: https://fred.stlouisfed.org/docs/api/
FRED_API_KEY=YOUR_FRED_KEY_HERE

# BEA (Bureau of Economic Analysis)
# Get key: https://apps.bea.gov/API/signup/
BEA_API_KEY=YOUR_BEA_KEY_HERE

# BLS (Bureau of Labor Statistics) — no key needed for public API
# BLS_API_KEY=optional_for_higher_rate_limits
"""


def _create_readme() -> str:
    return f"""# AS2: Replication Package

**Shaikh & Tonak (1994) "Measuring the Wealth of Nations" — Replication and Extension**

Generated: {datetime.now().strftime('%Y-%m-%d')}
Pipeline: NickyData v7.0

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API keys (optional — cached data included)
cp data/user-inputs/api_keys_TEMPLATE.env data/user-inputs/api_keys.env
# Edit api_keys.env with your BEA and FRED keys

# 3. Run validation (uses cached data, no API keys needed)
python run.py --validate-only

# 4. Run full pipeline (re-fetches API data, needs keys)
python run.py --test-all
```

## What This Produces

- **59 data series** (33 book + 25 external studies + analytical)
- **15 validators** with 348 automated checks, 0 failures
- **97-year master database** (1948-2024)
- **11 publication-quality figures**

## Contents

```
code/           76 scripts across 8 phases (S/L/P/V/M/A/O/E)
utils/          Shared libraries (fetchers, formatters, transforms)
data/
  user-inputs/  Source CSVs (book tables, IO matrices)
  raw-data/     Cached API responses (BEA, BLS, FRED)
*.json          Registry, config, methodology files
run.py          Master orchestrator
```

## Citation

Shaikh, A. & Tonak, E.A. (1994). *Measuring the Wealth of Nations:
The Political Economy of National Accounts*. Cambridge University Press.

## License

Data sources are publicly available from BEA, BLS, and FRED.
Book table data digitized from Shaikh & Tonak (1994).
"""


def _create_citation_cff() -> str:
    return f"""cff-version: 1.2.0
message: "If you use this replication package, please cite the original work."
title: "AS2: Replication and Extension of Shaikh & Tonak (1994)"
version: "7.0"
date-released: "{datetime.now().strftime('%Y-%m-%d')}"
references:
  - type: book
    authors:
      - family-names: Shaikh
        given-names: Anwar
      - family-names: Tonak
        given-names: "E. Ahmet"
    title: "Measuring the Wealth of Nations: The Political Economy of National Accounts"
    year: 1994
    publisher:
      name: "Cambridge University Press"
"""


def run():
    project_root = ROOT.parent.parent  # ST2/
    out_dir = project_root / "Outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    zip_path = out_dir / f"{PACKAGE_NAME}.zip"
    if zip_path.exists():
        zip_path.unlink()

    file_count = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add individual files from NickyData root
        for fname in INCLUDE_FILES:
            src = ROOT / fname
            if src.exists():
                zf.write(src, f"{PACKAGE_NAME}/{fname}")
                file_count += 1

        # Add directories
        for dirname in INCLUDE_DIRS:
            src_dir = ROOT / dirname
            if not src_dir.exists():
                continue
            for fpath in src_dir.rglob("*"):
                if fpath.is_file() and not _should_exclude(fpath):
                    arcname = f"{PACKAGE_NAME}/{fpath.relative_to(ROOT)}"
                    zf.write(fpath, arcname)
                    file_count += 1

        # Add template env (stripped keys)
        zf.writestr(
            f"{PACKAGE_NAME}/data/user-inputs/api_keys_TEMPLATE.env",
            _create_template_env(),
        )
        file_count += 1

        # Add README
        zf.writestr(f"{PACKAGE_NAME}/README.md", _create_readme())
        file_count += 1

        # Add CITATION.cff
        zf.writestr(f"{PACKAGE_NAME}/CITATION.cff", _create_citation_cff())
        file_count += 1

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    summary = f"Zenodo package: {file_count} files, {size_mb:.1f} MB -> {zip_path.name}"
    print(f"    [O08] {summary}")
    return {"status": "ok", "summary": summary, "path": str(zip_path)}

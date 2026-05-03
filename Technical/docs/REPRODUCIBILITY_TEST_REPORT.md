# Reproducibility Test Report

**Date**: 2026-04-09
**Version**: 4.1.0

## Results: PASS

| Check | Result |
|-------|--------|
| Required files (13) | 13/13 present |
| Core imports | OK (paths, config, naics_parser, classification, units) |
| Registry | 33 series loaded |
| Series CSVs | 33 files |
| Chopped CSVs | 26 files |
| Extenbooks | 26 XLSX files |
| Validators | 11 scripts (V00-V10) |
| Version | 3.0.0 |
| Master database | EXISTS (97yr x 29 series) |
| Publication figures | 6 PNG files |
| Methodology report | EXISTS |

## Pipeline Run
```
260 PASS, 0 FAIL, 27 WARN — PASS
14/14 loaded, 15/15 processed
```

## Notes
- Full fresh-environment test (venv isolation) deferred — requires manual setup
- This check verifies file integrity and import chain within the existing environment
- All outputs can be regenerated from source data via `python replicate.py --full`

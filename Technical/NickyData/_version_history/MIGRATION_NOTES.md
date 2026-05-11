# Migration Notes: ANU_REPLICATOR → NickyData

**Date**: 2026-04-09
**From**: ANU_REPLICATOR v3.0 (Anu Replicator, 4-phase L/P/V/M)
**To**: NickyData v1.1 (8-phase S/L/P/V/M/A/O/E)

## What Changed

| Aspect | Before | After |
|--------|--------|-------|
| Location | `Technical/ANU_REPLICATOR/` | `Technical/NickyData/` |
| Orchestrator | `replicate.py` | `run.py` |
| Config | `series_registry.json` | `project_registry.json` |
| Library | `lib/` | `utils/` |
| Scripts | `scripts/{phase}/` | `code/{phase}/` |
| Phases | 4 (L/P/V/M) | 8 (S/L/P/V/M/A/O/E) |
| External papers | "Chapters 10-17" | "Studies 1-8" |
| Book data | `data/final-data/series/T*.csv` | `data/final-data/book/series/` |
| Study data | `data/final-data/series/N*.csv` | `data/final-data/studies/series/` |

## What Did NOT Change

- All T-series and N-series data values preserved exactly
- All L##, P##, V##, M##, O##, E## script logic unchanged
- All validation results maintained
- All lib/utils module code unchanged

## New Components

- `code/setup/S01_validate_environment.py` — environment validation
- `code/analysis/A01-A04` — cross-study analysis (migrated from O03)
- `project_registry.json` — unified book + studies registry
- `data/final-data/book/` vs `data/final-data/studies/` separation

## Archive

Previous version archived at: `Technical/_archive/v5.0_2026-04-09/ANU_REPLICATOR/`

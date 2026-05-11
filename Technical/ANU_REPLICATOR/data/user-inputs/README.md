# User Inputs Directory

Per Anu Replicator v3.0, this directory contains human-provided inputs that feed into the loading phase.

## AS2 Path Mapping

ST2 stores its inputs at the **project level** per Druck standards, not inside the Replicator package. The mapping is handled by `lib/paths.py`:

| Replicator Standard | AS2 Actual Location | paths.py Constant |
|---------------------|---------------------|-------------------|
| `data/user-inputs/chopped/` | `Inputs/ST_Chopped/` | `ST_CHOPPED` |
| `data/user-inputs/provenance/` | `Technical/docs/series/` | (accessed directly) |
| `data/user-inputs/research/` | `Technical/research/` | (accessed directly) |

## Subdirectories

- `chopped/` — See README for pointer to actual input location
- `provenance/` — See README for pointer to DPR/EPR docs
- `research/` — Contains S###_research.json files (populated)

## Why Not Duplicate?

Duplicating source files inside the Replicator would violate Druck's read-only Inputs/ principle and create synchronization issues. The path mapping in `lib/paths.py` provides seamless access.

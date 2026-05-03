# Exploration Scripts (E##)

Standalone exploratory scripts for testing new methods, prototyping data
processing, and investigating data questions. These scripts are **never deleted**
-- they form a permanent record of the research process.

## Naming Convention

- `E01_description.py` through `E99_description.py`
- Scripts are NOT auto-discovered by the orchestrator
- Each script is self-contained and runs independently

## Outputs

Exploration outputs go to `data/scratch/` (cleared periodically) or are
printed to console. They do not feed into the main pipeline.

## Scripts

| Script | Purpose |
|--------|---------|
| `E01_explore_wave3.py` | Quick test of Wave 3 components (L13, L14, P15) |

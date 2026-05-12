# Anu Suite - Data Construction Framework

**Version**: 6.0
**Last Updated**: 2026-04-08
**Canonical Source**: `

---

## Overview

The Anu Suite is a 12-skill framework for agent-driven data construction projects covering the full lifecycle from research through visualization and audit. It produces outputs reproducible without agents.

**Note**: The canonical skill definitions live in `Council/Druck/.claude/skills/`. This directory contains project-local reference copies and templates. Always defer to the Council versions for the latest specifications.

---

## All 12 Skills (v6.0)

### Core Pipeline Skills (sequential)

| # | Skill | Version | Stage | Purpose |
|---|-------|---------|-------|---------|
| 0 | **anu-adequacy** | 1.2 | Gate | Pre-pipeline readiness check (KB + data sufficiency) |
| 1 | **anu-research** | 2.0 | 1 | Mine Knowledge Base for series methodology |
| 2 | **anu-ingestion** | 4.0 | 2 | Data import, absorption, decomposition, provenance (DPR/FPR) |
| 3 | **anu-extension** | 3.0 | 3 | Maximum-faithfulness data extension (EPR) |
| 4 | **anu-replicator** | 3.0 | 4 | Self-contained replication package (L##/P##/V##/M##) |
| 5 | **anu-chopped** | 1.0 | 5 | Self-documenting CSV format |
| 6 | **anu-extenbook** | 3.0 | 5 | Series-level Excel workbooks |
| 7 | **anu-shiny** | 4.3 | 5b-6 | Interactive visualization (R Shiny + Plotly) |
| 8 | **anu-review** | 2.0 | 6 | 12-dimension quality audit |

### Support Skills (parallel/on-demand)

| # | Skill | Version | Purpose |
|---|-------|---------|---------|
| 9 | **anu-pipeline** | 1.0 | Master orchestrator (10 stages) |
| 10 | **anu-variant** | 1.4 | Methodology variant tracking |
| 11 | **anu-ledger** | 2.2 | Auto-generated artifact inventory |

---

## Pipeline Flow

```
Raw Sources (PDF/Excel/API)
         |
    [anu-adequacy] ← GATE (must score >= 80%)
         |
    [anu-research] → S###_research.json
         |
    [anu-ingestion] → series_registry.json, DPRs, decompositions
         |
    [anu-extension] → EPRs, EXTENSION_LOG.json
         |
    [anu-replicator]
      ├─ Loading (L##) → raw-data/
      ├─ Processing (P##) → final-data/ (series, chopped, extenbooks)
      ├─ Validation (V##) → VALIDATION_REPORT.json
      └─ Manual Adjust (M##) → adjusted-final-data/
         |
    [anu-chopped] + [anu-extenbook] → validated CSVs + XLSX
         |
    [anu-shiny] → interactive visualization app
         |
    [anu-review] → quality score + certification
```

---

## Local Reference Copies

This directory contains templates and scripts ported from the canonical source:

### Present (ported from CD2)
- `anu-standard/` — Core DPR/FPR templates and validation (v2.2, **archived**: replaced by anu-ingestion v4.0)
- `anu-extension/` — EPR templates, transition analysis
- `anu-extenbook/` — Excel workbook generation
- `anu-chopped/` — CSV format spec, conversion scripts, validator
- `anu-review/` — Review report, checklist, gap analysis templates
- `ANU_STANDARD_UNIFIED.md` — Consolidated v2.2 spec

### Not Locally Copied (use Council canonical)
- anu-adequacy — Pre-pipeline readiness gate
- anu-research — KB mining framework
- anu-ingestion — Comprehensive data intake (replaces anu-standard)
- anu-replicator — 4-phase replication package
- anu-shiny — Interactive visualization standard
- anu-pipeline — Master orchestrator
- anu-variant — Methodology variant tracking
- anu-ledger — Auto-generated artifact inventory

---

## Key Concepts

### Series Identifiers
- **Standard**: `S###` (e.g., S001, S015)
- **AS2 variant**: `T###` (e.g., T501, T601) — chapter-based table numbering (see DEC-001)
- Subseries: `-A`, `-B`, `-EXT`, `-COMBINED` suffixes

### Single Source of Truth
- `series_registry.json` — all series metadata, subsources, construction steps, extension config

### Quality Certification
- **EXEMPLARY**: >= 95% — Reference implementation
- **COMPLETE**: >= 85% — Meets all core requirements
- **ADEQUATE**: >= 70% — Functional with documented gaps
- **INCOMPLETE**: < 70% — Requires attention

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 6.0 | 2026-04-08 | Updated to 12-skill framework, v3.0 Replicator (L/P/V/M) |
| 2.3 | 2026-02-11 | Added anu-chopped |
| 2.2 | 2026-02-02 | Consolidated to project, added anu-extenbook |
| 2.1 | 2026-01-28 | Added anu-review |
| 2.0 | 2025-12-15 | Introduced EPR system |
| 1.0 | 2025-10-01 | Initial DPR framework |

---

*Consolidated reference for the AS2 project. Canonical definitions at Council/Druck/.claude/skills/*

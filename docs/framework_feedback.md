# Anu Framework Feedback from the RMWND Build

The 21-commit RMWND rebuild surfaced 12 friction points in the Anu Framework v10.0. Three RFC-style documents capture what was learned and propose remediations. They live in the framework's canonical docs directory:

| Document | Location | Length | Audience |
|---|---|---|---|
| **`LESSONS_LEARNED_RMWND_2026.md`** | `Council/Druck/docs/` | ~3000 words | future agents starting a similar rebuild |
| **`ANU_FRAMEWORK_IMPROVEMENTS_RFC.md`** | `Council/Druck/docs/` | ~6000 words | framework maintainers |
| **`ANU_REBUILD_META_SKILL.md`** | `Council/Druck/docs/` | ~2500 words | proposed skill spec for `anu-rebuild` v1.0 |

## Summary of proposed framework changes

**Two new skills proposed**:

1. `anu-scaffold` v1.0 — generates L01/P02/V03 stubs from registry entries. Replaces this build's `MIGRATION/_gen_*_scripts.py` generators.
2. `anu-rebuild` v1.0 — meta-skill wrapping the 6-wave (Foundation → per-cohort → Distribution → Polish) cadence proven on RMWND. Replaces the ad-hoc planning that consumed ~2 hours of upfront work.

**Enhancements to ten existing skills**:

| Skill | Change | Source friction |
|---|---|---|
| `anu-ingestion` v4.0 → v4.1 | `migrate-scheme`, `batch-create-dpr`, status-taxonomy enum | Frictions 1, 2, 7 |
| `anu-extension` v3.4 → v3.5 | `batch-create-epr` | Friction 2 |
| `anu-research` v2.0 → v2.1 | `port --from <predecessor>` | Friction 6 |
| `anu-publish` v1.1 → v1.2 | `audit.py` ships as canonical impl; `.publish_ignore` formalized | Friction 4 |
| `anu-replicator` v3.0 → v3.1 | `lib/` structure prescribed; helper templates | Friction 5 |
| `anu-data` v2.0 → v2.1 | BEA/BLS/FRED cache schemas documented | Friction 10 |
| `anu-pipeline` v3.1 → v3.2 | `run.py` template scaffolded by `init` | Friction 9 |
| `anu-doctor` v1.0 → v1.1 | `project` mode (10 P##-checks) | Friction 12 |
| _(cross-skill)_ | `DIVERGENCE_REGISTER.json` hoisted to top-level + shared `register_divergence()` helper | Friction 3 |

**Framework version bump**: v10.0 → v11.0 (justified by 2 new skills + breaking status-taxonomy schema change).

**Estimated benefit**: 30-50% reduction in rebuild session count for future projects. RMWND baseline was 12-15 sessions; target is 7-10.

## How the build informed each proposal

Every friction point in the RFC has a concrete antecedent in this repo:

- 17 generator scripts in `MIGRATION/_gen_*.py` → batch-creation commands (Frictions 2, 6, 8)
- `MIGRATION/divergences_from_ST2.md` → unified divergence register (Friction 3)
- `code/S00_setup/S06_publish_scrub_audit.py` → ships as `anu-publish/audit.py` (Friction 4)
- `code/utils/{series,bea_cache,io_matrix,fred_cache,paths,io}.py` → `anu-replicator lib/` templates (Frictions 5, 10)
- 10 ad-hoc status values across the registry → standardized enum (Friction 7)
- The 6-wave cadence in `docs/ROADMAP.md` and `docs/IMPLEMENTATION_PLAN.md` → formalized as `anu-rebuild` skill (Friction 11)

## Status

The RFCs are DRAFT, ready for framework maintainer review. Actual implementation (editing the 20 SKILL.md files) is a separate workstream once the proposals are approved.

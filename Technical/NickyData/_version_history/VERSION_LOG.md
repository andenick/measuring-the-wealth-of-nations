# AS2 NickyData Version Log

## v6.0.0 — NickyData Restructure (2026-04-09)

**Scope**: Complete restructuring from ANU_REPLICATOR to NickyData architecture

**Changes**:
- Migrated from Anu Replicator v3.0 (4-phase) to NickyData v1.1 (8-phase)
- External papers renamed from "Chapters 10-17" to "Studies 1-8"
- Book series (T-series) separated into `data/final-data/book/`
- Study series (N-series) separated into `data/final-data/studies/`
- Created unified `project_registry.json` with book_replication + studies sections
- Added S## setup phase and A## analysis phase
- `lib/` renamed to `utils/`
- `scripts/` renamed to `code/`
- Previous version archived at `_archive/v5.0_2026-04-09/`

**Preserved**: All data values, validation results, and computed series unchanged.

---

*For pre-NickyData history, see Technical/VERSION_LOG.md (v1.0-v5.0)*

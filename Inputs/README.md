# AS2 Inputs

**Read-only source data for the AS2 replication and extension package.**

All files in this directory are treated as immutable originals. Processing happens in `Technical/`; results go to `Outputs/`.

---

## Directory Structure

| Directory | Content | Source |
|-----------|---------|--------|
| `BookTables/ch05/` | Tables 5.5-5.14 (exploitation, labor, surplus value) | Shaikh & Tonak (1994) |
| `BookTables/ch06/` | NSW tables | Shaikh & Tonak (1994) |
| `BookTables/ch07/` | IO application tables | Shaikh & Tonak (1994) |
| `BookTables/ch09/` | Summary tables | Shaikh & Tonak (1994) |
| `BookTables/appendix/` | Appendix E data tables | Shaikh & Tonak (1994) |
| `IO_Matrices/` | Benchmark IO tables (A, L, Z matrices, 1947-1977) | Migrated from Shaikh Tonak project |
| `NIPA/` | BEA NIPA table extracts (1948-1989 book period) | Migrated from Shaikh Tonak project |
| `BLS/` | Employment and production worker data | BLS API / manual collection |
| `Concordances/` | SIC-NAICS industry classification mappings | Migrated from Shaikh Tonak Phase 3 |
| `API_Data/BEA/` | BEA API downloads for extension period | Robin/BEA |
| `API_Data/FRED/` | FRED API downloads for extension period | Robin/FRED |
| `API_Data/BLS/` | BLS API downloads for extension period | Robin/BLS |
| `ExternalSources/Mohun/` | Mohun productive labor comparison data | Migrated from Shaikh Tonak |
| `ExternalSources/Tonak_Benchmarks/` | Tonak benchmark files and correspondence | Migrated from Shaikh Tonak Knowledge_Base |

## Data Provenance

All data in this directory traces to one of:
1. **Shaikh & Tonak (1994)** book tables (digitized)
2. **Shaikh Tonak project** authoritative datasets (Phases 1-3)
3. **BEA/FRED/BLS API** downloads for extension periods
4. **External researchers** (Mohun, Moos, Tsoulfidis) for comparison/validation

## Rules

- **Never modify files in this directory.** All transformations happen in `Technical/scripts/`.
- **One sheet per Excel file.** No multi-sheet workbooks.
- **UTF-8 encoding** for all CSV files.
- **Provenance metadata** must accompany every new data file added.

---

*AS2 Inputs - February 23, 2026*

# T401 — A-Matrix (Input-Output Technical Coefficients)

## Quick Reference

| Field | Value |
|-------|-------|
| Series ID | T401 |
| Chapter | 4 |
| Book Table | 4.1 |
| Period | 1947, 1958, 1963, 1967, 1972, 1977 (6 SIC benchmarks) + 1997, 2002, 2007, 2012, 2017 (5 NAICS benchmarks) |
| Units | matrix (85x85 SIC, 71-sector NAICS) |
| Status | benchmark_only |

## Source Context

The A-matrix contains technical coefficients a_ij = intermediate input from sector i used per unit of output in sector j. It is the foundation of the IO framework for computing labor values (Chapter 7) and sector classification (productive vs unproductive).

## Subsources

- **T401-A (SIC)**: 6 BEA benchmark IO tables (1947-1977), 85x85 sectors. Source: `Inputs/IO_Matrices/`
- **T401-NAICS**: 5 NAICS benchmark IO tables (1997-2017), ~71 sectors. Source: `Inputs/IO_Matrices/NAICS/`

## Transformation Chain

1. L11 loads raw IO matrices from CSV files
2. P13 parses into A-matrices, computes Leontief inverse B = (I-A)^{-1}
3. Classifies sectors as productive (75) or unproductive (7) per Appendix B

## Validation

- V10 IO consistency: 21 PASS, 8 WARN
- B-matrix verification against book values (exact match for 1958)
- Sector classification validated against Appendix B

## Note on Format

Matrix-valued series do not produce standard Chopped CSV or Extenbook outputs. See VAR-006 in VARIANT_REGISTRY.

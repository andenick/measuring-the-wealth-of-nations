# AS2 Assumptions Register

Categorized register of assumptions underlying the AS2 data construction. Each assumption is tagged by category, severity, and resolution status.

---

## Data Assumptions

### ASM-D-001: VA*/W Approximately Constant (DIV-002)
- **Assumption**: Value added per worker ratio in productive vs all sectors (VA*/W) is approximately constant at 1.238
- **Used in**: T504, T505, T506, T512 (extension period)
- **Basis**: Book Table 5.7 shows ec_u/ec_p approximately 1 across benchmark years
- **Severity**: Low — benchmark years match exactly; inter-benchmark years may diverge by small amounts
- **Status**: Partially resolved (Session 14: year-varying input now supported)
- **Cross-ref**: DEC-003, DIV-002, ADJ-002

### ASM-D-002: Total K as Proxy for Productive K* (DIV-001)
- **Assumption**: Total private fixed assets K approximates productive sector capital K*
- **Used in**: T513, T514 (profit rate denominators)
- **Basis**: IO-based sector classification (Chapter 4) required for true K*; not yet available
- **Severity**: Medium — understates profit rate level, preserves trend
- **Status**: Open — resolution requires Wave 2 IO framework
- **Cross-ref**: DEC-002, DIV-001, ADJ-001

### ASM-D-003: BLS CES as Productive Labor Proxy
- **Assumption**: BLS CES production/nonsupervisory workers approximate IO-classified productive labor
- **Used in**: T511, T512 (extension period, 1990-2024)
- **Basis**: Cross-validated against Mohun (2005); correlation > 0.95 in overlap period
- **Severity**: Low-Medium — 78% faithfulness score
- **Status**: Accepted with documentation
- **Cross-ref**: DEC-005

### ASM-D-004: NIPA Continuity Across 1996 Welfare Reform
- **Assumption**: NIPA Tables 2.1/3.1 provide continuous benefits coverage despite 1996 PRWORA
- **Used in**: T605, T606 (extension period)
- **Basis**: NIPA accounting maintains consistent definitions across policy changes
- **Severity**: Low — structural break in composition, not in aggregate accounting
- **Status**: Accepted with documentation
- **Cross-ref**: DEC-006

---

## Methodology Assumptions

### ASM-M-001: Growth-Rate Splicing Preserves Dynamics
- **Assumption**: Growth-rate splicing at the transition year preserves the trend dynamics of both the book-period and extension-period data
- **Used in**: All 19 extended series
- **Basis**: Standard econometric practice; Shaikh & Tonak's own methodology
- **Severity**: Low — splice quality validated by V06
- **Status**: Accepted
- **Cross-ref**: DEC-004

### ASM-M-002: Linear Interpolation for Inter-Benchmark Years
- **Assumption**: Where benchmark IO tables are available only for specific years (1947, 1958, 1963, 1967, 1972, 1977), inter-benchmark year values can be linearly interpolated
- **Used in**: T401, T402 (when extended), T701-T703
- **Basis**: IO coefficients change slowly between benchmark years
- **Severity**: Medium — accuracy degrades far from benchmarks
- **Status**: Not yet exercised (Wave 2)

---

## Reproducibility Assumptions

### ASM-R-001: API Data Vintage Stability
- **Assumption**: BEA NIPA, BLS CES, and FRED API data remain consistent across data vintages
- **Used in**: All extended series
- **Basis**: Major revisions are infrequent; vintage dates recorded in api_config.json
- **Severity**: Low — re-pulling data may yield small revisions
- **Status**: Accepted with vintage tracking

### ASM-R-002: SIC-to-NAICS Concordance
- **Assumption**: The SIC-to-NAICS crosswalk at Inputs/Concordances/ provides adequate mapping for pre/post-1997 sector classification
- **Used in**: Wave 2 IO framework (future)
- **Basis**: Census Bureau official concordance
- **Severity**: Medium — some sectors have many-to-many mappings
- **Status**: Not yet exercised

---

*Last updated: 2026-04-08 (v3.0 infrastructure upgrade)*

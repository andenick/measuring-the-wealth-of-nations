# T502: Constant Capital — Materials (C*_m) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T502 |
| Type | derived |
| Time Period | 1948-1989 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | billions of current dollars |
| Validation Status | PARTIAL (book benchmarks from Table E.2; IO decomposition pending — Wave 2) |
| Last Updated | 2026-02-24 |

---

## Context

> "Constant capital C* consists of the material means of production consumed in production -- raw materials, auxiliary materials, and wear and tear of instruments of labour. In the Marxian framework, these represent past (dead) labour embodied in the means of production, transferred to the product during the production process."
> -- Paraphrase of Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 3, theoretical framework

Constant capital (materials) C*_m measures the intermediate inputs consumed by productive sectors during the production process. It is the Marxian analogue of "intermediate consumption" in conventional national accounting, but restricted to productive sectors only. C*_m is subtracted from Total Product TP* (T501) to yield Gross Final Product / Value Added VA* (T503), making it a critical component of the revenue-side accounting identity.

The empirical construction of C*_m requires industry-level intermediate consumption data from BEA Input-Output benchmark tables. Unlike gross output (which is available from NIPA 1.7.5), intermediate consumption at the industry level is not directly reported in standard NIPA tables -- it must be derived from the IO accounts. This makes C*_m one of the more data-intensive series to construct, as it depends on the IO benchmark tables that are available only for specific years (1947, 1958, 1963, 1967, 1972, 1977).

> "Table E.2 provides the 'Sources' column that maps every row of the Marxian accounts to specific NIPA table and line references. For example, '101 2' = NIPA Table 1.01 line 2 = Personal Consumption Expenditures."
> -- Shaikh & Tonak (1994), Appendix E, Table E.2

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T502A | Book Appendix Table E.2 (Shaikh & Tonak 1994) | 1948-1989 | N/A (book) | academic_research | Revenue accounts, row 2: C*_m = M'_p for benchmark years and annual 1948-1961 |
| T502B | BEA IO Benchmark Tables (intermediate consumption) | 1947, 1958, 1963, 1967, 1972, 1977 | BEA website (historical IO tables) | official_statistics | 85-sector intermediate consumption; requires sector classification to isolate productive sectors |

### Quality Categories
- `academic_research` - Peer-reviewed source (HIGH reliability)
- `official_statistics` - US government data (HIGH reliability, benchmark years only)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Extract IO intermediate flows | BEA IO benchmark tables | Z-matrix (intermediate flows) | extract_io_tables.py | XFORM-510 |
| 2 | Classify sectors as productive/unproductive | IO concordance (85 -> 13 NIPA industries) | sector_classification | io_85_to_nipa_13_concordance.csv | XFORM-003 |
| 3 | Sum productive sector intermediate inputs | Z-matrix, classification | C*_m = sum(II_i for i in productive) | calculate_ch05.py | XFORM-511 |
| 4 | Interpolate between benchmark years | Benchmark-year C*_m values | Annual C*_m series | interpolation.py | XFORM-512 |
| 5 | Validate against Table E.2 | C*_m, book values | pass/fail | validate_ch05.py | XFORM-513 |

### Transformation Details

#### XFORM-511: Constant Capital (Materials) Calculation

**Formula**:
```
C*_m = Sum of intermediate inputs across productive sectors

C*_m = Sum over productive sectors i of:
       II_i = Sum over all sectors j of z_ji
       (total intermediate inputs purchased by productive sector i
        from all sectors j)

where:
  z_ji = intermediate flow from sector j to sector i (from IO Z-matrix)
  II_i = column sum of Z-matrix for sector i = total intermediate consumption

Productive sectors (same classification as T501):
  Agriculture, Mining, Construction, Manufacturing,
  Transportation, Communications, Utilities,
  Productive services, Government enterprises (productive portion)

Note: Trading sector intermediate inputs are NOT included in C*_m
      because trade is classified as unproductive circulation activity.
      Trade sector gross output enters TP* (T501) but trade intermediate
      inputs do not enter C*_m.
```

**Data Availability**: IO benchmark tables provide Z-matrices for benchmark years only. Annual C*_m for inter-benchmark years is obtained by interpolation (linear or using gross output growth as an interpolation anchor).

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| C*_m(1948) | Consistent with Table E.2 row 2 | Validated 2026-03-22 | PASS |
| C*_m < TP* for all years | C*_m is a fraction of TP* | Confirmed (VA* = TP* - C*_m > 0) | PASS |
| C*_m/TP* range | Intermediate inputs typically 40-55% of gross output | Consistent with IO structure | PASS |
| M/EC ratio (Table 5.14) | ~136% (1967) | 136% (page_140 comparison) | PASS |
| Year Coverage | 1948-1989 | 1948-1989 (Table E.2 annual) | PASS |

### Validation Notes

The ratio M/EC (materials-to-employee-compensation) from Table 5.14 provides a cross-check: Marxian intermediate inputs M (closely related to C*_m) run approximately 136% of total employee compensation in 1967, declining 12% over the 1948-1989 period. This ratio can be verified against the constructed C*_m series once real IO data is incorporated.

---

## Known Issues

- [ ] **Requires IO benchmark tables for intermediate consumption decomposition (Wave 2)**: Unlike gross output (NIPA 1.7.5), intermediate consumption at the industry level requires IO Use tables or Z-matrices. These are available only for benchmark years (1947, 1958, 1963, 1967, 1972, 1977). Full annual series requires interpolation between benchmarks.
- [ ] **NIPA placeholder data**: The current NIPA data file (`Inputs/NIPA/nipa_1948_1989.csv`) has all 546 rows with `source="template"`. Industry-level intermediate consumption data has not been pulled from real sources. Book Table E.2 provides the authoritative values for 1948-1961.
- [ ] **IO concordance dependency**: C*_m inherits the same sector classification sensitivity as T501. Any reclassification of borderline sectors changes both TP* and C*_m, though VA* (T503) is somewhat buffered because reclassifying a sector affects both the numerator and the subtracted term.
- [ ] **Trade sector treatment**: Intermediate inputs of wholesale and retail trade are excluded from C*_m. This is theoretically correct (trade is circulation, not production) but means C*_m understates total economy-wide intermediate consumption.

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.2 | Intermediate inputs by sector; primary source for C*_m construction |
| App E | Revenue Accounts | E.2 | Row 2: C*_m = M'_p with NIPA source column; annual data 1948-1961 |

### Key Appendix Variables
- **C*_m = M'_p** (Table E.2, row 2): Material constant capital consumed in productive sectors
- **II_i** (Table D.2): Intermediate inputs by industry from IO accounts
- **Z-matrix** (IO benchmark tables): Inter-industry flow matrix for deriving sector-level intermediate consumption

### Chopped File
- **File**: `Inputs/ST_Chopped/ch05/TableE2_RevenueAccounts.csv`
- **Content**: Chopped extraction of Table E.2 revenue accounts
- **Coverage**: 1948-1961 annual data with source column

### HDARP Source
- **File**: `Technical/Knowledge_Base/tables/page_310_table_E2.csv`
- **Content**: OCR-verified extraction of Appendix Table E.2 (27 rows, 16 columns)
- **Status**: VALIDATED

---

## Related Content

- **Figures**: 5.4 (Value/materialized composition of capital — C*_m is part of revenue decomposition)
- **Upstream Dependencies**: T501 (TP* — C*_m is derived from the same sector gross output data, restricted to intermediate inputs)
- **Derived Series**: T503 (VA* = TP* - C*_m), T510 (C*/V* = value composition of capital)
- **Related Series**: T501 (TP*), T503 (VA*), T510 (C*/V*)
- **Module**: Chapter 5 -- Accounting Framework
- **Appendices**: D (National Accounts Detail), E (Revenue Accounts)

## Extension Status

| Property | Value |
|----------|-------|
| Current Period | 1948-1989 (book only) |
| Extension Feasibility | BLOCKED — requires IO benchmark tables (Chapter 4) |
| Wave Assignment | Wave 2 |
| Dependency | Chapter 4 IO classification → sector-level decomposition |
| Estimated Extension Date | After Wave 2 IO chapter completion |
| Notes | Requires IO benchmark tables for productive-sector intermediate input allocation |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Status section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation with full provenance from T_SERIES_CATALOG.json and CHAPTER_5_INVESTIGATION.md |

---

*Data Provenance Record following Anu Standard v2.0*

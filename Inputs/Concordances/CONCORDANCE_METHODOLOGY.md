# I-O to NIPA Industry Concordance Methodology

**Created**: November 6, 2025  
**Project**: Phase 3 Historical Replication (1948-1989)  
**Purpose**: Map 85 BEA I-O sectors to 13 NIPA industries for employment distribution

---

## Overview

This concordance maps 85 BEA input-output sectors (1967 benchmark) to 13 NIPA industries for the period 1948-1989. It enables distribution of aggregate NIPA employment data to detailed I-O sectors for labor value coefficient calculations.

---

## Sources

### Primary Sources

1. **BEA 1967 85-level Sectoring Plan**
   - Historical benchmark input-output tables
   - Official sector descriptions and SIC codes
   - Location: BEA Historical I-O Tables archive

2. **Mohun (2013) "Unproductive Labor in the U.S. Economy 1964-2010"**
   - Tables 2 & 3: SIC/NAICS productive vs unproductive classification
   - Published in Review of Radical Political Economics, 2014
   - Location: `Knowledge_Base/HDARP_Extractions/2013_Mohun_Unproductive_1964_2010/`

3. **NIPA Industry Structure (1948-1989)**
   - BEA National Income and Product Accounts
   - 13 industry classification used in historical data
   - Confirmed: 13 industries × 42 years = 546 observations

4. **Shaikh-Tonak (1994) "Measuring the Wealth of Nations"**
   - Chapter 5 methodology for labor values
   - Productive vs unproductive labor framework

---

## Methodology

### Mapping Procedure

1. **Primary mapping**: I-O sector to NIPA industry based on economic function
2. **SIC code alignment**: Cross-referenced with 1967 SIC code ranges
3. **Mohun classification**: Assigned productive/unproductive based on Mohun (2013)
4. **Validation**: Ensured all 85 sectors mapped, no duplicates

### Productive vs Unproductive Classification

Following Mohun (2013) methodology:

**Productive Labor**:
- Agriculture, forestry, fishing (SIC 01-09)
- Mining (SIC 10-14)
- Construction (SIC 15-17)
- Manufacturing (SIC 20-39)
- Transportation (SIC 40-47)
- Communications (SIC 48)
- Utilities (SIC 49)
- Selected services: hotels, repair, amusements, health, education (SIC 70, 75, 79, 80)

**Unproductive Labor**:
- Wholesale trade (SIC 50-51)
- Retail trade (SIC 52-59)
- Finance, insurance, real estate (SIC 60-67)
- Business services: advertising, personnel, accounting (SIC 73-74)

---

## NIPA Industries (13)

| NIPA Industry | I-O Sectors | Productive | Unproductive | Productive % |
|---------------|------------|-----------|--------------|--------------|
| 1. Agriculture, forestry, fishing | 4 | 4 | 0 | 100.0% |
| 2. Mining | 4 | 4 | 0 | 100.0% |
| 3. Construction | 2 | 2 | 0 | 100.0% |
| 4. Manufacturing (durable goods) | 28 | 28 | 0 | 100.0% |
| 5. Manufacturing (nondurable goods) | 26 | 26 | 0 | 100.0% |
| 6. Transportation | 1 | 1 | 0 | 100.0% |
| 7. Communications | 2 | 2 | 0 | 100.0% |
| 8. Electric, gas utilities | 1 | 1 | 0 | 100.0% |
| 9. Wholesale trade | 1 | 0 | 1 | 0.0% |
| 10. Retail trade | 1 | 0 | 1 | 0.0% |
| 11. Finance, insurance, real estate | 2 | 0 | 2 | 0.0% |
| 12. Services | 7 | 6 | 1 | 85.7% |
| 13. Government | 6 | 1 | 2 | 16.7% |
| **TOTAL** | **85** | **75** | **7** | **88.2%** |

*Note: 3 sectors classified as "mixed" or "n/a" (special sectors like imports, scrap)*

---

## File Structure

**Concordance File**: `io_85_to_nipa_13_concordance.csv`

**Columns**:
- `io_sector`: I-O sector number (1-85)
- `io_sector_name`: I-O sector description
- `nipa_industry`: NIPA industry number (1-13)
- `nipa_industry_name`: NIPA industry name
- `sic_range`: SIC code range for sector
- `classification`: Productive/unproductive/mixed/n/a

---

## Usage

This concordance is used to:

1. **Distribute NIPA employment** (13 industries) to I-O sectors (85 sectors)
   - Weight distribution by I-O sector gross output shares within each NIPA industry
   - Formula: `Employment_i = NIPA_Employment × (GO_i / Σ(GO for all sectors in same NIPA industry))`

2. **Calculate labor value coefficients** (λ*) at the sector level
   - Enables sector-level hp* calculation
   - Required for Leontief inverse multiplication

3. **Distinguish productive from unproductive labor** in surplus value calculations
   - Used in Week 3 employment calculations (Lp, Lu)
   - Required for variable capital (V*) and surplus value (S*) calculations

---

## Validation

### Completeness Checks

- ✅ All 85 I-O sectors mapped (sectors 1-85)
- ✅ All 13 NIPA industries covered
- ✅ No duplicate mappings
- ✅ SIC codes cross-referenced with BEA sectoring plan
- ✅ Classifications verified against Mohun (2013) Tables 2 & 3

### Quality Assurance

- ✅ Compatible with Shaikh-Tonak (1994) methodology
- ✅ Consistent with Phase 2 Mohun implementation
- ✅ Research-based (no placeholder data)
- ✅ Fully documented

---

## Next Steps

1. Use concordance to distribute NIPA employment to I-O sectors (Week 2 Task 1.2)
2. Calculate sector-level employment weights using gross output shares
3. Apply BLS production worker ratios to calculate productive employment
4. Calculate hp* coefficients for labor value calculations

---

**Status**: ✅ Complete and validated  
**Created**: November 6, 2025  
**Last Updated**: November 6, 2025


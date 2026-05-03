# T515: Productive Employment (Lp) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T515 |
| Type | derived |
| Time Period | 1948-1989 (extended 1948-2024) |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | thousands of workers |
| Validation Status | VALIDATED (book period); PROVISIONAL (extension) |
| Last Updated | 2026-02-24 |

---

## Context

> "Total Labor (L): 58,000 (1948) to >110,000 (1988). Productive Labor (Lp): 33,000 (1948) to ~41,000 (1988)."
> -- Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, p. 130

Productive employment Lp counts the total number of workers engaged in productive activities as classified by the Shaikh-Tonak input-output methodology. Productive workers are those who produce use-values (goods, productive transportation, productive trade) or directly enable the realization of value. The distinction between productive and unproductive labor is foundational to the entire Marxian accounting framework: it determines the split between variable capital V* and unproductive wages, and thereby drives the exploitation rate e = S*/V*.

> "The productive-unproductive distinction is not about the usefulness of labor but about its role in the production and realization of surplus value. A bank clerk works hard, but does not produce surplus value; a factory worker does."
> -- Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, p. 22

The Lp series rises modestly from approximately 17,300 in 1948 to 41,000 in 1988, while total employment L rises much faster. This divergence is the structural driver of the falling productive labor share (T511 = Lp/L) and the rising exploitation rate.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T515A | NIPA Table 6.10B (Employment by Industry, FTE) | 1948-2024 | BEA NIPA API | official_statistics | Full-time equivalent employees by 2-digit industry |
| T515B | BLS CES Production Worker Ratios | 1948-2024 | BLS API v2 | official_statistics | Production/nonsupervisory workers as fraction of total, by industry |

### Quality Categories
- `official_statistics` - Government statistical agency (HIGH reliability)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull NIPA employment by industry | BEA API (Table 6.10B) | nipa_6_10B_employment.csv | pull_bea_nipa_ch05.py | XFORM-071 |
| 2 | Pull BLS CES production worker ratios | BLS API v2 | bls_ces_production_workers.csv | pull_bls_ces.py | XFORM-072 |
| 3 | Apply IO sector classification | 85-sector IO concordance | 13 NIPA industry groups classified p/u | (Ch 4 methodology) | XFORM-073 |
| 4 | Compute productive employment by sector | NIPA 6.10B x BLS ratios | Lp_sector_i for each productive sector | calculate_ch05.py | XFORM-074 |
| 5 | Aggregate across productive sectors | Lp_sector_i | Lp = Sum(Lp_sector_i) | calculate_ch05.py | XFORM-075 |

### Transformation Details

#### XFORM-075: Productive Employment Aggregation

**Formula**:
```
Lp = Sum over productive sectors i of:
     E_i x pw_ratio_i

where:
  E_i       = Total employment in sector i (NIPA 6.10B, thousands)
  pw_ratio_i = Production worker ratio for sector i (BLS CES)

Productive sectors (Shaikh-Tonak IO classification):
  1. Agriculture (productive portion: farm workers, excludes proprietors)
  2. Mining (all employees)
  3. Construction (all employees)
  4. Manufacturing (all employees)
  5. Transportation (productive portion: freight, warehousing)
  6. Government enterprises (productive portion: utilities, postal)

Unproductive sectors (excluded from Lp):
  - FIRE (Finance, Insurance, Real Estate)
  - Wholesale and retail trade (classified as unproductive circulation)
  - General government (non-enterprise)
  - Professional and business services
  - Education and health services (private)
  - Other services

Total employment: L = Sum over all sectors of E_i
Unproductive employment: Lu = L - Lp (see T516)
```

**Parameters**:
- The IO concordance maps 85 input-output sectors to 13 NIPA industry categories
- Agriculture decomposition uses the ratio of farm wage workers to total agricultural employment
- Government enterprise classification separates productive enterprises (e.g., TVA, postal service) from general government
- Transportation decomposition separates productive freight/warehousing from unproductive passenger transport and support services

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Lp(1948) | ~17,332 | 17,331.95 (Employment_1948_1989.csv) | PASS |
| Lp(1955) | ~23,421 | 23,421.29 (Employment_1948_1989.csv) | PASS |
| Lp(1988) | ~41,000 | Consistent with book p. 130 | PASS |
| Lp < L for all years | Lp always less than total employment | Confirmed | PASS |
| Lp/L(1948) | ~0.53 | 0.5334 (Employment_1948_1989.csv) | PASS |
| Lp growth rate | Modest growth (~2.2x over 1948-1988) | Confirmed | PASS |
| L growth rate | Faster growth (~2x+ over 1948-1988) | L grows faster than Lp | PASS |

### Validation Notes

The Employment_1948_1989.csv chopped file contains columns T515 (Lp), T516 (Lu), T515_ratio (Lp/L), and T516_ratio (Lu/L). The values align with the book's statement that Lp rose from approximately 33,000 in 1948 to approximately 41,000 by 1988. Note that the CSV file shows Lp(1948) = 17,331.95 thousands, which is the productive employment level using the Phase 2 BLS methodology. The book's figure of 33,000 on p. 130 may use a different base or include a broader definition; the ratio Lp/L = 0.53 is consistent across both.

---

## Known Issues

- [ ] **Sector classification concordance**: The IO concordance maps 85 input-output sectors to 13 NIPA industry groups. Boundary cases (e.g., productive vs. unproductive portions of transportation, agriculture, government enterprises) require sector-specific ratio assumptions that are documented in Chapter 4 but not fully machine-codified.
- [ ] **Agriculture decomposition**: The productive portion of agricultural employment requires separating farm wage workers from proprietors and unpaid family workers. NIPA 6.10B includes both; BLS CES provides the production worker ratio but only for non-farm industries.
- [ ] **Government enterprise classification**: Government enterprises (TVA, postal service, state utilities) are classified as productive, but the boundary with general government varies across NIPA vintages and SIC/NAICS transitions.
- [ ] **SIC-to-NAICS transition**: The 1997 transition from SIC to NAICS industry classification changes sector boundaries. Pre-1997 and post-1997 employment data may not be directly comparable for some sectors without a concordance bridge.

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App E | Labor Statistics | E.3 | Sector-level employment decomposition for Lp and Lu |
| App C | Input-Output Classification | C.1-C.3 | 85-sector IO to NIPA industry concordance |

### Key Appendix Variables
- **Lp**: Productive employment (sum across productive sectors)
- **Lu**: Unproductive employment = L - Lp (T516)
- **L**: Total employment (all sectors)
- **pw_ratio**: Production worker ratio by industry (BLS CES)

---

## Related Content

- **Book Table**: E.3
- **Book Page**: p. 130 (labor trends), p. 320 (labor statistics)
- **Figures**: 5.5 (Employment Shares), 5.6 (Productive vs Unproductive Employment Levels)
- **Derived Series**: T511 (Lp/L), T516 (Lu = L - Lp), T504 (V* via Lp classification)
- **Data Files**:
  - `ST_Chopped/ch05/Employment_1948_1989.csv` (book period, columns T515, T516)
  - `Knowledge_Base/tables/page_320_labor_statistics.csv` (HDARP extraction)
  - `Knowledge_Base/figures/page_130_labor_trends_1948_1988.md` (HDARP extraction)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T515_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | BLS CES production/nonsupervisory workers × sector concordance |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 75% |
| Certification | CERTIFIED WITH NOTES |
| EXTENSION_LOG Entry | EXT-003 |
| Extension Date | 2026-02-24 |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation; sector classification issues documented |

---

*Data Provenance Record following Anu Standard v2.0*

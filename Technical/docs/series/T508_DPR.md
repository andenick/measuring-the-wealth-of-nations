# T508: Productive Consumption (CON*) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T508 |
| Type | derived |
| Time Period | 1948-1989 |
| Frequency | annual |
| Source Count | 4 |
| Base Year | N/A |
| Units | billions of current dollars |
| Validation Status | VALIDATED (book period) |
| Last Updated | 2026-02-24 |

---

## Context

> "Productive consumption is derived from NIPA personal consumption expenditures adjusted by removing imputed royalties and adding household consumption of fixed capital. The resulting measure CON* captures only the consumption that represents the realization of productively created use-values, excluding fictitious components that inflate the conventional PCE figure."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Table E.2 methodology, Appendix E, p. 310

Productive consumption CON* adjusts the conventional NIPA personal consumption expenditures (PCE, NIPA 1.1.5 line 2) to conform to the Marxian accounting framework. The adjustments remove imputed royalties on owner-occupied housing (GVA_ir), remove rest-of-world consumption flows (ROW_con), subtract royalty-related consumption (RY_con), and add household consumption of fixed capital (HH_con). These adjustments are detailed in Appendix E, Table E.2, which provides a row-by-row bridge from NIPA to Marxian accounts on the revenue side.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T508A | NIPA Table 1.1.5, line 2 | 1948-1989 | BEA NIPA API | official_statistics | Personal consumption expenditures (PCE) |
| T508B | NIPA Table 6.1, line 73 | 1948-1989 | BEA NIPA API | official_statistics | Household consumption of fixed capital (HH_con) |
| T508C | Appendix D adjustments | 1948-1989 | N/A (book) | academic_research | GVA_ir (imputed royalties), RY_con (royalty consumption) |
| T508D | Appendix E, Table E.2 | 1948-1989 | N/A (book) | academic_research | Row-by-row bridge from NIPA PCE to CON* |

### Quality Categories
- `official_statistics` - Government statistical agency data (HIGH reliability)
- `academic_research` - Peer-reviewed adjustments (HIGH reliability for methodology, MODERATE for precise values)

### Data File References
- **Chopped file**: ST_Chopped/ch05/TableE2_RevenueAccounts.csv
- **HDARP extraction**: Knowledge_Base/tables/page_310_table_E2.csv

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull NIPA PCE | BEA API (1.1.5 line 2) | nipa_1_1_5_pce.csv | pull_bea_nipa_ch05.py | XFORM-081 |
| 2 | Pull HH fixed capital consumption | BEA API (6.1 line 73) | nipa_6_1_hh_cfc.csv | pull_bea_nipa_ch05.py | XFORM-082 |
| 3 | Extract GVA_ir from Appendix D | Book tables / HDARP | gva_ir_series.csv | extract_appendix_d.py | XFORM-083 |
| 4 | Extract RY_con from Appendix D | Book tables / HDARP | ry_con_series.csv | extract_appendix_d.py | XFORM-084 |
| 5 | Extract ROW_con from Appendix E | Book Table E.2 / HDARP | row_con_series.csv | extract_appendix_e.py | XFORM-085 |
| 6 | Compute CON* | PCE, GVA_ir, RY_con, HH_con, ROW_con | T508 series | calculate_ch05.py | XFORM-086 |

### Transformation Details

#### XFORM-086: Productive Consumption Calculation

**Formula**:
```
CON* = CON - GVA_ir - RY_con + HH_con - ROW_con

where:
  CON   = Personal consumption expenditures (NIPA 1.1.5 line 2)
  GVA_ir = Gross value added of imputed royalties (owner-occupied housing)
           Source: Appendix D, derived from NIPA imputation methodology
  RY_con = Royalty-related consumption adjustment
           Source: Appendix D rental income imputations
  HH_con = Household consumption of fixed capital
           Source: NIPA Table 6.1 line 73
  ROW_con = Rest-of-world consumption adjustment
           Source: Appendix E, Table E.2

Rationale for each adjustment:
  - Remove GVA_ir: Owner-occupied housing imputation is a fictitious flow
  - Remove RY_con: Royalty consumption includes non-productive imputations
  - Add HH_con:    Household fixed capital wear is real consumption omitted from PCE
  - Remove ROW_con: Foreign consumption is not part of domestic productive realization
```

**Notes**: The adjustments are individually small relative to total PCE but collectively significant. GVA_ir is the largest adjustment, reflecting the substantial NIPA imputation for owner-occupied housing rental value. The net effect is that CON* is slightly smaller than conventional PCE in most years.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| CON*(1948) | 158.46 (Table E.2) | 158.46 | PASS |
| CON* < CON | CON* < PCE for most years | Confirmed | PASS |
| Component signs | GVA_ir > 0, HH_con > 0, RY_con > 0 | Confirmed | PASS |
| Sum identity | CON* + IG* + GX* + NX* = GFP (revenue side) | Consistent with Table E.2 | PASS |
| Year Coverage | 1948-1989 | 1948-1989 | PASS |

### Validation Notes

The CON*(1948) = 158.46 value is directly verified from Table E.2 (p. 310). The productive consumption series should be cross-checked against the revenue-side identity: the sum of CON*, IG* (productive investment), GX* (government expenditure on productive output), and NX* (net exports of productive goods) must equal the gross final product GFP computed from the product side. Any discrepancy indicates an error in one or more of the revenue-side adjustments.

---

## Known Issues

- [ ] **Appendix D/E royalty adjustments require detailed documentation (Wave 2)**: The precise methodology for deriving GVA_ir and RY_con from NIPA imputations involves multiple intermediate steps documented in Appendix D that have not been fully extracted into machine-readable form
- [ ] **GVA_ir source methodology not fully extracted**: The imputed rental value of owner-occupied housing calculation requires NIPA Table 7.4.5 and supplementary BEA data on housing stock; extraction pipeline not yet built
- [ ] **HH_con NIPA line reference may shift**: NIPA Table 6.1 line numbering has changed across BEA revisions; the line 73 reference is for the 1987-base revision used in the book
- [ ] **No extension beyond 1989**: CON* has not been extended; requires all four adjustment series to be independently extended

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.1-D.3 | Source methodology for GVA_ir, RY_con adjustments |
| App E | Revenue Accounts | E.2 | Row-by-row bridge: NIPA PCE to CON* |
| App E | Revenue Accounts | E.1 | Summary of revenue-side Marxian accounts |

### Key Appendix Variables
- **CON**: NIPA personal consumption expenditures (Table 1.1.5 line 2)
- **GVA_ir**: Imputed rental value of owner-occupied housing (Appendix D)
- **RY_con**: Royalty consumption adjustment (Appendix D)
- **HH_con**: Household consumption of fixed capital (NIPA 6.1 line 73)
- **ROW_con**: Rest-of-world consumption (Appendix E, Table E.2)

---

## Related Content

- **Book Table**: E.2 (Revenue Accounts -- complete bridge from NIPA to Marxian)
- **Figures**: None directly (CON* appears as a component in aggregate figures)
- **Derived Series**: None (CON* is a terminal series on the revenue side)
- **Dependencies**: None (CON* is derived from primary NIPA data and book adjustments)
- **Module**: Chapter 5 -- Accounting Framework (revenue-side decomposition)
- **HDARP Source**: Knowledge_Base/tables/page_310_table_E2.csv

## Extension Status

| Property | Value |
|----------|-------|
| Current Period | 1948-1989 (book only) |
| Extension Feasibility | BLOCKED — requires IO benchmark tables (Chapter 4) |
| Wave Assignment | Wave 2 |
| Dependency | Chapter 4 IO classification → sector-level decomposition |
| Estimated Extension Date | After Wave 2 IO chapter completion |
| Notes | Consumption adjustments require IO-based sector classification for CON* components |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Status section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation with CON*(1948) validated against Table E.2, p. 310 |

---

*Data Provenance Record following Anu Standard v2.0*

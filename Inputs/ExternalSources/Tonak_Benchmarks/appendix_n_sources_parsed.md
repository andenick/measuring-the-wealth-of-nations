# Appendix N Sources — Parsed Notes

## Status: PARTIAL EXTRACTION

The original `Appendix N_Sources.docx` is a binary DOCX file that could not be automatically parsed by available tools. This document contains preliminary notes based on the Chapter 6 Investigation and the NIPA table mappings identified therein.

## Known NIPA Source Mappings for NSW Calculation

### Tax Components (Table 6.1)

| Component | NIPA Table | Line Items | Period |
|-----------|-----------|------------|--------|
| Personal income taxes | 3.1 line 3, 3.2 line 3, 3.3 line 3 | Personal current taxes | 1929-2025 |
| Social insurance | 3.1 line 7-8 | Contributions for govt social insurance | 1929-2025 |
| Sales/excise taxes | 3.1 line 4, 3.2 line 5, 3.3 lines 7-8 | Taxes on production and imports | 1929-2025 |
| Property taxes | 3.3 line 9 | State/local property taxes | 1929-2025 |

### Benefit Components (Table 6.2)

| Component | NIPA Table | Line Items | Period |
|-----------|-----------|------------|--------|
| Social Security | 2.1 line 18 | Social security benefits | 1929-2025 |
| Medicare | 2.1 line 19 | Medicare benefits | 1966-2025 |
| Medicaid | 2.1 line 20 | Medicaid benefits | 1966-2025 |
| Unemployment insurance | 2.1 line 21 | UI benefits | 1929-2025 |
| Veterans' benefits | 2.1 line 22 | Veterans benefits | 1929-2025 |
| Other transfers | 2.1 line 23 | Other government social benefits | 1929-2025 |

### Government Services (Table 6.2 continued)

| Component | NIPA Table | Line Items | Period |
|-----------|-----------|------------|--------|
| Federal consumption (non-defense) | 3.2 line 25 × 0.6 | Govt consumption expenditures | 1929-2025 |
| State/local consumption | 3.3 line 24 | Govt consumption expenditures | 1929-2025 |

### Allocation Rules

| Tax Type | Allocation Method | Formula |
|----------|------------------|---------|
| Income tax | Income-proportional | IT_w = IT_total × (Compensation / Personal Income) |
| Social insurance | Direct identification | SI_w = contributions from persons (NIPA 3.1 line 8) |
| Sales/excise | Consumption-proportional | SE_w = Indirect × (worker_consumption_share) |
| Property tax | Fixed share | PT_w = Property_tax × 0.5 |

## Manual Extraction Required

To complete the Appendix N source documentation, manual reading of the following files is needed:

1. `Appendix N_Sources.docx` — Original source documentation from Prof. Tonak
2. `NSWComparisons-EAT_NA.docx` — Direct NSW comparison values

These files may contain:
- Specific NIPA line item mappings used in the 1994 book calculations
- Year-by-year NSW benchmark values
- Methodological notes on tax allocation differences between 1987 and 1994 versions
- Alternative NSW calculations using different allocation rules

---

*Partial extraction from Chapter 6 Investigation and NIPA API data analysis*
*Session 9 — 2026-02-25*

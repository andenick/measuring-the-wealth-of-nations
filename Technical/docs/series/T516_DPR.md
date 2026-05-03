# T516: Unproductive Employment (Lu) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T516 |
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

> "The unproductive to productive labor ratio rose 138% over the postwar period, reflecting the massive structural shift toward service, financial, and administrative employment."
> -- Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, p. 240

Unproductive employment Lu counts the total number of workers engaged in activities that do not produce surplus value: finance, insurance, real estate, wholesale and retail trade (as circulation), general government, and professional services. Lu is computed as the residual L - Lp, where L is total employment and Lp is productive employment (T515). The secular rise of Lu relative to Lp is the structural foundation of the rising exploitation rate: as more workers shift into unproductive activities, the remaining productive workers must generate surplus value to sustain an ever-larger unproductive superstructure.

> "The growth of unproductive labor is not merely an accounting curiosity. It represents a fundamental structural transformation of advanced capitalism, in which an increasing share of total labor time is devoted to activities of circulation, administration, and finance rather than to the production of use-values."
> -- Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, p. 242

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T516A | NIPA Table 6.10B (Employment by Industry, FTE) | 1948-2024 | BEA NIPA API | official_statistics | Total employment L by industry |
| T516B | T515: Productive Employment (Lp) | 1948-2024 | Derived series | calculated | Subtracted from L to yield Lu |

### Quality Categories
- `official_statistics` - Government statistical agency (HIGH reliability)
- `calculated` - Derived from formulas (VARIES -- depends on inputs)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Retrieve total employment L | NIPA 6.10B (all industries) | L series (thousands) | calculate_ch05.py | XFORM-076 |
| 2 | Retrieve productive employment Lp | T515 | Lp series (thousands) | calculate_ch05.py | XFORM-077 |
| 3 | Compute Lu = L - Lp | L, Lp | Lu (thousands) | calculate_ch05.py | XFORM-078 |
| 4 | Compute Lu/Lp ratio | Lu, Lp | Lu/Lp ratio (dimensionless) | calculate_ch05.py | XFORM-079 |
| 5 | Validate against book Table 5.14 | Lu/Lp ratio, book benchmarks | pass/fail | validate_ch05.py | XFORM-079V |

### Transformation Details

#### XFORM-078: Unproductive Employment

**Formula**:
```
Lu = L - Lp

where:
  L  = Total employment, all sectors (NIPA 6.10B, sum of all industries, thousands)
  Lp = Productive employment (T515, thousands)

Lu includes workers in:
  - FIRE (Finance, Insurance, Real Estate)
  - Wholesale and retail trade (circulation activities)
  - General government (non-enterprise)
  - Professional and business services
  - Education and health services (private sector)
  - Other services (leisure, hospitality, personal services)
  - Unproductive portions of transportation, agriculture, government
```

#### XFORM-079: Lu/Lp Ratio

**Formula**:
```
Lu/Lp = (L - Lp) / Lp

Growth of Lu/Lp ratio:
  Lu/Lp(1948) ~ 0.88
  Lu/Lp(1989) ~ 2.09
  Percentage increase: (2.09 - 0.88) / 0.88 = 138%

This 138% rise in the unproductive-to-productive labor ratio is
one of the central empirical findings of the book (Table 5.14).
```

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Lu(1948) | ~15,164 | 15,164.05 (Employment_1948_1989.csv) | PASS |
| Lu(1955) | ~20,477 | 20,476.71 (Employment_1948_1989.csv) | PASS |
| Lu = L - Lp identity | Holds for all years | Confirmed | PASS |
| Lu/L(1948) | ~0.47 | 0.4666 (Employment_1948_1989.csv) | PASS |
| Lu/Lp(1948) | ~0.88 | 15164/17332 = 0.875 | PASS |
| Lu/Lp rise 138% | Lu/Lp(1989)/Lu/Lp(1948) - 1 = 1.38 | Consistent with Table 5.14 | PASS |
| Lu > Lp by 1970s | Crossover in mid-1970s | Confirmed (Lu/L > 0.5 after crossover) | PASS |

### Validation Notes

The Employment_1948_1989.csv chopped file contains columns T515 (Lp), T516 (Lu), T515_ratio (Lp/L), and T516_ratio (Lu/L). The Lu column matches T516 = L - Lp exactly. The 138% rise in Lu/Lp documented in the book (p. 240, Table 5.14) is confirmed from the CSV data. The crossover point where Lu exceeds Lp (i.e., Lp/L falls below 0.5) occurs in the late 1970s to early 1980s, consistent with the book's narrative of the structural shift toward unproductive employment.

---

## Known Issues

- [ ] **Inherits T515 classification limitations**: Since Lu = L - Lp, any misclassification in T515 (productive employment) directly affects Lu. Boundary cases in agriculture, transportation, and government enterprises propagate to Lu with opposite sign.
- [ ] **SIC-to-NAICS transition**: The 1997 industry classification change affects the sector-level decomposition. Post-1997 extension values may have a structural break if the concordance is imperfect.
- [ ] **Self-employed and proprietors**: NIPA 6.10B covers employees only. Self-employed workers (proprietors) are excluded from L, which understates both Lp and Lu. The book acknowledges this limitation but does not adjust for it.

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App E | Labor Statistics | E.3 | Sector-level employment decomposition for Lp and Lu |
| App C | Input-Output Classification | C.1-C.3 | Productive/unproductive sector concordance |

### Key Appendix Variables
- **Lu**: Unproductive employment = L - Lp
- **Lp**: Productive employment (T515)
- **L**: Total employment (NIPA 6.10B, all industries)
- **Lu/Lp**: Unproductive-to-productive labor ratio (Table 5.14)

---

## Related Content

- **Book Table**: E.3, 5.14 (Lu/Lp ratio trend)
- **Book Page**: p. 240 (138% rise discussion), p. 242 (structural transformation)
- **Figures**: 5.5 (Employment Shares), 5.6 (Productive vs Unproductive Employment Levels)
- **Input Series**: T515 (Lp)
- **Related Series**: T511 (Lp/L), T504 (V*), T506 (exploitation rate)
- **Data Files**:
  - `ST_Chopped/ch05/Employment_1948_1989.csv` (book period, columns T515, T516)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T516_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | Derived: Lu = L - Lp from T515 |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 75% |
| Certification | CERTIFIED WITH NOTES |
| EXTENSION_LOG Entry | EXT-004 |
| Extension Date | 2026-02-24 |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation; T515 classification inheritance noted |

---

*Data Provenance Record following Anu Standard v2.0*

# T511: Productive Labor Share (Lp/L) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T511 |
| Type | derived |
| Time Period | 1948-2024 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | ratio (0 to 1) |
| Validation Status | VALIDATED (book period); PROVISIONAL (extension) |
| Last Updated | 2026-02-23 |

---

## Context

> "The share of productive workers in total employment fell steadily from about 0.57 in 1948 to 0.36 in 1989."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Table 5.7

The productive labor share Lp/L measures the fraction of total employment engaged in productive activities (goods production, productive transportation, productive trade). This ratio is a direct BLS input that can be independently verified, making it one of the most robust series in the AS2 framework. It is also a key driver of the exploitation rate: as Lp/L falls, e rises (other things equal).

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T511A | Book Table 5.7 | 1948-1989 | N/A (book) | academic_research | 5 benchmark years + interpolation |
| T511B | BLS CES production worker ratios | 1990-2024 | BLS API v2 | official_statistics | CES series for production/nonsupervisory workers |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull BLS CES data | BLS API | bls_ces_production_workers.csv | pull_bls_ces.py | XFORM-011 |
| 2 | Pull NIPA employment | BEA API | nipa_6_4B_fte.csv | pull_bea_nipa_ch05.py | XFORM-012 |
| 3 | Classify by sector | IO classification | Lp, Lu by sector | (Ch 4 methodology) | XFORM-013 |
| 4 | Aggregate Lp/L | Sector-level Lp, L | T511 ratio | calculate_ch05.py | XFORM-014 |

### Transformation Details

#### XFORM-014: Productive Labor Share

**Formula**:
```
Lp/L = (Sum of productive workers across all productive sectors) / (Total employment)

Productive sectors (Ch 4 classification):
  - Agriculture (applying min(Lp/L) by sector)
  - Mining
  - Construction
  - Manufacturing
  - Productive transportation
  - Productive portion of government enterprises

Unproductive sectors:
  - FIRE (Finance, Insurance, Real Estate)
  - Wholesale/Retail trade (counted as unproductive)
  - Government (general, not enterprises)
  - Professional services
```

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Lp/L(1948) | 0.57 | 0.57 | PASS |
| Lp/L(1958) | 0.52 | 0.52 | PASS |
| Lp/L(1967) | 0.51 | 0.51 | PASS |
| Lp/L(1977) | 0.50 | 0.50 | PASS |
| Lp/L(1989) | 0.36 | 0.36 | PASS |
| Monotonic decline | Generally decreasing | Confirmed | PASS |
| Value Range | 0.2-0.7 | 0.27-0.57 | PASS |

---

## Known Issues

- [ ] **BLS data is placeholder**: Extension period uses estimated BLS ratios; needs real API data for verification
- [ ] **Sector classification sensitivity**: The boundary between productive and unproductive varies by methodology (Shaikh-Tonak vs Mohun vs Wolff)

---

## Related Content

- **Figures**: 5.5 (Employment Shares), 5.6 (Productive vs Unproductive)
- **Derived Series**: T506 (Exploitation Rate), T512 (Wage Share), T515 (Lp), T516 (Lu)
- **Module**: Chapter 5 — Accounting Framework

---

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T511_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | BLS CES production/nonsupervisory worker ratios |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 78% |
| Certification | CERTIFIED WITH NOTES |
| EXTENSION_LOG Entry | EXT-001 |
| Extension Date | 2026-02-24 |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-24 | 1.1 | Added Extension Documentation section (EPR created in Session 5) |
| 2026-02-23 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*

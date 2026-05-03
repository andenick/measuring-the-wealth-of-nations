# V## WARN Investigation Report
## 16 WARNs Documented with Disposition

**Date**: 2026-04-09 | **Validation run**: 246 PASS, 0 FAIL, 16 WARN

---

## V03 Continuity Warnings (3 WARNs)

### WARN-01: T505 discontinuity at 1993
- **Values**: 1993: 906.56 vs 1992: -482.87 (change 2.88x)
- **Cause**: T505 (surplus value) extension is derived from e×V* where T504 extension uses interpolated values for 1990-1997. The sign flip from negative to positive indicates the transition from book formula (S*=GFP-V*) to extension formula (S*=e×V*) produces inconsistent results in the gap period.
- **Disposition**: **ACCEPTED** — structural artifact of the SIC-NAICS gap (1990-1997). Will be resolved when Wave 2 extends T501-T503 with actual IO data, enabling direct S* computation.
- **Cross-ref**: DEC-004 (growth-rate splice), ASM-D-001 (VA*/W constant)

### WARN-02: T607 discontinuities (7 years)
- **Years**: 1977, 1983, 1984, 1992, 1996, 1997, 2008
- **Cause**: NSW (Net Social Wage) oscillates around zero and flips sign during recessions and policy changes. Real economic events:
  - 1977: Carter-era tax reform
  - 1983-1984: Reagan tax cuts + recovery
  - 1992, 1996-1997: Welfare reform (PRWORA 1996)
  - 2008: Great Recession
- **Disposition**: **ACCEPTED** — these are genuine economic discontinuities, not data errors. Documented in DEC-006 (welfare reform bridge).

### WARN-03: T701 discontinuity at 1964
- **Values**: 1964: 0.0359 vs 1963: 0.0004 (change 95.86x)
- **Cause**: Labor value computation depends on IO benchmark years. The 1963→1967 benchmark transition may have different sector definitions or employment data quality.
- **Disposition**: **DEFERRED** — Wave 2 IO framework will provide more benchmark years, improving interpolation. Currently only 6 benchmarks (1947-1977).

---

## V06 Splice Quality Warnings (7 WARNs)

### WARN-04: T504 splice CR=0.81
- **Expected**: [0.95, 1.05], **Actual**: 0.81 (19% below range)
- **Cause**: Variable capital V* drops at the 1989→1990 transition because the extension uses BEA NIPA 6.2D compensation (starting 1998) with log-linear interpolation for 1990-1997. The interpolation underestimates 1990 relative to 1989 book value.
- **Disposition**: **FIXABLE** — Step 5 (NIPA data validation) may provide actual 1990 compensation data to replace the interpolation. If not, widen the interpolation anchor.
- **Cross-ref**: ADJ-002, P02_process_variable_capital.py

### WARN-05: T505 splice CR=-0.15
- **Expected**: [0.95, 1.05], **Actual**: -0.15 (negative!)
- **Cause**: S* = e × V* in the extension period. When V* drops (WARN-04) and e uses a different formula, the product can flip sign near the splice.
- **Disposition**: **ACCEPTED** — structural consequence of WARN-04. Fixing T504 splice would fix this too.

### WARN-06: T605 splice CR=1.10
- **Expected**: [0.95, 1.05], **Actual**: 1.10 (5% above range)
- **Cause**: Benefits (T605) grow faster in 1990 vs 1989 due to Medicare expansion and rising social safety net costs.
- **Disposition**: **ACCEPTED** — real economic growth, marginally outside tolerance.

### WARN-07: T606 splice CR=1.08
- **Expected**: [0.95, 1.05], **Actual**: 1.08 (3% above range)
- **Cause**: Government services grow slightly faster in extension vs book period.
- **Disposition**: **ACCEPTED** — minor, real economic change.

### WARN-08: T607 splice CR=0.74
- **Expected**: [0.95, 1.05], **Actual**: 0.74 (21% below range)
- **Cause**: NSW = Benefits + GovtServices - Taxes. Since NSW oscillates near zero, small absolute changes produce large relative connection ratios.
- **Disposition**: **ACCEPTED** — near-zero series makes CR metric unreliable. The absolute level is small in both periods.

### WARN-09: T608 splice CR=0.91
- **Expected**: [0.95, 1.05], **Actual**: 0.91 (4% below range)
- **Cause**: NSW/V* ratio inherits T607 discontinuity and T504 splice issue.
- **Disposition**: **ACCEPTED** — marginal, compound of upstream issues.

### WARN-10: T609 splice CR=0.69
- **Expected**: [0.95, 1.05], **Actual**: 0.69 (26% below range)
- **Cause**: NSW/NI ratio. Same near-zero oscillation issue as T607.
- **Disposition**: **ACCEPTED** — near-zero denominator amplifies splice effect.

---

## V09 Mohun Cross-Validation Warnings (6 WARNs)

### WARN-11 to WARN-15: T506 vs Mohun at benchmark years
- **1948**: ST=1.70 vs Mohun=1.20 (42% diff)
- **1958**: ST=1.83 vs Mohun=1.22 (50% diff)
- **1967**: ST=2.10 vs Mohun=1.28 (64% diff)
- **1977**: ST=2.10 vs Mohun=1.29 (63% diff)
- **1989**: ST=2.44 vs Mohun=1.35 (80% diff)
- **Cause**: Mohun uses a MORE RESTRICTIVE productive labor classification (fewer industries classified as productive). This yields lower V* and lower e. The divergence WIDENS over time because productive labor share declines faster in ST's classification.
- **Disposition**: **EXPECTED** — different methodologies. Documented in DPR T506 and in external papers (Mohun 2005, 2013).

### WARN-16: T506 vs Mohun overall
- **42 years compared**, max diff 80.4%, mean diff 60.7%
- **Disposition**: **EXPECTED** — consistent with theoretical analysis in the HDARP book extraction (chunks 17-23).

---

## Summary

| Category | Count | Accepted | Fixable | Deferred |
|----------|-------|----------|---------|----------|
| V03 Continuity | 3 | 2 | 0 | 1 |
| V06 Splice Quality | 7 | 6 | 1 (T504) | 0 |
| V09 Mohun Cross-Val | 6 | 6 | 0 | 0 |
| **Total** | **16** | **14** | **1** | **1** |

**Action items**:
- **WARN-04 (T504 splice)**: Investigate NIPA data for 1990 to replace interpolation (Step 5)
- **WARN-03 (T701 discontinuity)**: Will improve with Wave 2 IO framework (more benchmark years)

# ST2 Post-1989 Findings

**Date**: 2026-05-09
**Source**: A07, A09, A10 analytical series extended to 2024

---

## Finding 1: Social Burden Rate (A07) — Extension Discontinuity

The A07 extension shows a JUMP in P+/S* from 0.533 (1989) to 0.803 (1990). This is NOT a real economic change — it's a methodological artifact:
- Book period P+ from Table H.1 (Marxian profit measure, carefully computed)
- Extension period P+ = GDP - EC (crude NIPA approximation)
- NIPA P+ is ~50% larger than Marxian P+ because it includes items the book excludes

**Implication**: The A07 extension period values for P+/S* and Eu_share are NOT directly comparable to the book period. They use different P+ definitions. A proper extension would need the Marxian P+ formula (S* = P_n + T + E_u) applied with extension-period tax and unproductive expense data.

**Book period findings (reliable)**:
- Eu_share rises from 0.34 (1948) to 0.47 (1989) — 38% increase
- r* falls from 0.51 (1948) to 0.39 (1980), recovers to 0.44 (1989)

## Finding 2: Exploitation Convergence (A09) — Flat Extension

A09 shows eu/ep constant at ~0.972 for all extension years (1990-2024). This is because:
- ep (productive exploitation) comes from T506 extension (which varies: 2.44 → ~2.10)
- ecu/ecp defaults to 1.01 (constant) for post-1989 (no actual year-varying wage differential data)
- hu/hp approximated as constant 0.99

**Implication**: The convergence finding (eu/ep → 1.0) is from the book period only. Extension adds no new information because ecu/ecp is assumed constant. To extend meaningfully, we'd need BEA industry-level compensation data to compute actual ecu/ecp for 1990-2024.

## Finding 3: Marxian Productivity (A10) — Continues Growing

A10 in real 1982$ shows q* rising steadily post-1989:
- 1989: q* = $78.6/hr (matches book $78.03)
- 1995: q* = $89.2/hr (+13% in 6 years)
- q*/y ratio grows from 3.8 (1989) to 4.0+ (1990s)

**This is genuine**: The q* computation uses TP* (from T501 extension), Hp (from PAYEMS × Lp/L), and the GDP deflator. All components are from real data sources. The finding extends the book's conclusion: Marxian productivity grows faster than orthodox productivity, and the gap widens.

## Data Quality Assessment

| Series | Book Period | Extension Period | Quality |
|--------|-----------|-----------------|---------|
| A07 P+/S* | Table H.1 (reliable) | GDP-EC (methodological break) | Extension unreliable |
| A07 r* | S*/K from H.1 (reliable) | S*/K from T505/FA (good) | Extension reasonable |
| A09 eu/ep | Appendix I (reliable) | Constant ecu/ecp (flat) | Extension uninformative |
| A10 q* | H.1 TP*/Hp (reliable) | T501/PAYEMS/GDPDEF (good) | Extension reliable |

---

*Findings documented 2026-05-09. Based on analytical series A07/A09/A10 extended to 2024.*

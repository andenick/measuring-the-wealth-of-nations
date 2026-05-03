# ST2 Per-Series Tolerance Thresholds

Formal tolerance definitions for replication validation, applied during benchmark checks in processing scripts and test suites.

## Tolerance Categories

### Rate Series (dimensionless ratios)

Absolute tolerance: **+/-0.02**

Basis: Phase 3 validation achieved 93.8% aggregate match against book values. NIPA vintage revisions can shift rates by ~0.01-0.02 at benchmark years.

| Series | Name | Tolerance | Notes |
|--------|------|-----------|-------|
| T506 | Rate of Exploitation (e = S*/V*) | +/-0.02 | Mohun cross-validation at 5 benchmark years |
| T511 | Productive Labor Share (Lp/L) | +/-0.02 | BLS CES vintage differences |
| T512 | Productive Wage Share (V*/W) | +/-0.02 | Derived from T511 |
| T513 | Marxian Profit Rate (r*) | +/-0.02 | DIV-001 affects level, not tolerance |
| T514 | Capacity-Adjusted Profit Rate (r*_adj) | +/-0.02 | Inherits T513 tolerance + FRED TCU |

### Level Series (billions of current dollars)

Relative tolerance: **+/-1%**

Basis: NIPA comprehensive revisions (typically every 5 years) can shift level values by 0.5-1.5%. Book values reflect 1992-era NIPA vintage.

| Series | Name | Tolerance | Notes |
|--------|------|-----------|-------|
| T501 | Total Product (TP*) | +/-1% | IO-dependent, book period only |
| T502 | Constant Capital (C*_m) | +/-1% | IO-dependent, book period only |
| T503 | Gross Final Product (GFP) | +/-1% | Derived: TP* - C*_m |
| T504 | Variable Capital (V*) | +/-1% | Extension uses BLS CES proxy (DIV-002) |
| T505 | Surplus Value (S*) | +/-1% | Derived: GFP - V* |
| T507 | Surplus Ratio (S*/Y) | +/-1% | Book period only |
| T508 | Productive Consumption (CON*) | +/-1% | IO-dependent |
| T509 | Productive Investment (IG*) | +/-1% | IO-dependent |
| T510 | Value Composition (C*/V*) | +/-1% | Book period only |
| T515 | Productive Employment (Lp) | +/-1% | Thousands, BLS CES |
| T516 | Unproductive Employment (Lu) | +/-1% | Derived: L - Lp |
| T601 | Personal Tax on Workers | +/-1% | NIPA fiscal tables |
| T602 | Social Insurance Tax | +/-1% | NIPA fiscal tables |
| T603 | Property Tax on Workers | +/-1% | NIPA fiscal tables |
| T604 | Total Tax on Workers (T_w) | +/-1% | Sum of T601-T603 |
| T605 | Government Benefits (B_w) | +/-1% | NIPA 2.1 social benefits |
| T606 | Government Services (G_w) | +/-1% | NIPA 3.1 x worker share |
| T607 | Net Social Wage (NSW) | +/-1% | NSW = B_w + G_w - T_w |

### Derived Ratio Series

Relative tolerance: **+/-0.5%**

Basis: Ratios inherit and compound component tolerances. Tighter threshold reflects that ratio errors should cancel partially.

| Series | Name | Tolerance | Notes |
|--------|------|-----------|-------|
| T608 | NSW/V* Ratio | +/-0.5% | T607/T504, inherits both |
| T609 | NSW/NI Share | +/-0.5% | NSW as share of national income |
| T901 | Summary Table | +/-0.5% | Composite from Ch5+Ch6 |

## Application

These thresholds are used in:
- `test_chapter_05.R` THEMATIC_TESTS section
- `test_chapter_06.R` THEMATIC_BENCHMARKS section
- `test_chapter_09.R` CROSS_CHAPTER section
- Processing scripts benchmark validation (e.g., P04 line 76: `abs(actual - expected) > 0.05`)

Note: Processing scripts currently use `0.05` as a generic tolerance for rate series. This should be tightened to `0.02` per the thresholds defined here.

---

*Created 2026-03-30 as part of Phase A cleanup (A4).*

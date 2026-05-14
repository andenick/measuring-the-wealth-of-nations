# Intentional Divergences from ST2

This document records places where the from-scratch re-build deliberately departs from ST2's implementation. Each divergence is grounded in the Anu Framework's rules (no proxies, no lazy splices, no synthetic data) and the book itself as ground truth.

---

## S507 — Surplus Ratio S\*/Y

**ST2 behavior**: T507 was loaded from `Inputs/ST_Chopped/ch05/ExploitationComposition_1948_1989.csv`, column `T509_surplus_ratio`, with 1948 value 0.5698 and 1989 value 0.5991. ST2's `validation_config.json` recorded these as the T507 benchmarks (0.57 and 0.60).

**Problem**: That source file is documented as "NIPA-derived exploitation and composition ratios" — not the book's Marxian S\*/Y. The values do not match the algebraic relation S\*/Y = e/(1+e) implied by the book's own published rate of exploitation (S506).

Independent check using the book's H.1 values at 1948:
- S\* = 149.94 (H.1)
- V\* = 88.41 (H.1)
- e = S\*/V\* = 1.70 (H.1, matches book Table 5.7 benchmark)
- S\*/(S\*+V\*) = 149.94/238.35 = 0.6291 = 1.70/2.70 = e/(1+e). ✓ self-consistent.

ST2's 0.5698 is a NIPA reconstruction with a different denominator concept — it can't simultaneously be true that the book reports e=1.70 *and* S/Y=0.57, because S/Y = e/(1+e) is an algebraic identity over the same accounting universe.

**New build's choice**: Re-author S507 to compute S\*/(S\*+V\*) directly from S505 and S504. Validate against the algebraically-implied benchmarks (0.6296 in 1948, 0.7093 in 1989). This is the book-faithful value. Document the NIPA-proxy alternative as an external sensitivity check (not the canonical S507) if needed.

**Where**:
- `code/P02_processors/P02_S507_surplus_ratio.py` — computes from S505/S504
- `code/V03_validators/V03_S507_surplus_ratio.py` — benchmarks 0.6296, 0.7093
- `series_registry.json` — S507 stays "derived" with construction documented

---

(Other divergences will be added here as they surface during the build.)

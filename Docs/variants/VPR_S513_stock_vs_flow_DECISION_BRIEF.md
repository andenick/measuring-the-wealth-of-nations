# Decision Brief: S513 Stock-Form vs Flow-Form Primary Adoption

**Series**: S513 (Marxian profit rate r*), S514 (capacity-adjusted r*_adj)
**Companion VPR**: `VPR_S513_stock_vs_flow.md` (v1.1 Phase 3, 2026-05-24)
**Author**: v1.2 Iter 1 Track A.1 (examine-only)
**Date**: 2026-05-24
**Status**: DECISION REQUIRED (user authorize / decline / defer)
**Scope**: READ-ONLY analysis. No code or registry changed.

---

## 1. Book Canonical Form (verbatim cite)

From *Measuring the Wealth of Nations* §5.5, page 122 (KB extraction
`chunk_15/full_transcription.md` line 12):

> "the **Marxian general rate of profit r***, defined here as **the ratio
> of surplus value to total fixed capital K**;16 the average rate of
> profit r, defined as the ratio of profit-type income net of individual
> business taxes (P = P+ − IBT) to K..."

Footnote 16 (same page):

> "**More properly, one should add the stock of circulating capital** (i.e.,
> inventories of raw materials and goods in process, which are the **stock
> equivalents** of C* and V*, or M and W in the orthodox case) to the
> stock of fixed capital. But consistent data on the former are not
> readily available."

**Verdict**: The book defines r* in **stock form** unambiguously. Both the
fixed-capital denominator K and the ideal circulating-capital addition are
explicitly stock concepts. The footnote calls C* and V* "stock equivalents"
when used as a denominator, confirming that any flow form is a proxy for
the stock concept the book actually wants. The §5.5 figures (5.16, 5.17,
referenced as the "basic results") plot the stock-form r*.

The internal contradiction in `series_registry.json` is that S513's `name`
field declares `r* = S*/(C*+V*)` (flow form) while the published 1948-1989
data values in `chopped/S513.csv` (e.g. 1989 = 0.3723) are **identical to
r_stock** in `data/scratch/S513_stock_vs_flow.csv`. The book period was
computed stock-form; only the EXT block (1998-2024) was computed flow-form.
The naming label was never reconciled with the implementation.

---

## 2. ES Series Cross-Validation

| ES         | Source                       | Profit-rate form?                | Implication for S513             |
|------------|------------------------------|----------------------------------|----------------------------------|
| ES1201/02  | Moos 2017 (NSW)              | Not a profit rate; flow ratios   | Neutral                          |
| ES1401     | Mohun 2005 exploitation      | Not a profit rate                | Neutral                          |
| ES1402     | Mohun 2005 prod. labor share | Not a profit rate                | Neutral                          |
| ES1501-04  | Mohun 2013 unproductive labor| Stock/flow language re labor; no r* | Neutral                       |
| ES1701/02  | Cronin 2001 NZ s/v, surplus  | Not a profit rate; flow only     | Neutral                          |
| **ES1703** | **Cronin 2001 NZ c/v**       | **c/v = constant-cap flow / V (NOT fixed-cap stock)**. Cronin explicitly **criticizes Pearce (1986) for including fixed-capital stock in c**, calling it a 6-8x overestimate. | **Flow form for VCC, NOT for r*.** Cronin's c/v is the *value composition* (a flow ratio for organic composition analysis), **not** the rate of profit. The Pearce critique reinforces that adding *fixed-capital stock* to a *flow* denominator (which is what hybrid stock/flow mixing does) is a methodological error in the Shaikh tradition. |
| ES1704     | Cronin 2001 NZ total value   | Flow only; no r*                 | Neutral                          |

**Verdict**: None of the ES replications publish a competing r* in flow
form. ES1703 (Cronin) is the only direct methodological signal and it
**supports stock-form integrity**: it treats c/v as a flow ratio for VCC
analysis specifically because it is NOT the rate of profit, and it warns
against the very mixing (stock-in-numerator-flow-in-denominator) that the
current S513 splice performs. No ES series provides evidence to prefer
flow-form r* over stock-form r* for the headline S513.

---

## 3. Three Trend Scenarios (1948-2024)

Computed from `data/scratch/S513_stock_vs_flow.csv` (69 years where all
inputs combined; 1990-1997 gap preserved). Trends are OLS slopes on
`log(r) ~ year`.

| Scenario       | r(1948) | r(2024) | Δ% endpoint-to-endpoint | log-trend / yr | Narrative compatibility |
|----------------|--------:|--------:|------------------------:|---------------:|-------------------------|
| **Stock-form primary** (S*/(K*+V*)) | 0.3946 | 0.1604 | **−59.4%** | **−1.66 %/yr** | Strong TRPF: confirms Shaikh narrative; consistent with §5.5 "basic results" of profit-rate decline; visible Reagan recovery 1980-89 followed by deeper post-1989 decline |
| **Flow-form primary** (S*/(C*+V*))   | 0.5227 | 0.4903 | **−6.2%**  | **−0.56 %/yr** | Weak/ambiguous TRPF: profit rate roughly flat; would contradict Ch.5 §5.5 and Ch.9 conclusions |
| **Current splice** (stock 1948-89 + flow 1998-2024) | 0.3946 | 0.4903 | **+24.3%** | **+0.16 %/yr** | **Anti-TRPF**: profit rate rises 24% over 76 years. Optically continuous because denominator silently shrinks at the splice. **Directly contradicts the book the project replicates.** |

Splice-junction discontinuity made visible by stock-form adoption:
- Stock: 0.3723 (1989) → 0.1693 (1998) = **−54% in 9 years** (real economic event)
- Flow:  0.6563 (1989) → 0.3583 (1998) = −45% in 9 years (real economic event)
- Published splice: 0.3723 → 0.3583 = −3.8% (optical smoothing only)

The current published series **manufactures continuity** by switching
denominators at the moment of the largest post-war structural break.

---

## 4. Cascade Impact

Downstream artifacts affected by form choice:

| Artifact                                     | Affected? | Notes |
|----------------------------------------------|-----------|-------|
| `series_registry.json` S513                  | Yes       | Name string + extension formula must align (currently mis-aligned) |
| `series_registry.json` S514                  | Yes       | S514 = S513 × TCU; same form choice cascades |
| `code/scripts/P02_S513.py`                   | Yes       | Recompute EXT under stock form using S517-COMBINED |
| `code/scripts/P02_S514.py`                   | Yes       | Inherits S513 form change |
| `code/scripts/V03_S513.py` / `V03_S514.py`   | Yes       | Reference values at extension endpoints change (1998: 0.3583 → 0.1693) |
| `chopped/S513.csv`, `chopped/S514.csv`       | Yes       | Regenerate; metadata Row 1 form-string must match |
| Figures 5.5, 5.8, 9.2, 9.4 (per registry)    | Yes       | Visual narrative changes substantially (deeper post-1989 decline) |
| `DIVERGENCE_REGISTER.json`                   | Yes       | Add DIV-009 explicit splice-form-change disclosure |
| Methodology docs (`docs/methodology/`)       | Yes       | Add explanation of stock-form primacy + variant flow-form availability |
| Variant subseries `S513-EXT-FLOW` (new)      | Yes       | Retain flow-form as published variant per VPR |
| Upstream S505/S502/S504/S517                 | **No**    | Inputs unchanged; only derived series re-run |
| Other r* dependents (none in registry)       | n/a       | Self-contained cascade |

---

## 5. Recommendation

**Adopt stock-form as primary across full 1948-2024 span. Retain flow-form
as published variant subseries `S513-EXT-FLOW` / `S514-EXT-FLOW`.**

**Confidence**: HIGH.

Arguments by option:

**Stock-form primary (recommended)**
- For: book canonical (§5.5 verbatim definition); matches existing book-period
  data (no 1948-89 recompute); preserves §5.5 / Ch.9 narrative; eliminates
  silent splice methodology change (Decision 0008 spirit); cross-validated
  by ES1703 Pearce-critique logic; reveals real post-1989 economic
  decline currently masked.
- Against: visible post-1989 discontinuity may look like a "data problem"
  to casual readers (mitigated by explicit splice disclosure in viz captions);
  requires S514 lockstep change.

**Flow-form primary**
- For: data availability simpler (no S517 K* extension dependency); flow
  ratios used in book's §5.4 reproduction-flow discussions.
- Against: contradicts §5.5 verbatim definition of r*; weakens TRPF
  narrative the project exists to replicate; no ES support; would require
  recomputing book period 1948-89.

**Status-quo splice**
- For: zero work; existing artifacts unchanged.
- Against: **trend reverses sign** (+24% vs book's documented decline);
  silent methodology change; violates Decision 0008 splice-disclosure
  expectation; the published headline number actively contradicts the
  book this project replicates. **Indefensible on methodological grounds.**

---

## 6. Implementation Cost

**If user APPROVES stock-form adoption** (iteration 3 work):

Files to touch (≈12 edits, 2 iterations):
1. `series_registry.json` — fix S513 name (`S*/(K*+V*)`), update S513.extension
   formula + provenance, mirror for S514; add `S513-EXT-FLOW` and
   `S514-EXT-FLOW` variant subseries entries.
2. `code/scripts/P02_S513.py` — extension branch uses K*+V* (from S517-COMBINED).
3. `code/scripts/P02_S514.py` — inherits via S513 input.
4. `code/scripts/V03_S513.py`, `V03_S514.py` — update extension reference
   values (1998 anchor: 0.1693 stock; tolerance bands).
5. `chopped/S513.csv`, `chopped/S514.csv` — regenerate via Stage 6a.
6. `DIVERGENCE_REGISTER.json` — add DIV-009.
7. Viz scripts for Fig_5_5, Fig_5_8, Fig_9_2, Fig_9_4 — re-render.
8. `docs/methodology/S513_primary_form.md` — new methodology note.
9. `VPR_S513_stock_vs_flow.md` — flip status from `exploratory` to
   `adopted_v1.2`; add adoption-date stamp.
10. Optional companion: author `VPR_S514_stock_vs_flow.md` (paired VPR).
11. `STEP_LOG.jsonl`, `ANU_LEDGER.json`, `MANIFEST.json` — regen.
12. `NARRATIVE.md` — short update.

Re-baseline cost: V03 regression tests for S513 and S514 must accept new
extension reference values; otherwise pipeline-internal.

**If user DECLINES** (status quo retained):

Files to touch (≈3 edits, 1 short iteration):
1. `series_registry.json` — at minimum, fix the S513 name field so it no
   longer claims `S*/(C*+V*)` while the book-period data is stock-form
   (current state is internally contradictory regardless of which form is
   chosen as primary).
2. `DIVERGENCE_REGISTER.json` — strengthen DIV-005 to spell out the
   trend-sign reversal explicitly (current entry understates the impact).
3. `VPR_S513_stock_vs_flow.md` — flip status from `exploratory` to
   `declined_v1.2` with user-supplied rationale.

The naming/data mismatch in (1) above is a defect that must be fixed
regardless of the primary-form decision.

---

## 7. STEP_LOG Entry

Appended to `Technical/STEP_LOG.jsonl`:

```json
{"ts": "2026-05-24T00:00:00Z", "step_id": "v1.2-iter1-A1-examine-S513", "mode": "execute", "stage": 9, "cohort": "v1.2_iter1", "series": "S513,S514", "action": "examine_S513_stock_vs_flow_decision_brief", "inputs": ["docs/variants/VPR_S513_stock_vs_flow.md", "Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_15", "research/ES1401-1704"], "outputs": ["docs/variants/VPR_S513_stock_vs_flow_DECISION_BRIEF.md"], "doctor_check_ids": [], "outcome": "pass", "artifacts_emitted": ["S513_decision_brief"], "notes": "Track A.1 examination complete; recommendation: stock-form primary, HIGH confidence; flow-form retained as published variant"}
```

# Decision Brief: S503 Broader-NAICS Coordinated Adoption (Track A.2)

**Series in scope**: S501, S502, S503, S505, S506, S507, S513, AS001, AS002
**Variant under examination**: Variant B (productive partition = `[11, 21, 22, 23, 31G, 42, 44RT, 48TW, 51, 54]`)
**Date**: 2026-05-24
**Author**: v1.2 Iteration 1, Track A.2 examiner
**Status**: EXAMINE ONLY — no methodology change committed
**Predecessor**: `VPR_S503_alt_extension.md` (anu-rebuild v1.1 Phase 3)

---

## 1. Identity Audit

### Canonical identity from Shaikh & Tonak 1994 Ch5 §5.2

> "GVA\* = TV\* − C\*m = Marxian gross value added." (ST 1994 p.95, chunk_12 line 154)

GFP\* is used interchangeably with GVA\* throughout Ch5 (p.92 visual derivation, p.94
Table 5.2 commentary, p.131 §5.7 productivity discussion). The relationship is a
**strict accounting identity** under the IO partition: GFP\* (S503) = TP\* (S501) − C\*_m (S502).

This is not a regression/proxy/splice — it follows necessarily from the productive
boundary chosen. The identity TV\* = TP\* is itself proved algebraically in §3.6.2
(chunk_10 lines 165–189) from IO row-sum = column-sum identities, conditional on
the partition.

**Implication**: If S501 and S502 are recomputed under a broader partition (Variant B),
S503 = S501 − S502 must be recomputed under the same partition for the identity to hold.
Computing S503 under Variant B while leaving S501/S502 under Variant A breaks the GFP
identity that V03_S503 validates. Coordinated adoption is therefore **required**, not
optional.

### S505 wedge: does it constrain Variant B?

`test_S505_identity_book_period` (XFAIL, `tests/test_identities.py` lines 77–104)
documents that S505-A ≠ S503-A − S504-A in the book period (1948–1989). The wedge
is attributed in the test docstring to the GFP\*/VA\* gap (indirect business taxes
and other accounting items present in S503 but not in S504+S505 in the book's per-table
exposition).

This wedge is **partition-invariant** at first order: broadening the partition
rescales the S503 level but does not change the structural reason S505 ≠ S503 − S504
in the book period (that reason is items between GFP and VA, not the productive
boundary). The wedge therefore neither blocks nor unlocks Variant B.

In the extension period, by construction (P02_S505 line 80):
S505-EXT = S503-COMBINED − S504-COMBINED. So **any S503 partition change propagates
1:1 to S505-EXT**.

---

## 2. Cross-Series Cascade

If S501/S502/S503 all adopt Variant B (broaden to include NAICS 51 + 54 from 1997
forward), the post-1997 extension period is affected as follows. Pre-1997 book values
are frozen and unaffected.

### 2024 endpoint values

Current chopped (Variant A) and projected (Variant B from `data/scratch/S503_alt_extension.csv`):

| Series  | Formula                          | 2024 Variant A | 2024 Variant B (est.) | Δ at 2024 |
|---------|----------------------------------|---------------:|----------------------:|----------:|
| S501-EXT | TP\* = Σ GO over partition       | 19224.3        | ~26900 (×1.40)        | +40%      |
| S502-EXT | C\*_m = Σ II over partition      | 9367.3         | ~13100 (×1.40)        | +40%      |
| S503-EXT | GFP = S501 − S502 = Σ VA         | 9857.0         | 13804.8 (verified)    | +40.1%    |
| S505-EXT | S\* = S503 − S504                | 6325.1         | ~10272 (S503_B − S504) | +62.4%    |
| S506-EXT | e = S505 / S504                  | 1.791          | ~2.908                | +62.4%    |
| S507-EXT | S/(S+V) = S505 / (S505 + S504)   | 0.642          | 0.744                 | +0.10 abs |
| S513-EXT | r\* = S505 / (S502 + S504)        | 0.490          | ~0.620                | +26.5%    |
| AS001-EXT | 1 − (NIPA L17 / S505)            | partial        | shifts: ~−10pp        | partial   |
| AS002-EXT | (similar S505 denominator)       | partial        | partial               | partial   |

S504 (variable capital) is independent of the GO/II/VA partition — it draws from
BLS productive-worker compensation under its own concordance and is unchanged by
Variant B.

### Cross-series cascade summary

- **Direct 1:1 partition shift** (S501, S502, S503, S505, S507, S513): all governed
  by the GFP identity chain. Coordinated re-derivation required.
- **Ratio amplification** (S505, S506, S513): the ratio S\*/V\* and r\* amplify
  partition shifts because the denominator V\* is unchanged while the numerator
  swells. Variant B raises e\* by ~62% and r\* by ~27% at 2024 — large enough to
  qualitatively change post-2000 narrative (currently e\* peaks ~1.8; under B it
  would peak >2.9, comparable to Cronin's NZ figures).
- **No cascade**: S701/S702 (Ch7 labor coefficients) use Appendix F's 13-NIPA
  partition with `productive_share > 0.5` filter (`L01_S701` lines 65–86), entirely
  independent of the S501–S503 NAICS partition. Ch6 series, ES1xxx, ES2xxx untouched.
- **Partial cascade** (AS001, AS002): use S505 in their numerator/denominator, so
  the S505 level shift propagates, but the AS series' qualitative content (social
  burden, social wage relations) re-anchors to a different baseline.

---

## 3. External-Study Alignment (ES-replication)

| Study                          | Productive partition | NAICS 51 (Info)? | NAICS 54 (Prof/Tech)? | Vote |
|--------------------------------|----------------------|------------------|------------------------|------|
| Shaikh & Tonak 1994 (book)     | SIC, narrow         | n/a (pre-NAICS) | n/a (pre-NAICS)        | A    |
| Mohun 2005 (ES1301/1302)       | ST's SIC, accepted  | n/a              | n/a                    | A    |
| Mohun 2013 (ES1401–1404)       | Modified            | **Yes — entirely productive** | Not explicitly stated  | **B-leaning** |
| Cronin 2001 (ES1701–1704)      | NZSNA 25-group, ST procedure | n/a (NZ classification) | n/a              | neutral |
| Moos 2017 (ES1201–1202)        | NSW, ST procedure   | n/a (AU classification) | n/a              | neutral |
| Tsoulfidis/Paitaridis 2019     | Narrow ST           | No               | No                     | A    |
| Karabacak/Tonak 2022 (ES1601-2)| ST framework (TR)   | n/a              | n/a                    | A    |

**Key finding**: Only Mohun 2013 in the RMWND ES corpus has explicitly broadened the
productive boundary, and his broadening directly endorses including **NAICS 51
Information as entirely productive** (ES1401 research line on classification
differences: "his Information sector is treated as entirely productive, and retail
eating/drinking places are also classified productive"). This is a non-trivial
modern endorsement of the NAICS-51 half of Variant B.

Mohun 2013 does **not** explicitly endorse NAICS 54 Professional/Scientific/Technical
inclusion. Variant B's NAICS 54 component remains unsupported by external authority
and rests only on the "level continuity at 1997" argument.

**Partial-alignment hybrid (Variant B-prime)**: include NAICS 51 (Mohun-endorsed) but
exclude NAICS 54 (unsupported). Predecessor VPR did not test this; it would require
new code/E08 exploration to quantify whether the level-continuity benefit at 1997
survives without the 54 contribution. Likely answer: most of the +12.6% closure of
the Variant A gap comes from 51 + 54 jointly; 51 alone may leave a 10–15% residual
discontinuity. **This is a follow-up investigation, not a current decision input.**

---

## 4. Book-Fidelity vs Modernization Trade-Off

| Dimension                          | Variant A (current)         | Variant B (broader)                                |
|------------------------------------|-----------------------------|----------------------------------------------------|
| Book literalism                    | High — direct port of ST 1994 SIC partition via Appendix C concordance | Modernization choice; NAICS 51/54 had no clean SIC counterpart in book era |
| GFP identity preservation          | Yes (S503 = S501 − S502)    | Yes if coordinated; broken if S503-only            |
| 1997 SIC→NAICS continuity          | −20.7% downward step        | −0.2% essentially continuous                       |
| External-study alignment           | Aligns with most ES studies | Aligns with Mohun 2013                            |
| Curve-fitting risk                 | None                        | Real — 1997 level-match may be coincidence not principle |
| Cross-series concordance proven    | Yes (existing S501 EPR App. C) | No — would require new concordance audit       |
| Magnitude of post-1997 estimates   | Conservative, narrow productive core | +40% TP\*, +62% S\*, ~+27% r\* — qualitatively different story |

### What would ST do today?

The book's Appendix B documents that the SIC-era "Business Services" (SIC 73) was
partially included via the building/equipment rentals two-step procedure but explicitly
excluded "distributive transport" as a noted limitation (chunk_11 lines 323–330).
This suggests ST were case-by-case rather than dogmatic about boundary inclusions and
were willing to acknowledge their own omissions. Karabacak & Tonak 2022 (ES1601–1602,
applied to Turkey) uses an ST-style narrow partition, so the most recent ST coauthor
work continues with Variant A logic.

Net read: there is **no clean book signal** that ST would modernize to NAICS 51/54
inclusion. They might, but the evidence is absent rather than supportive.

---

## 5. Recommendation

**Retain Variant A as the primary methodology. Document Variant B as a per-anu-variant
methodology variant with traceable provenance and a clear follow-up pathway. Defer
Variant B coordinated adoption to a future cohort.**

**Decision 2026-05-24: declined per recommendation.** The S503 extension retains its primary methodology; the Variant B-prime (NAICS 51 only, Mohun-aligned) is recorded here for transparency but not adopted. No code changes.

Confidence: **Medium-high**. The decision could legitimately go either way given
Mohun 2013's NAICS 51 endorsement, but the implementation cost, qualitative narrative
shift, and absence of cross-series concordance audit weigh against unilateral
adoption in v1.2.

### Reasoning

1. **Identity preservation is now affirmatively confirmed as a constraint**:
   GFP = TP\* − C\*_m is a strict accounting identity from ST 1994 §5.2 p.95, not
   an approximation. Any partition change must be coordinated across S501/S502/S503.
   The Variant B move is **possible** (coordinated adoption is technically feasible),
   but it is a much bigger change than the predecessor VPR framing of "S503-only" implied.

2. **Cascade is large and qualitatively important**: at 2024, Variant B raises
   the rate of exploitation by 62% and the Marxian profit rate by 27%. These are
   load-bearing series for any political-economy reading of the post-2000 US. Such
   a shift demands the kind of concordance audit that anu-research stage would
   produce, not a v1.2 implementation iteration.

3. **External alignment is partial, not unanimous**: Mohun 2013 supports NAICS 51
   but not 54. Most other ES studies retain narrow partition. Variant B mixes
   one endorsed change with one unendorsed change.

4. **Implementation cost is real** (see §6 below) and the v1.2 release scope
   (Track A.2 examine + B/C/D/E tracks) cannot absorb a methodology-wide
   re-anchoring without delaying the release.

### Alternative paths considered

- **Variant B-prime (NAICS 51 only)**: would test whether Mohun-endorsed inclusion
  alone closes most of the gap. Estimated to leave 10–15% residual discontinuity at
  1997. **Recommend adding to future-cohort backlog** as the principled compromise.
- **Hybrid (B in -EXT only, A retained in book period)**: rejected. Creates an
  internal partition switch at 1997 that is a different kind of methodological
  break (different productive boundary between book and extension), violating the
  S&T conceptual continuity the extension is meant to provide.

---

## 6. Implementation Cost (for future coordinated adoption)

If a future cohort decides to adopt Variant B, the following changes are required:

### Code changes
- `code/L01_loaders/L01_S501_total_product.py` — extend `PRODUCTIVE_TRADE_INDUSTRIES`
- `code/L01_loaders/L01_S502_constant_capital.py` — same
- `code/L01_loaders/L01_S503_gross_final_product.py` — same
- `code/P02_processors/P02_S501.py`, `P02_S502.py`, `P02_S503.py` — re-anchor
  1990–1996 log-linear bridge to new 1997 endpoint
- `code/V03_validators/V03_S501.py`, `V03_S502.py`, `V03_S503.py` —
  update `reference_values` in series_registry to new 1997 endpoint
- `code/P02_processors/P02_S505.py`, `P02_S506.py`, `P02_S507.py`, `P02_S513.py`,
  `P02_AS001.py`, `P02_AS002.py` — no code change, but outputs shift

### Documentation
- `docs/series/S501_EPR.md` Appendix C — new concordance section explaining
  NAICS 51/54 inclusion criterion under Shaikh productive-labor test
- `docs/series/S502_EPR.md`, `S503_EPR.md` — same
- `DIVERGENCE_REGISTER.json` — promote DIV-007 from "variant tracked" to
  "methodology adopted"; update DIV-003 vintage-note framing
- `docs/methodology/productive_classification_NAICS.md` — update partition
  documentation

### Registry / pipeline
- `series_registry.json` — update `extension.reference_values` for S501, S502,
  S503, S505, S506, S507, S513
- Re-run S501/S502/S503/S504/S505/S506/S507/S513/AS001/AS002 chopped/extenbook
  builds
- Re-run all validators (V03)
- Update visualizations (viz/) for affected series — narrative panel text changes
- `PIPELINE_STATE.json` and `STEP_LOG` entries

### Validation
- `tests/test_identities.py` — `test_S505_identity_book_period` xfail unchanged
  (wedge is partition-invariant)
- `tests/test_regression.py` — golden_chopped fixtures for affected series need
  regeneration
- Verify ES1401–1404 (Mohun 2013) divergence narrative still holds under new
  partition (since RMWND would now partially align with Mohun's classification)

### Estimated effort
- 1 dedicated cohort (3–5 iterations) for coordinated S501/S502/S503 change with
  full concordance documentation
- Half-iteration for downstream propagation through S505/S506/S507/S513/AS001/AS002
- Quarter-iteration for viz regeneration and ES alignment audit

**Total: ~1.5–2 release cohorts of focused work**, justifying deferral to a future
release rather than absorption into v1.2.

---

## 7. STEP_LOG Entry

```
{"ts": "2026-05-24T<UTC>", "step_id": "v1.2-iter1-A2-examine-S503", "mode": "execute", "stage": 9, "cohort": "v1.2_iter1", "series": "S501,S502,S503,S505,S506,S507,S513,AS001,AS002", "action": "examine_S503_broader_NAICS_decision_brief", "inputs": ["docs/variants/VPR_S503_alt_extension.md", "Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/", "research/ES*"], "outputs": ["docs/variants/VPR_S503_alt_extension_DECISION_BRIEF.md"], "doctor_check_ids": [], "outcome": "pass", "artifacts_emitted": ["S503_decision_brief"], "notes": "Track A.2 examination complete; recommendation: variant_A (retain) with Variant B-prime (NAICS 51 only) added to future-cohort backlog"}
```

---

## References

- `docs/variants/VPR_S503_alt_extension.md` — predecessor exploratory VPR
- `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_10/full_transcription.md` — Ch3 §3.6 TV\*=TP\* identity proof
- `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_12/full_transcription.md` — Ch5 §5.2 GVA\* = TV\* − C\*m
- `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_15/full_transcription.md` — §5.7 GFPr in quasi-Marxian productivity
- `Technical/tests/test_identities.py` lines 77–104 — S505 wedge XFAIL documentation
- `Technical/code/L01_loaders/L01_S501_total_product.py`, `L01_S502_constant_capital.py`, `L01_S503_gross_final_product.py` — current PRODUCTIVE_TRADE_INDUSTRIES (Variant A)
- `Technical/code/L01_loaders/L01_S701_labor_values.py` lines 65–86 — Appendix F 13-NIPA partition (Ch7, independent)
- `Technical/research/ES1401_research.json` — Mohun 2013 classification differences
- `Technical/research/S503_research.json` — verbatim ST 1994 quotes on GVA\* = TV\* − C\*m
- `Technical/data/scratch/S503_alt_extension.csv` — Variant A/B/C levels 1948–2024
- `Technical/chopped/S503.csv`, `S505.csv`, `S504.csv` — current 2024 endpoints

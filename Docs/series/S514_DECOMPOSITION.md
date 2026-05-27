# S514 — Decomposition

**Series**: Capacity-Adjusted Profit Rate (r*_adj = r*Ã—TCU)

## Construction Flow

```mermaid
flowchart TD
    S514_A["S514-A<br/>S&T 1994"]
    S514_EXT["S514-EXT<br/>FRED TCU"]
    S514_COMBINED["S514-COMBINED<br/>"]
    S514_EXT["S514-EXT<br/>derive: r*_adj = r* Ã— TCU"]
    S513_COMBINED --> S514_EXT
    S514_COMBINED["S514-COMBINED<br/>splice"]
    S514_A --> S514_COMBINED
    S514_EXT --> S514_COMBINED
```

## Step-by-step construction

**Step 1** — load
  - Inputs: S514-A

**Step 2** — derive
  - Inputs: S513-COMBINED
  - Output: `S514-EXT`
  - Formula: `r*_adj = r* Ã— TCU`

**Step 3** — splice
  - Inputs: S514-A, S514-EXT
  - Output: `S514-COMBINED`
  - At year: 1989

## Extension

- Splice year: 1989
- Splice method: derive
- Depends on: S513

## Provenance

See [`S514_DPR.md`](S514_DPR.md) for the canonical Data Provenance Record, including source-file citations, validation benchmarks, and known caveats.

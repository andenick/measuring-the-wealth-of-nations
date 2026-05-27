# S515 — Decomposition

**Series**: Productive Employment (Lp)

## Construction Flow

```mermaid
flowchart TD
    S515_A["S515-A<br/>S&T 1994"]
    S515_EXT["S515-EXT<br/>BLS CES"]
    S515_COMBINED["S515-COMBINED<br/>"]
    S515_COMBINED["S515-COMBINED<br/>splice"]
    S515_A --> S515_COMBINED
    S515_EXT --> S515_COMBINED
```

## Step-by-step construction

**Step 1** — load
  - Inputs: S515-A

**Step 2** — load
  - Inputs: S515-EXT

**Step 3** — splice
  - Inputs: S515-A, S515-EXT
  - Output: `S515-COMBINED`
  - At year: 1989

## Extension

- Splice year: 1989
- Splice method: level
- Depends on: (none)

## Provenance

See [`S515_DPR.md`](S515_DPR.md) for the canonical Data Provenance Record, including source-file citations, validation benchmarks, and known caveats.

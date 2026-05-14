# S511 — Decomposition

**Series**: Productive Labor Share (Lp/L)

## Construction Flow

```mermaid
flowchart TD
    S511_A["S511-A<br/>S&T 1994"]
    S511_EXT["S511-EXT<br/>BLS CES"]
    S511_COMBINED["S511-COMBINED<br/>"]
    S511_COMBINED["S511-COMBINED<br/>splice"]
    S511_A --> S511_COMBINED
    S511_EXT --> S511_COMBINED
```

## Step-by-step construction

**Step 1** — load
  - Inputs: S511-A

**Step 2** — load
  - Inputs: S511-EXT

**Step 3** — splice
  - Inputs: S511-A, S511-EXT
  - Output: `S511-COMBINED`
  - At year: 1989

## Extension

- Splice year: 1989
- Splice method: level
- Depends on: (none)

## Provenance

See [`S511_DPR.md`](S511_DPR.md) for the canonical Data Provenance Record, including source-file citations, validation benchmarks, and known caveats.

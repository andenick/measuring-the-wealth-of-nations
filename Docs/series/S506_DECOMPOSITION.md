# S506 — Decomposition

**Series**: Rate of Exploitation (e = S*/V*)

## Construction Flow

```mermaid
flowchart TD
    S506_A["S506-A<br/>S&T 1994"]
    S506_EXT["S506-EXT<br/>BLS CES + BEA NIPA"]
    S506_COMBINED["S506-COMBINED<br/>"]
    S506_EXT["S506-EXT<br/>derive: e = 1.238/(V*/W) - 1"]
    S506_COMBINED["S506-COMBINED<br/>splice"]
    S506_A --> S506_COMBINED
    S506_EXT --> S506_COMBINED
```

## Step-by-step construction

**Step 1** — load
  - Inputs: S506-A

**Step 2** — derive
  - Output: `S506-EXT`
  - Formula: `e = 1.238/(V*/W) - 1`

**Step 3** — splice
  - Inputs: S506-A, S506-EXT
  - Output: `S506-COMBINED`
  - At year: 1989

## Extension

- Splice year: 1989
- Splice method: derive
- Depends on: S512

## Provenance

See [`S506_DPR.md`](S506_DPR.md) for the canonical Data Provenance Record, including source-file citations, validation benchmarks, and known caveats.

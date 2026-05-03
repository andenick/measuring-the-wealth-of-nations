# AS2 NickyData Package
## Shaikh & Tonak (1994) Replication and Extension

A unified data construction package replicating and extending the empirical work in
*Measuring the Wealth of Nations* (Shaikh & Tonak, 1994) plus 8 related academic studies.

## Architecture

NickyData v1.1 — 8-phase pipeline:

```
S## (Setup) → L## (Load) → P## (Process) → V## (Validate)
    → M## (Manual Adjust) → A## (Analyze) → O## (Output) → E## (Explore)
```

## Structure

### Book Replication (Chapters 4-9)
26 T-series replicating the book's empirical tables, extended 1948-2024.

### External Studies (8 papers)
22 N-series replicating quantitative work from related scholarship:
1. Tonak (1984) — State Revenues & Expenditures
2. Shaikh & Tonak (1987) — Social Wage Myth
3. Shaikh & Tonak (2002) — Rise and Fall of Welfare State
4. Moos (2017) — NSW in the 21st Century
5. Mohun (2005) — Productive Labor 1964-2001
6. Mohun (2013) — Unproductive Labor Decomposition
7. Karabacak & Tonak (2022) — NSW Turkey
8. Cronin (2001) — NZ Productive Capital

## Running

```bash
python run.py                    # Full pipeline
python run.py --dry-run          # Show plan
python run.py --from P           # Resume from processing
python run.py --setup-only       # Validate environment
python run.py --report           # Status report
```

## Key Findings

- Exploitation rate: 1.70 (1948) → 2.44 (1989) → ~3.59 (2024) = +111%
- Productive labor share: declining from 57% to ~25%
- Moos structural shift: NSW reverses post-2000 (from -1.1% to +1.4% GDP)
- Turkey: NSW negative ALL 40 years (strongest confirmation)
- ST/Mohun exploitation ratio: 1.61 (different classifications)
- Both divergences resolved (DIV-001 K→K*, DIV-002 ec_u/ec_p)

## Configuration

- `project_registry.json` — single source of truth
- `data/user-inputs/api_keys.env` — API credentials (BEA, FRED, BLS)

## Version: 6.0.0 (NickyData restructure)

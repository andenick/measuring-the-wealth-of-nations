# T901: Summary Table — Decomposition

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | T901 |
| Name | Summary Table |
| Chapter | 9 |
| Book Table | 9.1 |
| Period | 1948-1989 |
| Units | Various (ratios, indices) |
| Tier | 1 |
| Wave | 1 |

## Sub-Components

| Subseries | Name | Source | Period | Units |
|-----------|------|--------|--------|-------|
| T901-A | Summary table (assembled) | Book 9.1 | 1948-1989 | Various |

## Construction Steps

| Step | Operation | Input | Output | Notes |
|------|-----------|-------|--------|-------|
| 1 | Load | T506 | Rate of surplus value | Chapter 5 series |
| 2 | Load | T511 | Profit rate component | Chapter 5 series |
| 3 | Load | T512 | Profit rate component | Chapter 5 series |
| 4 | Load | T513 | Profit rate component | Chapter 5 series |
| 5 | Load | T514 | Profit rate component | Chapter 5 series |
| 6 | Load | T608 | NSW/V* | Chapter 6 series |
| 7 | Assemble | T506, T511-T514, T608 | T901 | No independent NIPA inputs; pure assembly |

## Flow Diagram

```mermaid
graph TD
    subgraph "Chapter 5 — Production & Profit"
        T504["T504<br/>Value Added (V*)"]
        T506["T506<br/>Rate of Surplus Value"]
        T511["T511<br/>Profit Rate Component"]
        T512["T512<br/>Profit Rate Component"]
        T513["T513<br/>Profit Rate Component"]
        T514["T514<br/>Profit Rate Component"]
    end

    subgraph "Chapter 6 — Net Social Wage"
        T601["T601<br/>Personal Tax Workers"]
        T602["T602<br/>Social Insurance Tax"]
        T603["T603<br/>Property Tax Workers"]
        T601 --> T604["T604<br/>Total Tax (T_w)"]
        T602 --> T604
        T603 --> T604

        T605["T605<br/>Benefits (B_w)"]
        T606["T606<br/>Services (G_w)"]

        T605 --> T607["T607<br/>Net Social Wage"]
        T606 --> T607
        T604 --> T607

        T607 --> T608["T608<br/>NSW/V*"]
        T504 --> T608
    end

    subgraph "Chapter 9 — Summary Assembly"
        T506 --> ASSEMBLE["ASSEMBLE<br/>Summary Table"]
        T511 --> ASSEMBLE
        T512 --> ASSEMBLE
        T513 --> ASSEMBLE
        T514 --> ASSEMBLE
        T608 --> ASSEMBLE
        ASSEMBLE --> T901["T901<br/>Summary Table<br/>(1948-1989)"]
    end

    style T901 fill:#f9f,stroke:#333,stroke-width:2px
    style ASSEMBLE fill:#bbf,stroke:#333,stroke-width:2px
    style T607 fill:#ddf,stroke:#333,stroke-width:1px
    style T608 fill:#ddf,stroke:#333,stroke-width:1px
```

## Source Methodology

See `Technical/research/T901_research.json` for full research documentation.

The Summary Table assembles key results from Chapters 5 and 6 into a single consolidated view. It draws on the rate of surplus value (T506), profit rate components (T511-T514), and the net social wage ratio (T608). No independent NIPA inputs are required — this is a pure assembly operation from upstream series.

Key figures: 9.1, 9.2, 9.3, 9.4, 9.5.

## Related Series

- **T506** — Rate of Surplus Value (input)
- **T511** — Profit Rate Component (input)
- **T512** — Profit Rate Component (input)
- **T513** — Profit Rate Component (input)
- **T514** — Profit Rate Component (input)
- **T608** — NSW/V* (input, which depends on T607 and T504)

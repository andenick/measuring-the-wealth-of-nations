# T501 — Extension Provenance Record

## Agent Understanding

T501 (Total Product, TP*) is extended from 1962-2024 using BEA GDP-by-Industry gross output data. The book period (1948-1961) comes from Table E.2.

## Original Methodology

Shaikh & Tonak compute TP* as gross output of productive and trading sectors from IO benchmark tables, interpolated between benchmark years using NIPA ratios.

## Current Methodology

Extension uses BEA GDP-by-Industry gross output (all industries, "II" code) spliced at 1997 via growth-rate method. P01 applies GDP growth rates to extend the book series forward.

## Methodology Changes

The extension proxy (total GDP-by-industry gross output) includes all sectors, not just productive+trading. This introduces a systematic bias if the unproductive sector share of gross output changes over time. Cross-validated against KLEMS gross output data.

## Faithfulness Score

**72%** — CERTIFIED WITH NOTES. Total gross output is a reasonable proxy for TP* growth rates, but does not perfectly capture the productive-sector restriction.

## Certification

**CERTIFIED WITH NOTES** — acceptable for trend analysis, level may diverge from true TP*.

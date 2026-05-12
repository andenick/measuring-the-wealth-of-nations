# Installation and Reproduction Guide

## Requirements

- Python 3.11+
- R 4.x (optional — only needed for the Shiny visualization app)
- ~50 MB disk space (repo) + ~200 MB (computed outputs)

## Setup

```bash
git clone https://github.com/andenick/measuring-the-wealth-of-nations.git
cd measuring-the-wealth-of-nations/Technical/NickyData
pip install -r requirements.txt
```

## Running the Pipeline

```bash
# Validate cached data (no API keys needed, ~2 seconds)
python run.py --validate-only

# Full pipeline: re-fetch all data from APIs, recompute, validate (~15 seconds)
python run.py --test-all

# Other modes
python run.py --from P          # Resume from processing phase
python run.py --setup-only      # Just setup scripts
python run.py --report          # Show pipeline status dashboard
python run.py --list            # List all 85 scripts
```

## API Keys (needed only for --test-all)

The `--validate-only` mode works immediately with cached data. To re-fetch fresh data from federal statistical agencies, you need free API keys:

1. Copy the template:
```bash
cp data/user-inputs/api_keys.env.example data/user-inputs/api_keys.env
```

2. Get free keys from:
   - **BEA**: https://apps.bea.gov/API/signup/
   - **FRED**: https://fred.stlouisfed.org/docs/api/api_key.html
   - **BLS**: https://data.bls.gov/registrationEngine/ (optional — increases rate limits)

3. Edit `data/user-inputs/api_keys.env`:
```
BEA_API_KEY=your_bea_key_here
FRED_API_KEY=your_fred_key_here
```

## Troubleshooting

**"BEA_API_KEY not found"**: Make sure `api_keys.env` is in `data/user-inputs/`, not the repo root.

**V15 data freshness warnings**: API data may be slightly stale if cached responses are old. Run `--test-all` to refresh.

**V01 reference value failure**: If a benchmark value changes after API refresh, this is a data vintage issue — BEA periodically revises historical estimates. The cached data in the repo represents the validated vintage.

**R Shiny app won't start**: Install R packages: `install.packages(c("shiny", "shinydashboard", "tidyverse", "plotly", "DT", "scales"))`. Then from `Technical/ShinyApp/`: `Rscript -e "shiny::runApp('.')"`.

## Outputs

After running the pipeline, outputs appear in:

- `Outputs/Data/COMPLETE_DATABASE/` — Master database (97 years x 48 series, CSV + Excel)
- `Outputs/Figures/` — 11 publication-quality figures (PNG + SVG)
- `Outputs/Reports/` — Methodology report (PDF)

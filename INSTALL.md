# Installation and Reproduction Guide

## Requirements

- Python 3.11+
- R 4.x (optional, for Shiny app only)

## Setup

```bash
git clone https://github.com/andenick/measuring-the-wealth-of-nations-replication.git
cd measuring-the-wealth-of-nations-replication/Technical/NickyData
pip install -r requirements.txt
```

## API Keys (for fresh data pulls)

Copy the example and fill in your keys:
```bash
cp data/user-inputs/api_keys.env.example data/user-inputs/api_keys.env
# Edit api_keys.env:
#   BEA_API_KEY=your_key_here
#   BLS_API_KEY=your_key_here
#   FRED_API_KEY=your_key_here
```

Free API keys from:
- BEA: https://apps.bea.gov/api/signup/
- BLS: https://data.bls.gov/registrationEngine/
- FRED: https://fred.stlouisfed.org/docs/api/api_key.html

## Reproduce

```bash
python run.py --test-all     # Full pipeline + verification (~100s)
python run.py --report       # Status dashboard
python run.py --list         # Show all 67 scripts
```

## Input Data

Some input datasets are too large for git. To obtain them:

1. **IO Matrices** (SIC 1947-1977): Available from BEA historical benchmark IO tables
2. **NAICS IO** (1997-2017): Available from `Inputs/IO_Matrices/NAICS/` or BEA API
3. **API Data**: Re-pulled automatically by L## scripts if API keys are configured
4. **Mohun Data**: Published in Mohun (2005) CJE Table 2

## Output

After running the pipeline:
- Master database: `Outputs/Data/COMPLETE_DATABASE/as2_master_1948_2024.csv`
- Figures: `Outputs/Figures/*.png`
- Report: `Outputs/Reports/AS2_Methodology_Report.pdf`

# Install / Setup

## Prerequisites

- Python 3.10 or newer (tested on 3.13)
- ~50 MB disk free (working tree + cached data)
- Optional: BEA, BLS, FRED API keys for fresh data fetches

## Install

```bash
git clone https://github.com/andenick/measuring-wealth-of-nations-replication.git
cd measuring-wealth-of-nations-replication
pip install -r requirements.txt
```

Required Python packages (in `requirements.txt`):

```
pandas>=2.0
numpy>=1.24
openpyxl>=3.1
requests>=2.31
```

## Quick verify (no API key needed)

```bash
python run.py --validate-only
```

Expected output:

```
Validation report: 64 series; status counts = {'PASS': 64}
```

This runs against the cached `data/raw/` BEA/BLS/FRED responses included in the repo. The build is fully reproducible offline.

## Fresh API fetches (optional)

To re-fetch data from the agencies directly rather than using the cached responses:

1. Get free API keys:
   - **BEA**: https://apps.bea.gov/API/signup/
   - **BLS**: https://data.bls.gov/registrationEngine/
   - **FRED**: https://fred.stlouisfed.org/docs/api/api_key.html

2. Copy the template:
   ```bash
   cp data/user-inputs/api_keys.env.template data/user-inputs/api_keys.env
   ```

3. Edit `data/user-inputs/api_keys.env`:
   ```
   BEA_API_KEY=your-key-here
   BLS_API_KEY=your-key-here
   FRED_API_KEY=your-key-here
   ```

4. Run the full pipeline:
   ```bash
   python run.py --test-all
   ```

   This re-fetches everything from the agencies, validates against the cached responses for parity, and produces the same 64 final CSVs.

`api_keys.env` is gitignored — your keys never leave your machine.

## Troubleshooting

**`ModuleNotFoundError: utils.paths`**: run scripts from the repo root, not from inside subdirectories. Each script adds the parent dir to `sys.path` but assumes you're invoking from the repo root.

**BEA rate-limit errors**: BEA caps free-tier at 100 requests/minute. The fetcher uses exponential backoff but if you hit a sustained 429, wait 1 minute and re-run with `--from L01_loaders` (resume mode, TBD).

**LaTeX errors building the methodology PDF**: install `texlive-full` (Linux) or MacTeX (macOS) / MiKTeX (Windows). The methodology PDF builds with `latexmk -pdf docs/methodology/methodology.tex`.

**Output dir permissions**: `data/intermediate/`, `data/final/`, `chopped/`, `extenbooks/` are written by the pipeline. Ensure they're writable.

## Development setup

For contributors:

```bash
pip install -e .
pytest code/tests/  # unit tests for utility modules (io_matrix, bea_cache, etc.)
```

CI runs `python run.py --validate-only` on every push; any series PASS → FAIL regression fails the build.

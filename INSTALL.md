# Install / Setup

## Prerequisites

- Python 3.10 or newer (tested on 3.13)
- ~50 MB disk free (working tree + cached data)
- Optional: BEA, BLS, FRED API keys for fresh data fetches

## Install

```bash
git clone https://github.com/andenick/measuring-the-wealth-of-nations.git
cd measuring-the-wealth-of-nations
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
python build.py status        # 9-stage pipeline state + gate marks
python tests/ci_smoke.py      # registry + every shipped data/*.csv load
```

Expected output:

```
# build.py status  -> the 9-stage pipeline table (8 PASS / 1 WAIVER), anu-doctor PASS
# ci_smoke.py       -> release v2.0 (registry version 2.3.0); 68/68 data CSVs parse and are non-empty
```

Both commands run fully offline against the shipped bundle. A green
`ci_smoke.py` (exit 0) is the package-integrity guarantee: the registry loads
and every shipped `data/*.csv` parses and is non-empty. See the README section
"What this bundle can and cannot reproduce" for the scope of offline verification.

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

4. Run the numbered loader scripts to re-fetch from the agencies, e.g.:
   ```bash
   python code/L00_setup/L00_bls_fetch.py
   # plus the other loaders under code/L01_loaders/
   ```

   The loaders re-fetch from BEA/BLS/FRED using your keys. Note: a full
   end-to-end rebuild of the final CSVs also requires the maintainer
   intermediate inputs (`data/final/`), which are not shipped in this bundle —
   see the README section "What this bundle can and cannot reproduce."

`api_keys.env` is gitignored — your keys never leave your machine.

## Troubleshooting

**`ModuleNotFoundError: utils.paths`**: run scripts from the repo root, not from inside subdirectories. Each script adds the parent dir to `sys.path` but assumes you're invoking from the repo root.

**BEA rate-limit errors**: BEA caps free-tier at 100 requests/minute. The fetcher uses exponential backoff but if you hit a sustained 429, wait 1 minute and re-run the loader script (loaders are idempotent — already-fetched files are skipped).

**LaTeX errors building the methodology PDF**: install `texlive-full` (Linux) or MacTeX (macOS) / MiKTeX (Windows). The methodology PDF builds with `latexmk -pdf docs/methodology/methodology.tex`.

**Output dir permissions**: `data/intermediate/`, `data/final/`, `chopped/`, `extenbooks/` are written by the pipeline. Ensure they're writable.

## Development setup

For contributors:

```bash
pip install -e .
pytest tests/  # regression + identity suite (93 pass / 2 skip / 2 xfail)
```

CI runs `python tests/ci_smoke.py` on every push; a package-integrity regression (registry or any shipped `data/*.csv` failing to load) fails the build.

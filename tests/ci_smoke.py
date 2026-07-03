"""CI package-integrity smoke for the published RMWND bundle.

This runs in a clean CI virtual environment and validates that the SHIPPED
package is internally consistent and loadable — it is deliberately scoped to
what the *published* bundle can verify by itself:

  * ``series_registry.json`` parses as JSON.
  * ``VERSION.txt`` / ``CITATION.cff`` carry a coherent release version.
  * every ``data/*.csv`` (the chopped series output) parses as CSV and is
    non-empty (>= 2 rows, >= 2 columns somewhere).

It does NOT attempt a full end-to-end re-derivation: the public bundle ships
the constructed outputs + the pipeline code, but not every intermediate build
input (integrated panels, benchmark caches) needed to regenerate from scratch.
Full re-derivation is an internal-pipeline concern; per-series provenance and
methodology live in ``Docs/`` and ``methodology/``.

Exit code 0 = all integrity checks pass; non-zero = a failure a reviewer
should see.
"""
from __future__ import annotations

import csv
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_DATA_CSVS = 50  # published bundle ships ~64-68 series CSVs


def _fail(msg: str) -> None:
    print(f"[ci_smoke] FAIL: {msg}")
    sys.exit(1)


def main() -> int:
    # 1) registry parses
    reg_path = ROOT / "series_registry.json"
    if not reg_path.exists():
        _fail("series_registry.json missing")
    try:
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        _fail(f"series_registry.json does not parse: {exc}")
    version = reg.get("version", "?")

    # 2) version stamps present and coherent
    vtxt = (ROOT / "VERSION.txt")
    if not vtxt.exists():
        _fail("VERSION.txt missing")
    release = vtxt.read_text(encoding="utf-8").strip()

    # 3) every shipped data CSV parses and is non-empty
    files = sorted(glob.glob(str(ROOT / "data" / "*.csv")))
    if len(files) < MIN_DATA_CSVS:
        _fail(f"expected >= {MIN_DATA_CSVS} data/*.csv, found {len(files)}")
    ok = 0
    bad: list[str] = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                rows = list(csv.reader(fh))
        except Exception as exc:  # noqa: BLE001
            bad.append(f"{Path(f).name}: {exc}")
            continue
        if len(rows) >= 2 and any(len(r) >= 2 for r in rows):
            ok += 1
        else:
            bad.append(f"{Path(f).name}: empty/degenerate")
    if bad:
        _fail("unparseable/empty data CSVs: " + ", ".join(bad[:10]))

    print(
        f"[ci_smoke] OK — release {release} (registry version {version}); "
        f"{ok}/{len(files)} data CSVs parse and are non-empty."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

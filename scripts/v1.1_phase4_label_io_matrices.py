"""
v1.1 Phase 4: Label BEA IO matrices with sector codes.

Reads cached unlabeled matrices in Inputs/ST2/Inputs/IO_Matrices/ and
writes labeled CSVs under Technical/data/intermediate/io_matrices_labeled/.

SIC era (1947, 1958, 1963, 1967, 1972, 1977): 85x85 bare floats.
  Labels applied from Inputs/ST2/Inputs/Concordances/io_85_to_nipa_13_concordance.csv.
  Sector codes 1..85 with names (and SIC ranges) preserved as metadata header.

NAICS era (1997, 2002, 2007, 2012, 2017): 75-row CSVs already labeled with
  RowCode column + 65 NAICS sector code headers; copied through with light
  normalization (verify col 0 is RowCode, restate index column name to
  'sector_code', drop blank trailing rows).
"""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path("D:/Arcanum/Projects/RMWND")
SRC_SIC = ROOT / "Inputs/ST2/Inputs/IO_Matrices"
SRC_NAICS = ROOT / "Inputs/ST2/Inputs/IO_Matrices/NAICS"
CONC = ROOT / "Inputs/ST2/Inputs/Concordances/io_85_to_nipa_13_concordance.csv"
OUT = ROOT / "Technical/data/intermediate/io_matrices_labeled"
OUT.mkdir(parents=True, exist_ok=True)

SIC_YEARS = ["1947", "1958", "1963", "1967", "1972", "1977"]
NAICS_YEARS = ["1997", "2002", "2007", "2012", "2017"]
MATRIX_TYPES_SIC = ["A", "L", "Z"]   # technical, Leontief inverse, transactions
MATRIX_TYPES_NAICS = ["A", "L"]


def load_85_sector_labels() -> list[tuple[str, str, str]]:
    """Return list of (code, name, sic_range) for the 85 BEA IO sectors."""
    rows: list[tuple[str, str, str]] = []
    with CONC.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((row["io_sector"], row["io_sector_name"], row["sic_range"]))
    assert len(rows) == 85, f"expected 85 sectors, got {len(rows)}"
    return rows


def label_sic_matrix(year: str, mtype: str, labels: list[tuple[str, str, str]]) -> tuple[str, int, int]:
    src = SRC_SIC / f"{year}_{mtype}_matrix.csv"
    if not src.exists():
        return ("missing", 0, 0)
    with src.open("r", encoding="utf-8", newline="") as f:
        data = list(csv.reader(f))
    # Trim trailing empty cells per row (some rows end with a stray comma).
    data = [[c for c in row] for row in data if any(c.strip() for c in row)]
    nrows = len(data)
    ncols = max(len(r) for r in data)
    if nrows != 85 or ncols not in (85, 86):
        return (f"bad_shape:{nrows}x{ncols}", nrows, ncols)
    # Strip trailing empty col if present (the 1947 sample showed a trailing comma).
    data = [r[:85] for r in data]

    codes = [c for c, _, _ in labels]
    names = [n for _, n, _ in labels]
    sic_ranges = [s for _, _, s in labels]

    out_path = OUT / f"{year}_{mtype}_matrix_labeled.csv"
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        # Header row: 'sector_code' label cell + 85 column sector codes.
        w.writerow(["sector_code", *codes])
        for i, row in enumerate(data):
            w.writerow([codes[i], *row])
    # Sidecar with names + SIC ranges for downstream readers.
    side = OUT / f"{year}_{mtype}_matrix_sector_index.csv"
    with side.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sector_code", "sector_name", "sic_range"])
        for c, n, s in zip(codes, names, sic_ranges):
            w.writerow([c, n, s])
    return ("ok", 85, 85)


def passthrough_naics_matrix(year: str, mtype: str) -> tuple[str, int, int]:
    src = SRC_NAICS / f"{year}_{mtype}_matrix_naics.csv"
    if not src.exists():
        return ("missing", 0, 0)
    with src.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    rows = [r for r in rows if any(c.strip() for c in r)]
    nrows = len(rows)
    ncols = len(rows[0])
    # Normalize index column header to 'sector_code' for consistency with SIC files.
    if rows and rows[0][0].strip().lower() in ("rowcode", "row code", ""):
        rows[0][0] = "sector_code"
    out_path = OUT / f"{year}_{mtype}_matrix_naics_labeled.csv"
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)
    return ("ok", nrows, ncols)


def main() -> None:
    labels = load_85_sector_labels()
    report: list[str] = []
    n_ok = 0
    for year in SIC_YEARS:
        for mtype in MATRIX_TYPES_SIC:
            status, r, c = label_sic_matrix(year, mtype, labels)
            report.append(f"SIC {year} {mtype}: {status} ({r}x{c})")
            if status == "ok":
                n_ok += 1
    for year in NAICS_YEARS:
        for mtype in MATRIX_TYPES_NAICS:
            status, r, c = passthrough_naics_matrix(year, mtype)
            report.append(f"NAICS {year} {mtype}: {status} ({r}x{c})")
            if status == "ok":
                n_ok += 1
    print(f"Labeled {n_ok} matrices.")
    print("\n".join(report))


if __name__ == "__main__":
    main()

"""Audit all 64 chopped CSVs vs Decision 0005 wide format + registry extension flags."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.paths import CHOPPED_DIR, REGISTRY  # noqa: E402


def audit() -> dict:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    series = reg["series"]

    results = []
    anomalies = []

    for sid in sorted(series.keys()):
        entry = series[sid]
        path = CHOPPED_DIR / f"{sid}.csv"
        if not path.exists():
            anomalies.append((sid, "missing chopped file"))
            results.append({"sid": sid, "status": "MISSING"})
            continue

        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        if len(rows) < 3:
            anomalies.append((sid, f"only {len(rows)} rows"))
            results.append({"sid": sid, "status": "TOO_FEW_ROWS", "rows": len(rows)})
            continue

        row1_meta = rows[0]
        row2_ids = rows[1]
        data_rows = rows[2:]

        # Wide format check: Row 2 should start with "Year"
        wide_ok = row2_ids[0] == "Year"

        cols = row2_ids[1:]  # subseries cols
        n_data_rows = len(data_rows)
        n_cols = len(cols)

        # Identify EXT/COMBINED columns
        has_ext_col = any(c.endswith("-EXT") for c in cols)
        has_combined_col = any(c.endswith("-COMBINED") for c in cols)
        has_a_col = any(c.endswith("-A") for c in cols)

        # EXT non-null count
        ext_idx = [i for i, c in enumerate(cols) if c.endswith("-EXT")]
        ext_nonnull = 0
        if ext_idx:
            for r in data_rows:
                for i in ext_idx:
                    cell = r[1 + i] if 1 + i < len(r) else ""
                    if cell not in ("", "nan", "NaN"):
                        ext_nonnull += 1

        # COMBINED non-null
        comb_idx = [i for i, c in enumerate(cols) if c.endswith("-COMBINED")]
        comb_nonnull = 0
        if comb_idx:
            for r in data_rows:
                for i in comb_idx:
                    cell = r[1 + i] if 1 + i < len(r) else ""
                    if cell not in ("", "nan", "NaN"):
                        comb_nonnull += 1

        # Registry extension declared?
        ext_decl = entry.get("extension") is not None

        rec = {
            "sid": sid,
            "wide_ok": wide_ok,
            "rows": n_data_rows,
            "cols": n_cols,
            "col_ids": cols,
            "has_a": has_a_col,
            "has_ext": has_ext_col,
            "has_combined": has_combined_col,
            "ext_nonnull": ext_nonnull,
            "comb_nonnull": comb_nonnull,
            "ext_declared": ext_decl,
            "status": entry.get("status", ""),
        }
        results.append(rec)

        # Anomaly checks
        if not wide_ok:
            anomalies.append((sid, "Row 2 doesn't start with 'Year'"))
        if ext_decl and not has_ext_col:
            anomalies.append((sid, "extension declared in registry but no -EXT col"))
        if ext_decl and not has_combined_col:
            anomalies.append((sid, "extension declared in registry but no -COMBINED col"))
        if ext_decl and has_ext_col and ext_nonnull == 0:
            anomalies.append((sid, "EXT col present but all null"))
        if not ext_decl and has_ext_col:
            anomalies.append((sid, "EXT col present but extension=null in registry"))

    return {"results": results, "anomalies": anomalies}


if __name__ == "__main__":
    out = audit()
    print(json.dumps(out, indent=2, default=str))

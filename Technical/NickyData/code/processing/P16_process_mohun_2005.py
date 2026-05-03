#!/usr/bin/env python3
"""P16 - Process Mohun (2005) series: N1401-N1404.

Formalizes Mohun's exploitation rate, productive labor, and variable capital
as proper pipeline series with book/combined columns and cross-validation.

Inputs:  parsed-raw/N1401-N1404_parsed.csv (from L15)
         final-data/series/T506.csv (for ST vs Mohun comparison)
Outputs: final-data/series/N1401.csv through N1404.csv
Dependencies: L15, P04 (for T506 comparison)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, STUDIES_OUT, RAW_DATA, ensure_dirs

SERIES_ID = "N1401"
SERIES_IDS = ["N1401", "N1402", "N1403"]
PRIORITY = 12


def process():
    ensure_dirs()
    parsed_dir = RAW_DATA / "parsed"
    steps = []
    data_dict = {}
    outputs = []

    for sid in SERIES_IDS:
        parsed_path = parsed_dir / f"{sid}_parsed.csv"
        if not parsed_path.exists():
            steps.append(f"{sid}: parsed file not found")
            continue

        df = pd.read_csv(parsed_path, index_col=0)
        if "value" not in df.columns:
            # Use first column
            df = df.rename(columns={df.columns[0]: "value"})

        series = df["value"].dropna()

        # For Mohun series, book = combined (no extension, direct data)
        out = pd.DataFrame({"book": series, "combined": series})
        out.index.name = "year"
        out_path = STUDIES_OUT / f"{sid}.csv"
        out.to_csv(out_path)

        outputs.append(str(out_path))
        data_dict[sid] = series
        steps.append(f"{sid}: {len(series)} rows ({int(series.index.min())}-{int(series.index.max())})")
        print(f"    [P16] {sid}: {len(series)} rows")

    # N1404: Compute ST/Mohun exploitation rate ratio
    t506_path = SERIES_OUT / "T506.csv"
    n1401_path = STUDIES_OUT / "N1401.csv"
    if t506_path.exists() and n1401_path.exists():
        t506 = pd.read_csv(t506_path, index_col=0)["combined"]
        n1401 = pd.read_csv(n1401_path, index_col=0)["combined"]

        common = t506.index.intersection(n1401.index)
        if len(common) > 0:
            ratio = t506[common] / n1401[common]
            out = pd.DataFrame({
                "st_e": t506[common],
                "mohun_e": n1401[common],
                "ratio": ratio,
                "combined": ratio,
            })
            out.index.name = "year"
            out_path = STUDIES_OUT / "N1404.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            data_dict["N1404"] = ratio
            steps.append(f"N1404: {len(ratio)} years, mean ratio={float(ratio.mean()):.2f}")
            print(f"    [P16] N1404: {len(ratio)} years (ST/Mohun ratio, mean={float(ratio.mean()):.2f})")

    return {
        "series_id": SERIES_ID,
        "status": "ok" if data_dict else "fail",
        "steps": steps,
        "data_dict": data_dict,
        "outputs": outputs,
    }

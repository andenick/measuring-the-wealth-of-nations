#!/usr/bin/env python3
"""O05 - Generate Shiny-compatible CSVs from NickyData final-data.

Bridges the NickyData pipeline to the legacy R Shiny app by reading
series_registry.json and writing updated data files to ShinyApp/data/.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
import pandas as pd
from utils.paths import (
    SERIES_OUT, STUDIES_OUT, CONFIG, TECHNICAL, ensure_dirs,
)

SHINY_DATA = TECHNICAL / "ShinyApp" / "data"


def generate():
    ensure_dirs()
    SHINY_DATA.mkdir(parents=True, exist_ok=True)

    reg_path = CONFIG / "series_registry.json"
    with open(reg_path, encoding="utf-8") as f:
        registry = json.load(f)

    outputs = []

    ch5_series = ["T501", "T502", "T503", "T504", "T505", "T506",
                   "T507", "T508", "T509", "T510", "T511", "T512",
                   "T513", "T514", "T515", "T516"]
    _write_chapter_csv(ch5_series, "exploitation_composition_1948_2024.csv", outputs)

    ch6_series = ["T601", "T602", "T603", "T604", "T605", "T606",
                   "T607", "T608", "T609"]
    _write_chapter_csv(ch6_series, "nsw_1952_2025.csv", outputs)

    rate_series = ["T506", "T511", "T512", "T513", "T514"]
    _write_chapter_csv(rate_series, "summary_indicators_1948_2024.csv", outputs)

    employment = ["T515", "T516"]
    _write_chapter_csv(employment, "employment_1948_2024.csv", outputs)

    profit = ["T513", "T514"]
    _write_chapter_csv(profit, "profit_rates_1948_2024.csv", outputs)

    n_nsw = ["N1301", "N1302", "N1304", "N1305"]
    _write_study_csv(n_nsw, "moos_nsw_comparison.csv", outputs)

    n_mohun = ["N1401", "N1402", "N1403", "N1404"]
    _write_study_csv(n_mohun, "mohun_comparison.csv", outputs)

    n_intl = ["N1601", "N1602", "N1701"]
    _write_study_csv(n_intl, "international_nsw.csv", outputs)

    summary = f"{len(outputs)} Shiny data files generated"
    print(f"    [O05] {summary}")
    return {"status": "ok", "summary": summary, "outputs": outputs}


def _write_chapter_csv(series_ids: list[str], filename: str, outputs: list):
    merged = pd.DataFrame()
    for sid in series_ids:
        csv_path = SERIES_OUT / f"{sid}.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path, index_col=0)
            if "combined" in df.columns:
                merged[sid] = df["combined"]
            elif "book" in df.columns:
                merged[sid] = df["book"]

    if not merged.empty:
        merged.index.name = "year"
        out_path = SHINY_DATA / filename
        merged.to_csv(out_path)
        outputs.append(str(out_path))


def _write_study_csv(series_ids: list[str], filename: str, outputs: list):
    merged = pd.DataFrame()
    for sid in series_ids:
        csv_path = STUDIES_OUT / f"{sid}.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path, index_col=0)
            if "combined" in df.columns:
                merged[sid] = df["combined"]

    if not merged.empty:
        merged.index.name = "year"
        out_path = SHINY_DATA / filename
        merged.to_csv(out_path)
        outputs.append(str(out_path))

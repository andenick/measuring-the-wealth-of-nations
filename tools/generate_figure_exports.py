"""Generate static PNG exports of representative RMWND series for Outputs/Figures/.

Reads the project's chopped CSVs (wide format: Year, S###-A, S###-B, S###-COMBINED, ...)
and produces minimally-styled matplotlib line plots, one PNG per selected SID.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parents[2]
TECHNICAL = PROJECT / "Technical"
CHOPPED = TECHNICAL / "chopped"
REGISTRY_PATH = TECHNICAL / "series_registry.json"
OUT_DIR = PROJECT / "Outputs" / "Figures"

REPRESENTATIVE = [
    "S501", "S506", "S511", "S513", "S601",
    "S607", "S701", "ES1001", "ES1401", "AS003",
]


def load_registry() -> dict:
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        reg = json.load(f)
    return reg.get("series", {})


def parse_wide_csv(csv_path: Path) -> tuple[list[str], list[int], dict[str, list[float]]]:
    """Parse a chopped CSV in RMWND wide format.

    Row 1: metadata comment (skipped)
    Row 2: header => Year, SID-A, SID-B, SID-COMBINED, ...
    Row 3+: data
    Returns (column_names_without_year, years, columns_dict[colname]=values)
    """
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    # find header row - it starts with 'Year'
    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0].strip().lower() == "year":
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"No 'Year' header found in {csv_path}")
    header = rows[header_idx]
    data_rows = rows[header_idx + 1:]
    cols = header[1:]
    years: list[int] = []
    col_vals: dict[str, list[float]] = {c: [] for c in cols}
    for r in data_rows:
        if not r or not r[0].strip():
            continue
        try:
            y = int(float(r[0]))
        except ValueError:
            continue
        years.append(y)
        for j, c in enumerate(cols, start=1):
            v = r[j] if j < len(r) else ""
            try:
                if v.strip().lower() in ("", "nan", "na", "none"):
                    col_vals[c].append(float("nan"))
                else:
                    col_vals[c].append(float(v))
            except ValueError:
                col_vals[c].append(float("nan"))
    return cols, years, col_vals


def plot_series(sid: str, registry: dict) -> Path | None:
    csv_path = CHOPPED / f"{sid}.csv"
    if not csv_path.exists():
        print(f"  [skip] {sid}: chopped CSV not found")
        return None
    entry = registry.get(sid, {})
    name = entry.get("name", sid)
    units = entry.get("units", "")
    try:
        cols, years, col_vals = parse_wide_csv(csv_path)
    except Exception as e:
        print(f"  [error] {sid}: {e}")
        return None
    if not years:
        print(f"  [skip] {sid}: no data rows")
        return None

    fig, ax = plt.subplots(figsize=(9, 5))
    plotted_any = False
    for c in cols:
        vals = col_vals[c]
        # filter NaNs by aligning years
        xy = [(y, v) for y, v in zip(years, vals) if not (isinstance(v, float) and math.isnan(v))]
        if not xy:
            continue
        xs = [p[0] for p in xy]
        ys = [p[1] for p in xy]
        ax.plot(xs, ys, label=c, linewidth=1.4)
        plotted_any = True

    if not plotted_any:
        plt.close(fig)
        print(f"  [skip] {sid}: all NaN")
        return None

    title = f"{sid} | {name}"
    if len(title) > 90:
        title = title[:87] + "..."
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Year")
    ax.set_ylabel(units or "value")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="best", fontsize=8, frameon=False)
    fig.tight_layout()
    out_path = OUT_DIR / f"{sid}.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    registry = load_registry()
    print(f"RMWND figure export -> {OUT_DIR}")
    generated = 0
    for sid in REPRESENTATIVE:
        out = plot_series(sid, registry)
        if out is not None:
            print(f"  wrote {out.name}")
            generated += 1
    print(f"Total: {generated}/{len(REPRESENTATIVE)} PNGs")


if __name__ == "__main__":
    main()

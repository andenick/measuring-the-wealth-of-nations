#!/usr/bin/env python3
"""AS2 NickyData v7.0 Pipeline — DAG-based orchestrator.

Usage:
    python -m pipeline.run              # Full pipeline
    python -m pipeline.run --fetch      # Fetch API data only
    python -m pipeline.run --compute    # Compute series only
    python -m pipeline.run --validate   # Validate only
    python -m pipeline.run --test       # Full + validation + checks
"""

import sys
import time
from pathlib import Path

# Add NickyData root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

VERSION = "7.0.0"


def _topological_sort(modules: list) -> list:
    """Sort compute modules by DEPENDS_ON declarations."""
    name_to_mod = {m.__name__.split(".")[-1]: m for m in modules}
    visited = set()
    order = []

    def visit(name):
        if name in visited:
            return
        visited.add(name)
        mod = name_to_mod.get(name)
        if mod:
            for dep in getattr(mod, "DEPENDS_ON", []):
                visit(dep)
        order.append(name)

    for name in name_to_mod:
        visit(name)

    return [name_to_mod[n] for n in order if n in name_to_mod]


def run_pipeline(fetch=True, compute=True, validate=True, output=True):
    """Execute the full pipeline."""
    from pipeline.sources.paths import ensure_dirs
    ensure_dirs()

    start = time.time()
    print(f"\n  AS2 NickyData v{VERSION} Pipeline")
    print(f"  {'=' * 40}")

    all_series = {}

    # Phase 1: Fetch API data
    if fetch:
        print("\n  -- Fetch Phase --")
        from pipeline.sources.api_fetch import fetch_all
        fetch_all()

    # Phase 2: Compute series
    if compute:
        print("\n  -- Compute Phase --")
        from pipeline.compute import revenue, employment, labor_shares, variable_capital, exploitation
        compute_modules = [revenue, employment, labor_shares, variable_capital, exploitation]
        sorted_modules = _topological_sort(compute_modules)

        for mod in sorted_modules:
            name = mod.__name__.split(".")[-1]
            try:
                result = mod.compute(all_series)
                all_series.update(result)
                for sid, df in result.items():
                    print(f"    {sid}: {len(df)} rows")
            except Exception as e:
                print(f"    {name}: FAIL - {e}")

    # Phase 3: Write series to disk
    if compute:
        from pipeline.sources.paths import BOOK_SERIES
        for sid, df in all_series.items():
            out_path = BOOK_SERIES / f"{sid}.csv"
            df.to_csv(out_path)

    # Phase 4: Validate
    if validate:
        print("\n  -- Validate Phase --")
        # TODO: run validation checks
        print("    (validation not yet implemented in v7.0)")

    elapsed = time.time() - start
    print(f"\n  Pipeline complete: {len(all_series)} series in {elapsed:.1f}s")
    return all_series


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AS2 NickyData v7.0")
    parser.add_argument("--fetch", action="store_true", help="Fetch API data only")
    parser.add_argument("--compute", action="store_true", help="Compute series only")
    parser.add_argument("--validate", action="store_true", help="Validate only")
    parser.add_argument("--test", action="store_true", help="Full pipeline + validation")
    args = parser.parse_args()

    if args.fetch:
        run_pipeline(fetch=True, compute=False, validate=False, output=False)
    elif args.compute:
        run_pipeline(fetch=False, compute=True, validate=False, output=False)
    elif args.validate:
        run_pipeline(fetch=False, compute=False, validate=True, output=False)
    else:
        run_pipeline()

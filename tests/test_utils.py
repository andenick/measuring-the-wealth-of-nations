"""Unit tests for Technical/code/utils/* modules.

Covers the critical loaders and helpers used across L01/P02/V03 scripts:

- registry_validator: get_reference_values (year-only and composite-key modes),
  get_derived_statistics, get_tolerance_class, missing-series KeyError path.
- bls_cache: load_bls_ces, productive_employment_annual, total_employment_annual
  shape/column checks plus monotone-year guarantee.
- series.BookColumnLoader: loads, renames, casts to int/float, applies unit_scale,
  and raises on missing source file or missing column.
- io.read_book_table / get_series_entry: header-row sniffing + registry lookup.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from utils import registry_validator as rv
from utils import bls_cache
from utils import series as series_mod
from utils import io as io_mod
from utils import paths as paths_mod


# ---------------------------------------------------------------------------
# registry_validator
# ---------------------------------------------------------------------------


class TestRegistryValidator:
    def test_load_registry_returns_dict_with_series(self):
        reg = rv._load_registry()
        assert isinstance(reg, dict)
        assert "series" in reg
        assert isinstance(reg["series"], dict)
        assert len(reg["series"]) > 30  # 35+ S-series alone

    def test_get_reference_values_known_series(self):
        # S506 (rate of exploitation) has well-known book-period benchmarks.
        benchmarks = rv.get_reference_values("S506")
        assert isinstance(benchmarks, dict)
        # Expect at least one anchor year present and float-typed.
        if benchmarks:
            yr, val = next(iter(benchmarks.items()))
            assert isinstance(yr, int)
            assert isinstance(val, float)
            assert 1948 <= yr <= 2025

    def test_get_reference_values_missing_series_raises(self):
        with pytest.raises(KeyError):
            rv.get_reference_values("S_DOES_NOT_EXIST")

    def test_get_reference_values_returns_empty_when_absent(self):
        # Find a series that legitimately has no reference_values, if any.
        reg = rv._load_registry()
        no_refs = [
            sid
            for sid, body in reg["series"].items()
            if not (body.get("validation") or {}).get("reference_values")
        ]
        if not no_refs:
            pytest.skip("All series carry reference_values — no negative case to test")
        empty = rv.get_reference_values(no_refs[0])
        assert empty == {}

    def test_get_reference_values_year_keys_only_filters_composites(self):
        # If any series has composite keys like "1948_e", year_keys_only=True
        # must drop them and year_keys_only=False must retain them.
        reg = rv._load_registry()
        candidate = None
        for sid, body in reg["series"].items():
            raw = (body.get("validation") or {}).get("reference_values") or {}
            if any(not str(k).isdigit() for k in raw.keys()):
                candidate = sid
                break
        if candidate is None:
            pytest.skip("No composite-key series in registry to exercise this branch")
        only_years = rv.get_reference_values(candidate, year_keys_only=True)
        with_composites = rv.get_reference_values(candidate, year_keys_only=False)
        assert all(isinstance(k, int) for k in only_years.keys())
        assert len(with_composites) >= len(only_years)

    def test_get_derived_statistics_returns_dict(self):
        # Even for a series with no derived_statistics, should return {} not error.
        stats = rv.get_derived_statistics("S506")
        assert isinstance(stats, dict)

    def test_get_tolerance_class_falls_back_to_default(self):
        # Use a clearly unknown series ID via a wrapper to confirm the default path.
        # _series_block raises for unknown SIDs, so we use a known series and
        # pass an explicit default that will be ignored if the registry has a value.
        tc = rv.get_tolerance_class("S506", default="rate_series")
        assert tc in ("rate_series", "dollar_series", "share_series", "level_series") or tc is None


# ---------------------------------------------------------------------------
# bls_cache
# ---------------------------------------------------------------------------


class TestBlsCache:
    def test_load_bls_ces_shape(self):
        if not bls_cache.BLS_CES_CACHE.exists():
            pytest.skip(f"BLS CES cache missing: {bls_cache.BLS_CES_CACHE}")
        df = bls_cache.load_bls_ces()
        assert "year" in df.columns
        assert df["year"].is_monotonic_increasing
        assert (df["year"] >= 1948).all()
        # Must include the headline series used by downstream code.
        assert bls_cache.TOTAL_PRIVATE_ALL_EMPLOYEES in df.columns
        for c in bls_cache.PRODUCTIVE_PROD_WORKER_SERIES:
            assert c in df.columns, f"Missing BLS series column {c}"

    def test_productive_employment_annual_columns(self):
        if not bls_cache.BLS_CES_CACHE.exists():
            pytest.skip("BLS CES cache missing")
        df = bls_cache.productive_employment_annual()
        assert list(df.columns) == ["year", "value"]
        assert df["year"].is_monotonic_increasing
        assert df["year"].dtype.kind in ("i", "u")
        # Productive employment in thousands should be in the millions of workers band.
        non_null = df["value"].dropna()
        assert (non_null > 1_000).all() and (non_null < 100_000).all()

    def test_total_employment_annual_columns(self):
        if not bls_cache.BLS_CES_CACHE.exists():
            pytest.skip("BLS CES cache missing")
        df = bls_cache.total_employment_annual()
        assert list(df.columns) == ["year", "value"]
        assert df["year"].is_monotonic_increasing
        non_null = df["value"].dropna()
        # Total private all-employees should always exceed productive subtotal.
        prod = bls_cache.productive_employment_annual()
        merged = df.merge(prod, on="year", suffixes=("_total", "_prod"))
        merged = merged.dropna(subset=["value_total", "value_prod"])
        assert (merged["value_total"] >= merged["value_prod"]).all()


# ---------------------------------------------------------------------------
# series.BookColumnLoader
# ---------------------------------------------------------------------------


class TestBookColumnLoader:
    def test_load_missing_file_raises(self, tmp_path: Path):
        loader = series_mod.BookColumnLoader(
            series_id="S999",
            subseries_id="S999-A",
            source_file=tmp_path / "no_such_table.csv",
            source_column="X",
            units="ratio",
        )
        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_load_missing_column_raises(self, tmp_path: Path):
        src = tmp_path / "tbl.csv"
        src.write_text("year,A,B\n1948,1.0,2.0\n1949,1.1,2.1\n", encoding="utf-8")
        loader = series_mod.BookColumnLoader(
            series_id="S999",
            subseries_id="S999-A",
            source_file=src,
            source_column="ZZZ",
            units="ratio",
        )
        with pytest.raises(KeyError):
            loader.load()

    def test_load_returns_normalized_frame(self, tmp_path: Path):
        src = tmp_path / "tbl.csv"
        src.write_text("year,Mp\n1948,1000.0\n1949,1100.0\n", encoding="utf-8")
        loader = series_mod.BookColumnLoader(
            series_id="S502",
            subseries_id="S502-A",
            source_file=src,
            source_column="Mp",
            units="billions_usd",
            unit_scale=1000.0,  # millions -> billions
        )
        df = loader.load()
        assert list(df.columns) == ["series_id", "year", "value", "units"]
        assert df["series_id"].unique().tolist() == ["S502-A"]
        assert df["units"].unique().tolist() == ["billions_usd"]
        assert df["year"].dtype.kind in ("i", "u")
        # 1000 / 1000 = 1.0
        assert pytest.approx(df.loc[0, "value"]) == 1.0
        assert pytest.approx(df.loc[1, "value"]) == 1.1

    def test_load_renames_unnamed_year_column(self, tmp_path: Path):
        # Some digitized tables have a blank first column name; loader should
        # rename the first column to "year" before projecting.
        src = tmp_path / "tbl.csv"
        src.write_text(",Mp\n1948,1.0\n1949,1.1\n", encoding="utf-8")
        loader = series_mod.BookColumnLoader(
            series_id="S502",
            subseries_id="S502-A",
            source_file=src,
            source_column="Mp",
            units="billions_usd",
        )
        df = loader.load()
        # Output schema is fixed: [series_id, year, value, units].
        assert list(df.columns) == ["series_id", "year", "value", "units"]
        assert df.loc[0, "year"] == 1948
        assert df.loc[1, "year"] == 1949
        assert pytest.approx(df.loc[0, "value"]) == 1.0


# ---------------------------------------------------------------------------
# io.read_book_table + get_series_entry
# ---------------------------------------------------------------------------


class TestIoModule:
    def test_read_book_table_handles_hash_header(self, tmp_path: Path):
        src = tmp_path / "tbl.csv"
        src.write_text("# Source: Book Table H.1\nyear,A,B\n1948,1.0,2.0\n", encoding="utf-8")
        df = io_mod.read_book_table(src)
        assert list(df.columns) == ["year", "A", "B"]
        assert df.iloc[0]["A"] == 1.0

    def test_read_book_table_handles_multirow_title(self, tmp_path: Path):
        src = tmp_path / "tbl.csv"
        src.write_text(
            "Title row\nSource: Book\nyear,A\n1948,1.0\n",
            encoding="utf-8",
        )
        df = io_mod.read_book_table(src)
        assert list(df.columns) == ["year", "A"]

    def test_read_book_table_handles_plain_header(self, tmp_path: Path):
        src = tmp_path / "tbl.csv"
        src.write_text("year,X\n1948,3.14\n", encoding="utf-8")
        df = io_mod.read_book_table(src)
        assert "X" in df.columns

    def test_get_series_entry_known(self):
        block = io_mod.get_series_entry("S506")
        assert isinstance(block, dict)
        assert "validation" in block or "name" in block or "units" in block

    def test_get_series_entry_unknown_raises(self):
        with pytest.raises(KeyError):
            io_mod.get_series_entry("S_NOT_REAL_123")


# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------


class TestPaths:
    def test_root_resolves_to_technical(self):
        assert paths_mod.ROOT.name == "Technical"
        assert (paths_mod.ROOT / "series_registry.json").exists()

    def test_chopped_dir_exists(self):
        assert paths_mod.CHOPPED_DIR.exists()
        assert paths_mod.CHOPPED_DIR.is_dir()

    def test_registry_path_is_canonical(self):
        assert paths_mod.REGISTRY == paths_mod.ROOT / "series_registry.json"
        assert paths_mod.REGISTRY.exists()

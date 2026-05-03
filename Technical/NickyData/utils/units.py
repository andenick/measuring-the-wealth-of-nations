"""Unit documentation and conversion for AS2 dollar-denominated series.

Per UNIT_AUDIT_REPORT.md (2026-04-09):
- T501-T503, T508-T509: billions (Table E.2)
- T504-T505: millions (Table 5.7, loaded via L02 ÷1000 from thousands)
- T601-T607: billions (Ch6 tables, loaded via L07 ÷1000 from thousands)
- T506, T507, T510-T514, T608-T609, T901: ratios (dimensionless)
- T515-T516: thousands (employment)
- BEA Fixed Assets: millions (UNIT_MULT=6)
- BEA NIPA 6.2D: millions (UNIT_MULT=6)
"""

SERIES_UNITS = {
    # Chapter 5 - Table E.2 aggregates (billions)
    "T501": {"unit": "billions", "source": "Table E.2", "type": "dollar"},
    "T502": {"unit": "billions", "source": "Table E.2", "type": "dollar"},
    "T503": {"unit": "billions", "source": "Table E.2", "type": "dollar"},
    "T508": {"unit": "billions", "source": "Table E.2", "type": "dollar"},
    "T509": {"unit": "billions", "source": "Table E.2", "type": "dollar"},

    # Chapter 5 - Table 5.7 labor measures (millions)
    "T504": {"unit": "millions", "source": "Table 5.7 via L02", "type": "dollar"},
    "T505": {"unit": "millions", "source": "Table 5.7 via L02", "type": "dollar"},

    # Chapter 5 - Ratios
    "T506": {"unit": "ratio", "source": "Table 5.7", "type": "ratio"},
    "T507": {"unit": "ratio", "source": "Table 5.7", "type": "ratio"},
    "T510": {"unit": "ratio", "source": "Table 5.7", "type": "ratio"},
    "T511": {"unit": "share", "source": "Table 5.7", "type": "ratio"},
    "T512": {"unit": "share", "source": "Table 5.7", "type": "ratio"},
    "T513": {"unit": "ratio", "source": "Table 5.11", "type": "ratio"},
    "T514": {"unit": "ratio", "source": "Table 5.11", "type": "ratio"},

    # Chapter 5 - Employment (thousands)
    "T515": {"unit": "thousands", "source": "BLS CES", "type": "employment"},
    "T516": {"unit": "thousands", "source": "BLS CES", "type": "employment"},

    # Chapter 6 - Dollar series (billions)
    "T601": {"unit": "billions", "source": "Table 6.1 via L07", "type": "dollar"},
    "T602": {"unit": "billions", "source": "Table 6.1 via L07", "type": "dollar"},
    "T603": {"unit": "billions", "source": "Table 6.1 via L07", "type": "dollar"},
    "T604": {"unit": "billions", "source": "Table 6.1 via L07", "type": "dollar"},
    "T605": {"unit": "billions", "source": "Table 6.2 via L08", "type": "dollar"},
    "T606": {"unit": "billions", "source": "Table 6.2 via L08", "type": "dollar"},
    "T607": {"unit": "billions", "source": "Derived (NSW)", "type": "dollar"},

    # Chapter 6 - Ratios
    "T608": {"unit": "ratio", "source": "Derived (NSW/V*)", "type": "ratio"},
    "T609": {"unit": "share", "source": "Derived (NSW/NI)", "type": "ratio"},

    # Chapter 9
    "T901": {"unit": "ratio", "source": "Assembled from Ch5+Ch6", "type": "ratio"},

    # External data
    "BEA_FIXED_ASSETS": {"unit": "millions", "source": "BEA Table 4.1", "type": "dollar"},
    "BEA_NIPA_6_2D": {"unit": "millions", "source": "BEA NIPA 6.2D", "type": "dollar"},
    "NAICS_GO": {"unit": "billions", "source": "BEA GDP-by-Industry", "type": "dollar"},
}


def get_unit(series_id: str) -> str:
    """Return the unit string for a series ID."""
    entry = SERIES_UNITS.get(series_id)
    if entry:
        return entry["unit"]
    return "unknown"


def is_dollar_series(series_id: str) -> bool:
    """Check if a series is dollar-denominated."""
    entry = SERIES_UNITS.get(series_id)
    return entry is not None and entry.get("type") == "dollar"


def assert_compatible(sid_a: str, sid_b: str) -> None:
    """Raise ValueError if two series have incompatible units for arithmetic."""
    unit_a = get_unit(sid_a)
    unit_b = get_unit(sid_b)

    if unit_a == "unknown" or unit_b == "unknown":
        return  # Can't check unknown units

    if unit_a != unit_b:
        raise ValueError(
            f"Unit mismatch: {sid_a} ({unit_a}) vs {sid_b} ({unit_b}). "
            f"Cannot perform arithmetic across different unit bases. "
            f"See UNIT_AUDIT_REPORT.md."
        )


def conversion_factor(from_unit: str, to_unit: str) -> float:
    """Return the multiplication factor to convert between units."""
    factors = {
        ("millions", "billions"): 1e-3,
        ("billions", "millions"): 1e3,
        ("thousands", "millions"): 1e-3,
        ("millions", "thousands"): 1e3,
        ("thousands", "billions"): 1e-6,
        ("billions", "thousands"): 1e6,
    }
    if from_unit == to_unit:
        return 1.0
    return factors.get((from_unit, to_unit), float("nan"))

"""BLS CES employment and wage data fetcher.

Fetches production worker counts, wages, and hours by sector via FRED mirrors.
Implements the data requirements of Appendix G (sector-by-sector V* computation).
"""

import pandas as pd
from .fred import fetch


# Production worker counts (CES*0006) and total employees (CES*0001)
WORKER_COUNT_SERIES = {
    "manufacturing": {"production": "CES3000000006", "total": "MANEMP"},
    "mining": {"production": "CES1000000006", "total": "CES1000000001"},
    "construction": {"production": "CES2000000006", "total": "CES2000000001"},
}

# Production worker earnings (CES*0008) and hours (CES*0007)
EARNINGS_SERIES = {
    "manufacturing": {"earnings": "CES3000000008", "hours": "CES3000000007"},
    "mining": {"earnings": "CES1000000008", "hours": "CES1000000007"},
    "construction": {"earnings": "CES2000000008", "hours": "CES2000000007"},
    "total_private": {"earnings": "CES0500000008", "hours": "CES0500000007"},
}

# Broad sector employment totals
EMPLOYMENT_SERIES = {
    "total_nonfarm": "PAYEMS",
    "trade": "USTRADE",
    "fire": "CEU5500000001",
    "government": "CEU9000000001",
}

# Default production worker fractions (used where BLS data unavailable)
DEFAULT_PW_RATIOS = {
    "agriculture": 0.71,
    "transport": 0.83,
    "utilities": 0.80,
    "services": 0.587,  # GNP ratio from Table F.1 (1989)
    "govt_enterprises": 0.73,
}


def fetch_production_worker_ratios(api_key: str) -> pd.DataFrame:
    """Fetch production/total worker ratios for sectors with BLS data."""
    ratios = {}
    for sector, series in WORKER_COUNT_SERIES.items():
        try:
            prod = fetch(series["production"], api_key, start="1948-01-01", min_year=1948)
            total = fetch(series["total"], api_key, start="1948-01-01", min_year=1948)
            common = prod.index.intersection(total.index)
            valid = common[total[common] > 0]
            ratios[sector] = prod[valid] / total[valid]
        except Exception:
            pass
    return pd.DataFrame(ratios) if ratios else pd.DataFrame()


def fetch_production_worker_wages(api_key: str) -> pd.DataFrame:
    """Fetch annual production worker wages by sector.

    Computes: annual_wage = hourly_earnings × weekly_hours × 52
    Returns DataFrame indexed by year with columns per sector.
    """
    wages = {}
    for sector, series in EARNINGS_SERIES.items():
        try:
            earnings = fetch(series["earnings"], api_key, start="1948-01-01", min_year=1948)
            hours = fetch(series["hours"], api_key, start="1948-01-01", min_year=1948)
            common = earnings.index.intersection(hours.index)
            if len(common) > 0:
                wages[sector] = earnings[common] * hours[common] * 52
        except Exception:
            pass
    return pd.DataFrame(wages) if wages else pd.DataFrame()


def fetch_production_worker_counts(api_key: str) -> pd.DataFrame:
    """Fetch production worker counts (thousands) by sector."""
    counts = {}
    for sector, series in WORKER_COUNT_SERIES.items():
        try:
            counts[sector] = fetch(series["production"], api_key, start="1948-01-01", min_year=1948)
        except Exception:
            pass
    return pd.DataFrame(counts) if counts else pd.DataFrame()


def fetch_employment_by_sector(api_key: str) -> pd.DataFrame:
    """Fetch total employment by broad sector."""
    result = {}
    for name, series_id in EMPLOYMENT_SERIES.items():
        try:
            result[name] = fetch(series_id, api_key, start="1948-01-01", min_year=1948)
        except Exception:
            pass
    return pd.DataFrame(result) if result else pd.DataFrame()

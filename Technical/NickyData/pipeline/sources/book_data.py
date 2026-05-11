"""Read all book-period source data.

Pure readers — no API calls, no computation, no side effects.
Each function returns a DataFrame indexed by year.
"""

import pandas as pd
from .paths import BOOK_SERIES, ST_CHOPPED


def load_table_h1() -> pd.DataFrame:
    """42-year annual data from digitized Table H.1 (1948-1989).

    Columns: S_star, VA_star, V_star, S_star_V_star, SP_star, FP_star,
             GFP_star, TP_star, Mp, Dp, P_plus, VA_NNP, EC, P_plus_EC
    Units: billions of current dollars (except ratios).
    """
    path = BOOK_SERIES / "book_tableH1_1948_1989.csv"
    return pd.read_csv(path, comment="#", index_col="year")


def load_key_ratios() -> pd.DataFrame:
    """42-year T511 (Lp/L) and T512 (V*/W) from Table 5.7."""
    path = ST_CHOPPED / "ch05" / "Table5_7_KeyRatios.csv"
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_employment() -> pd.DataFrame:
    """42-year T515 (Lp) and T516 (Lu) in thousands."""
    path = ST_CHOPPED / "ch05" / "Employment_1948_1989.csv"
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_revenue_accounts() -> pd.DataFrame:
    """Book-period TP*, C*m, GFP*, CON*, IG* from Table E.2."""
    path = ST_CHOPPED / "ch05" / "TableE2_RevenueAccounts.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_tax_accounts() -> pd.DataFrame:
    """38-year T601-T604 from Table 6.1 (1952-1989, millions)."""
    path = ST_CHOPPED / "ch06" / "Table6_1_TaxAccounts.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_benefit_accounts() -> pd.DataFrame:
    """38-year T605-T606 from Table 6.2 (1952-1989, millions)."""
    path = ST_CHOPPED / "ch06" / "Table6_2_BenefitAccounts.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_nsw() -> pd.DataFrame:
    """74-year NSW from Table 6.3 (1952-2025)."""
    for fname in ["Table6_3_Extended.csv", "Table6_3_NetSocialWage.csv"]:
        path = ST_CHOPPED / "ch06" / fname
        if path.exists():
            df = pd.read_csv(path, skiprows=1, index_col=0)
            df.index.name = "year"
            return df
    return pd.DataFrame()


def load_profit_rates() -> pd.DataFrame:
    """42-year T513, T514 from ProfitRates (1948-1989, percentages)."""
    path = ST_CHOPPED / "ch05" / "ProfitRates_1948_1989.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_composition() -> pd.DataFrame:
    """42-year T507, T510 from ExploitationComposition (1948-1989)."""
    path = ST_CHOPPED / "ch05" / "ExploitationComposition_1948_1989.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_summary() -> pd.DataFrame:
    """42-year T901 from Table 9.1."""
    path = ST_CHOPPED / "ch09" / "Table9_1_SummaryIndicators.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, skiprows=1, index_col=0)
    df.index.name = "year"
    return df


def load_mohun_exploitation() -> pd.DataFrame:
    """Mohun exploitation rates for cross-validation."""
    path = ST_CHOPPED.parent / "ExternalSources" / "Mohun" / "mohun_exploitation_rates_1948_1989_CORRECTED.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, index_col=0)

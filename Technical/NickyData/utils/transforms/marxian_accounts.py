"""Marxian national accounting formulas from Shaikh & Tonak (1994).

Implements the core accounting identities used in Chapters 5 and 6:
  TP* = productive + trading sector gross output
  C*_m = material constant capital (intermediate inputs)
  GFP = TP* - C*_m  (gross final product)
  V* = variable capital (productive worker compensation)
  S* = GFP - V*  (surplus value)
  e = S* / V*  (rate of exploitation)
  r* = S* / (C* + V*)  (Marxian profit rate)
  NSW = B_w + G_w - T_w  (net social wage)
"""

from __future__ import annotations

import pandas as pd


def compute_gfp(tp_star: pd.Series, c_star_m: pd.Series) -> pd.Series:
    """GFP = TP* - C*_m."""
    common = tp_star.index.intersection(c_star_m.index)
    return tp_star.reindex(common) - c_star_m.reindex(common)


def compute_surplus_value(gfp: pd.Series, v_star: pd.Series) -> pd.Series:
    """S* = GFP - V*."""
    common = gfp.index.intersection(v_star.index)
    return gfp.reindex(common) - v_star.reindex(common)


def compute_exploitation_rate(s_star: pd.Series, v_star: pd.Series) -> pd.Series:
    """e = S* / V*."""
    common = s_star.index.intersection(v_star.index)
    v = v_star.reindex(common)
    return s_star.reindex(common) / v.replace(0, float("nan"))


def compute_exploitation_from_wage_share(
    v_star_over_w: pd.Series,
    va_star_over_w: "pd.Series | float" = 1.238,
) -> pd.Series:
    """e = (VA*/W) / (V*/W) - 1.

    Parameters
    ----------
    v_star_over_w : pd.Series
        Productive wage share (V*/W) by year.
    va_star_over_w : pd.Series or float
        Productive value-added ratio (VA*/W) by year or constant.
        Default 1.238 is the 1989 value (DIV-002).
        Pass a year-indexed Series for year-varying computation.
    """
    denom = v_star_over_w.replace(0, float("nan"))
    if isinstance(va_star_over_w, pd.Series):
        common = denom.index.intersection(va_star_over_w.index)
        return va_star_over_w.reindex(common) / denom.reindex(common) - 1
    return va_star_over_w / denom - 1


def compute_profit_rate(
    s_star: pd.Series,
    c_star: pd.Series,
    v_star: pd.Series,
) -> pd.Series:
    """r* = S* / (C* + V*)."""
    common = s_star.index.intersection(c_star.index).intersection(v_star.index)
    denominator = c_star.reindex(common) + v_star.reindex(common)
    return s_star.reindex(common) / denominator.replace(0, float("nan"))


def compute_adjusted_profit_rate(
    r_star: pd.Series,
    tcu: pd.Series,
) -> pd.Series:
    """r*_adj = r* / TCU (capacity-adjusted profit rate)."""
    common = r_star.index.intersection(tcu.index)
    tcu_safe = tcu.reindex(common).replace(0, float("nan"))
    return r_star.reindex(common) / tcu_safe


def compute_nsw(
    benefits_w: pd.Series,
    govt_services_w: pd.Series,
    taxes_w: pd.Series,
) -> pd.Series:
    """NSW = B_w + G_w - T_w (net social wage)."""
    common = benefits_w.index.intersection(govt_services_w.index).intersection(taxes_w.index)
    return (
        benefits_w.reindex(common)
        + govt_services_w.reindex(common)
        - taxes_w.reindex(common)
    )


def compute_variable_capital(
    total_compensation: pd.Series,
    wage_share: pd.Series,
) -> pd.Series:
    """V* = W * (V*/W) where V*/W is the productive wage share."""
    common = total_compensation.index.intersection(wage_share.index)
    return total_compensation.reindex(common) * wage_share.reindex(common)

"""
WEEK 7B: Calculate Variable Capital (Mohun Methodology)

This script calculates V*_mohun following Mohun (2005, 2013) methodology.

METHODOLOGICAL FIDELITY TO MOHUN:
V*_mohun = Wp_mohun (wages of productive workers)

NO consumption baskets, NO sector-specific labor value weighting.

This is the SAME approach as Shaikh-Tonak (1994) Chapter 5,
but applied to Mohun's classification of productive workers.

Theoretical justification (ST 1994, p. 113; Mohun 2005, eq. 6):
- Approximation: CONWp ≈ Wp (consumption ≈ wages)
- Savings offset by dissaving across workers
- Simple wage approximation captures variable capital in money terms

Key difference from ST:
- Mohun classifies more workers as productive (Information sector)
- Therefore Wp_mohun > Wp_ST
- Expected: V*_mohun ≈ 1.10-1.15 × V*_ST

Data sources:
- Lp_mohun: From calculate_employment_mohun.py
- NIPA wages: BEA compensation data by industry
- BLS production worker wages: For wage adjustment

Author: Shaikh-Tonak Replication Project
Date: October 31, 2025
Phase: Week 7B - Mohun Extension
"""

import pandas as pd
import numpy as np
from pathlib import Path


class MohunVariableCapitalCalculator:
    """
    Calculate variable capital following Mohun methodology.

    Formula: V*_mohun = Wp_mohun (simple wage approximation)

    Variables:
    - Lp_mohun: Productive employment (thousands)
    - ec_mohun: Employee compensation per worker ($/worker)
    - Wp_mohun: Total wages of productive workers ($)
    - V*_mohun: Variable capital in money terms ($)

    NO consumption basket calculations, NO labor value weighting
    """

    def __init__(self, start_year=1948, end_year=1989):
        self.start_year = start_year
        self.end_year = end_year
        self.years = list(range(start_year, end_year + 1))

        print("\n" + "=" * 80)
        print("WEEK 7B: MOHUN VARIABLE CAPITAL CALCULATION (V*_mohun)")
        print("=" * 80)
        print(f"\nPeriod: {start_year}-{end_year} ({len(self.years)} years)")
        print(f"Methodology: Mohun (2005, 2013) - V* = Wp (simple approximation)")
        print(f"NO consumption baskets, NO labor value weighting")
        print("=" * 80)

    def load_data(self):
        """Load necessary data files."""

        print(f"\n[Step 1] Loading data...")

        # Load Mohun productive employment
        mohun_emp_file = Path("data/Mohun/mohun_employment_by_industry_1948_1989.csv")
        self.mohun_emp = pd.read_csv(mohun_emp_file)
        print(f"\n[OK] Loaded Mohun employment by industry: {len(self.mohun_emp)} observations")

        # Load NIPA data for wages
        nipa_file = Path("data/NIPA_Book_Period/nipa_1948_1989.parquet")
        self.nipa_df = pd.read_parquet(nipa_file)
        print(f"\n[OK] Loaded NIPA data: {len(self.nipa_df)} observations")

        # Standardize column names
        comp_col = [c for c in self.nipa_df.columns if 'compensation' in c.lower()][0]
        self.nipa_df = self.nipa_df.rename(columns={comp_col: 'compensation'})

        print(f"  Using compensation column: '{comp_col}'")

    def explain_methodology(self):
        """Explain the simple V* = Wp approximation."""

        print(f"\n[Step 2] Mohun Methodology for Variable Capital")

        print(f"\n  Formula: V*_mohun = Wp_mohun")
        print(f"  Where Wp_mohun = Total wages of productive workers")

        print(f"\n  Theoretical justification (Mohun 2005, Shaikh-Tonak 1994):")
        print(f"    - Variable capital represents value of labor-power")
        print(f"    - Approximation: Workers' consumption ~= Workers' wages")
        print(f"    - Savings of some offset by dissaving of others")
        print(f"    - Therefore: V* ~= Wp in money magnitudes")

        print(f"\n  What we do NOT do (contrary to initial plan):")
        print(f"    - X NO consumption basket calculations")
        print(f"    - X NO sector-specific labor values")
        print(f"    - X NO BEA PCE weighting")
        print(f"    - This is faithful to BOTH Shaikh-Tonak AND Mohun")

        print(f"\n  Calculation steps:")
        print(f"    1. Load Lp_mohun by industry-year")
        print(f"    2. Load compensation per worker (ec) by industry-year from NIPA")
        print(f"    3. Calculate: Wp_i = Lp_mohun_i * ec_i")
        print(f"    4. Sum: Wp_mohun = Sum(Wp_i)")
        print(f"    5. V*_mohun = Wp_mohun")

    def calculate_wages_productive_workers(self):
        """
        Calculate wages of productive workers (Wp_mohun).

        Methodology:
        1. Merge Lp_mohun with NIPA compensation data
        2. Calculate Wp_i = Lp_mohun_i * (compensation_i / employment_i)
        3. Sum across industries
        """

        print(f"\n[Step 3] Calculating Wp_mohun...")

        # Merge Mohun employment with NIPA compensation
        merged = self.mohun_emp.merge(
            self.nipa_df[['year', 'industry', 'compensation', 'employment']],
            on=['year', 'industry'],
            how='left',
            suffixes=('_mohun', '_nipa')
        )

        print(f"\n  [Status] Merge results:")
        print(f"    Total observations: {len(merged)}")
        print(f"    Missing compensation: {merged['compensation'].isna().sum()}")
        print(f"    Missing employment_nipa: {merged['employment_nipa'].isna().sum()}")

        # Calculate compensation per worker (ec)
        merged['ec'] = merged['compensation'] / merged['employment_nipa']

        # Calculate wages of productive workers by industry
        # Wp_i = Lp_mohun_i * ec_i
        merged['Wp_ind'] = merged['Lp_mohun'] * merged['ec']

        print(f"\n  [Calculation] Wp by industry:")
        print(f"    Formula: Wp_i = Lp_mohun_i × (compensation_i / employment_i)")
        print(f"    Where:")
        print(f"      - Lp_mohun_i: Productive employment in industry i (thousands)")
        print(f"      - ec_i: Employee compensation per worker in industry i ($/worker)")

        # Save industry-level detail
        self.Wp_by_industry = merged[['year', 'industry', 'Lp_mohun', 'compensation',
                                       'employment_nipa', 'ec', 'Wp_ind']].copy()

        # Aggregate to annual Wp_mohun
        self.Wp_mohun_annual = merged.groupby('year')['Wp_ind'].sum().reset_index()
        self.Wp_mohun_annual.columns = ['year', 'Wp_mohun']

        # V*_mohun = Wp_mohun (simple approximation)
        self.Wp_mohun_annual['V_star_mohun'] = self.Wp_mohun_annual['Wp_mohun']

        print(f"\n[Results] Variable capital (V*_mohun):")
        print(f"  1948: ${self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1948]['V_star_mohun'].iloc[0]:,.0f}")
        print(f"  1989: ${self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1989]['V_star_mohun'].iloc[0]:,.0f}")

        # Growth rate
        V_1948 = self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1948]['V_star_mohun'].iloc[0]
        V_1989 = self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1989]['V_star_mohun'].iloc[0]
        growth_rate = ((V_1989 / V_1948) ** (1/41) - 1) * 100

        print(f"  Annual growth rate: {growth_rate:.2f}%")

    def compare_with_st(self):
        """Compare V*_mohun with V*_ST (Shaikh-Tonak)."""

        print(f"\n[Step 4] Comparing with Shaikh-Tonak...")

        # Load ST variable capital
        st_file = Path("data/Variable_Capital/variable_capital_annual_1948_1989.csv")
        if st_file.exists():
            self.st_vc = pd.read_csv(st_file)

            # Merge with Mohun results
            comparison = self.Wp_mohun_annual.merge(
                self.st_vc[['year', 'Wp', 'V_star']],
                on='year',
                how='left'
            )

            # Calculate differences
            comparison['Wp_difference'] = comparison['Wp_mohun'] - comparison['Wp']
            comparison['Wp_diff_pct'] = (comparison['Wp_difference'] / comparison['Wp']) * 100

            comparison['V_star_difference'] = comparison['V_star_mohun'] - comparison['V_star']
            comparison['V_star_diff_pct'] = (comparison['V_star_difference'] / comparison['V_star']) * 100

            # Display key years
            key_years = [1948, 1958, 1968, 1978, 1989]
            comp_display = comparison[comparison['year'].isin(key_years)]

            print(f"\n  Comparison: Mohun vs Shaikh-Tonak (Key Years)")
            print(f"  {'-' * 90}")
            print(f"  {'Year':>6} {'V*_ST':>15} {'V*_Mohun':>15} {'Diff':>15} {'Diff %':>10}")
            print(f"  {'-' * 90}")
            for _, row in comp_display.iterrows():
                print(f"  {row['year']:>6.0f} ${row['V_star']:>14,.0f} ${row['V_star_mohun']:>14,.0f} ${row['V_star_difference']:>14,.0f} {row['V_star_diff_pct']:>9.1f}%")
            print(f"  {'-' * 90}")

            # Analysis
            avg_diff_pct = comparison['V_star_diff_pct'].mean()
            print(f"\n  Average difference: {avg_diff_pct:.1f}%")
            print(f"  Interpretation: Mohun's V* is {'higher' if avg_diff_pct > 0 else 'lower'} than ST")
            print(f"  Reason: Mohun classifies more workers as productive (Information sector)")

            print(f"\n  Note on ST calculation:")
            print(f"    - ST reports both Wp and V_star (with lambda_wage_goods)")
            print(f"    - For money magnitudes: V* = Wp (approximation)")
            print(f"    - V_star column uses labor value conversion (theoretical check)")
            print(f"    - Mohun uses V*_mohun = Wp_mohun directly")

            self.comparison = comparison
        else:
            print(f"\n  [WARNING] ST variable capital file not found: {st_file}")
            print(f"  Skipping comparison.")

    def calculate_per_worker_metrics(self):
        """Calculate V* per productive worker."""

        print(f"\n[Step 5] Calculating per-worker metrics...")

        # Load Lp_mohun annual
        mohun_emp_annual = pd.read_csv("data/Mohun/mohun_employment_annual_1948_1989.csv")

        # Merge with V*_mohun
        self.Wp_mohun_annual = self.Wp_mohun_annual.merge(
            mohun_emp_annual[['year', 'Lp_mohun']],
            on='year',
            how='left'
        )

        # Calculate V* per productive worker
        self.Wp_mohun_annual['V_star_per_worker'] = (
            self.Wp_mohun_annual['V_star_mohun'] / self.Wp_mohun_annual['Lp_mohun']
        )

        print(f"\n[Results] V* per productive worker:")
        print(f"  1948: ${self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1948]['V_star_per_worker'].iloc[0]:,.0f}")
        print(f"  1989: ${self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1989]['V_star_per_worker'].iloc[0]:,.0f}")

        # Growth rate
        V_pw_1948 = self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1948]['V_star_per_worker'].iloc[0]
        V_pw_1989 = self.Wp_mohun_annual[self.Wp_mohun_annual['year'] == 1989]['V_star_per_worker'].iloc[0]
        growth_rate = ((V_pw_1989 / V_pw_1948) ** (1/41) - 1) * 100

        print(f"  Annual growth rate: {growth_rate:.2f}%")

    def save_results(self):
        """Save variable capital results."""

        print(f"\n[Step 6] Saving results...")

        # Create output directory
        output_dir = Path("data/Mohun")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save annual V*_mohun
        annual_file = output_dir / "mohun_variable_capital_1948_1989.csv"
        output_cols = ['year', 'Wp_mohun', 'V_star_mohun', 'Lp_mohun', 'V_star_per_worker']
        self.Wp_mohun_annual[output_cols].to_csv(annual_file, index=False)
        print(f"\n[OK] Saved annual V*_mohun: {annual_file}")
        print(f"  {len(self.Wp_mohun_annual)} observations (42 years)")
        print(f"  Columns: year, Wp_mohun, V_star_mohun, Lp_mohun, V_star_per_worker")

        # Save industry-level Wp
        industry_file = output_dir / "mohun_wages_productive_by_industry.csv"
        self.Wp_by_industry.to_csv(industry_file, index=False)
        print(f"\n[OK] Saved industry-level Wp: {industry_file}")
        print(f"  {len(self.Wp_by_industry)} observations (13 industries x 42 years)")

        # Save comparison if available
        if hasattr(self, 'comparison'):
            comparison_file = output_dir / "mohun_vs_st_variable_capital_comparison.csv"
            self.comparison.to_csv(comparison_file, index=False)
            print(f"\n[OK] Saved ST vs Mohun V* comparison: {comparison_file}")

        print("\n" + "=" * 80)
        print("WEEK 7B STEP 3 COMPLETE: Variable capital calculation finished")
        print("=" * 80)
        print(f"\nMethodological Notes:")
        print(f"  - V*_mohun = Wp_mohun (simple wage approximation)")
        print(f"  - NO consumption baskets (faithful to Mohun 2005, 2013)")
        print(f"  - NO sector-specific labor values (faithful to ST 1994 Chapter 5)")
        print(f"  - Uses NIPA employee compensation by industry")
        print(f"\nOutputs:")
        print(f"  1. {annual_file}")
        print(f"  2. {industry_file}")
        if hasattr(self, 'comparison'):
            print(f"  3. {comparison_file}")
        print(f"\nNext: calculate_exploitation_mohun.py (conservation principle)")

    def run(self):
        """Execute full variable capital calculation pipeline."""
        self.load_data()
        self.explain_methodology()
        self.calculate_wages_productive_workers()
        self.compare_with_st()
        self.calculate_per_worker_metrics()
        self.save_results()


if __name__ == "__main__":
    calculator = MohunVariableCapitalCalculator(start_year=1948, end_year=1989)
    calculator.run()

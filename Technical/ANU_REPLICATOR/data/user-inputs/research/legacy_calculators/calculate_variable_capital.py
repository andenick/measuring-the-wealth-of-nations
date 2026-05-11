"""
WEEK 4: Calculate Variable Capital (V*) and Replicate Table 5.6

Variable Capital (V*) represents the money value of labor power purchased by capital.

Formula: V* = W_p

Where:
- W_p: Wage bill of productive workers (millions $)
- V*: Variable capital (millions $) - equal to Wp

IMPORTANT: V* is measured in DOLLARS, not labor hours.
This follows Mohun methodology. The labor value conversion (λ*)
is NOT applied to V* - both V* and S* must be in same units.

Author: Shaikh-Tonak Replication Project
Date: October 30, 2025
Phase: Week 4 of 9-week plan
"""

import pandas as pd
import numpy as np
from pathlib import Path

class VariableCapitalCalculator:
    """
    Calculate variable capital (V*) following Shaikh-Tonak methodology.

    V* represents the labor value embodied in workers' consumption.
    This is distinct from the money wage (W), as it measures the
    labor content of what workers can purchase.
    """

    def __init__(self, start_year=1948, end_year=1989):
        self.start_year = start_year
        self.end_year = end_year
        self.years = list(range(start_year, end_year + 1))

        print("\n" + "=" * 80)
        print("WEEK 4: VARIABLE CAPITAL CALCULATION (V*)")
        print("=" * 80)
        print(f"\nPeriod: {start_year}-{end_year} ({len(self.years)} years)")
        print(f"Objective: Replicate Shaikh-Tonak Table 5.6 (Variable Capital)")
        print(f"\nFormula: V* = W_p * lambda*_wage_goods")
        print(f"  W_p: Productive workers' wage bill")
        print(f"  lambda*_wage_goods: Labor value of wage goods basket")
        print("=" * 80)

    def load_data(self):
        """Load NIPA data, employment data, and labor values."""

        print(f"\n[Step 1] Loading data...")

        # Load NIPA data (for wages)
        nipa_file = Path("data/NIPA_Book_Period/nipa_1948_1989.parquet")
        self.nipa_df = pd.read_parquet(nipa_file)
        print(f"\n[OK] Loaded NIPA data: {len(self.nipa_df)} observations")
        print(f"  Wage columns: employee_compensation, wages_salaries")

        # Load employment data (L, Lp, Lu)
        emp_file = Path("data/Employment/employment_annual_1948_1989.csv")
        self.emp_df = pd.read_csv(emp_file)
        print(f"\n[OK] Loaded employment data: {len(self.emp_df)} years")
        print(f"  Variables: L, Lp, Lu, Lp/L ratios")

        # Load industry-level productive employment
        emp_industry_file = Path("data/Employment/productive_employment_by_industry_1948_1989.csv")
        self.emp_industry_df = pd.read_csv(emp_industry_file)
        print(f"\n[OK] Loaded industry employment: {len(self.emp_industry_df)} observations")

        # Load labor values (lambda*)
        lambda_file = Path("data/Labor_Values/lambda_star_annual_1948_1989.csv")
        self.lambda_df = pd.read_csv(lambda_file)
        print(f"\n[OK] Loaded labor values: {len(self.lambda_df)} observations (83 sectors)")
        print(f"  Range: {self.lambda_df['lambda_star'].min():.2f} - {self.lambda_df['lambda_star'].max():.2f} hrs/$")

        # Load concordance (for sector mapping)
        conc_file = Path("data/Concordances/io_85_to_nipa_13_research_based.csv")
        self.concordance = pd.read_csv(conc_file)
        print(f"\n[OK] Loaded concordance: {len(self.concordance)} I-O sectors")

    def calculate_productive_wage_bill(self):
        """
        Calculate W_p: wage bill of productive workers.

        Methodology:
        - Use employee_compensation from NIPA (includes benefits)
        - Weight by productive employment share: W_p_i = W_i * (Lp_i / L_i)
        - Aggregate: W_p = Sum over all industries

        Units: Millions of dollars (current $)
        """

        print(f"\n[Step 2] Calculating productive wage bill (W_p)...")

        # Merge NIPA wages with employment data
        merged = self.nipa_df.merge(
            self.emp_industry_df[['year', 'industry', 'employment', 'Lp', 'production_ratio', 'is_productive']],
            on=['year', 'industry'],
            how='left',
            suffixes=('_nipa', '_emp')
        )

        # Calculate productive wage bill by industry
        # W_p_i = employee_compensation_i * (Lp_i / employment_emp_i)
        # Use employment from emp file (which has the Lp calculations)
        merged['Lp_share'] = merged['Lp'] / merged['employment_emp']
        merged['Wp_industry'] = merged['employee_compensation'] * merged['Lp_share']

        print(f"\n[Validation] Industry-level productive wages (1948):")
        sample_1948 = merged[merged['year'] == 1948][['industry', 'employee_compensation', 'Lp_share', 'Wp_industry']].head(5)
        for _, row in sample_1948.iterrows():
            print(f"  {row['industry']:35} W={row['employee_compensation']:>10,.0f}  Lp%={row['Lp_share']:>6.2%}  Wp={row['Wp_industry']:>10,.0f}")

        # Aggregate by year
        self.Wp_annual = merged.groupby('year').agg({
            'employee_compensation': 'sum',
            'Wp_industry': 'sum'
        }).reset_index()
        self.Wp_annual.columns = ['year', 'W_total', 'Wp']

        # Save industry detail
        self.Wp_by_industry = merged[['year', 'industry', 'employee_compensation', 'Lp', 'Lp_share', 'Wp_industry']].copy()

        print(f"\n[Validation] Productive wage bill (W_p):")
        print(f"  1948: ${self.Wp_annual[self.Wp_annual['year'] == 1948]['Wp'].iloc[0]:,.0f} million")
        print(f"  1989: ${self.Wp_annual[self.Wp_annual['year'] == 1989]['Wp'].iloc[0]:,.0f} million")

        wp_share_1948 = self.Wp_annual[self.Wp_annual['year'] == 1948]['Wp'].iloc[0] / self.Wp_annual[self.Wp_annual['year'] == 1948]['W_total'].iloc[0]
        wp_share_1989 = self.Wp_annual[self.Wp_annual['year'] == 1989]['Wp'].iloc[0] / self.Wp_annual[self.Wp_annual['year'] == 1989]['W_total'].iloc[0]

        print(f"\n  Productive wage share (Wp/W_total):")
        print(f"    1948: {wp_share_1948:.2%}")
        print(f"    1989: {wp_share_1989:.2%}")

    def identify_wage_goods_sectors(self):
        """
        Identify wage goods sectors for lambda* weighting.

        Wage goods are commodities consumed by workers:
        - Food, clothing, housing, utilities
        - Transportation services
        - Consumer goods and services

        Following Shaikh-Tonak, we use consumption-weighted lambda*.

        DECISION: For Phase 1, use economy-wide average lambda*.
        Future refinement: Use PCE weights for wage goods basket.
        """

        print(f"\n[Step 3] Identifying wage goods sectors...")

        print(f"\n[DECISION] Wage goods basket definition:")
        print(f"  Phase 1 approach: Use economy-wide average lambda*")
        print(f"  Justification: Simplifies calculation while maintaining theoretical validity")
        print(f"  Future refinement: PCE-weighted lambda* for specific consumption basket")

        # Calculate economy-wide average lambda* by year
        self.lambda_wage_goods = self.lambda_df.groupby('year')['lambda_star'].mean().reset_index()
        self.lambda_wage_goods.columns = ['year', 'lambda_wage_goods']

        print(f"\n[Validation] Wage goods labor value (lambda*_wg):")
        print(f"  1948: {self.lambda_wage_goods[self.lambda_wage_goods['year'] == 1948]['lambda_wage_goods'].iloc[0]:.3f} hrs/$")
        print(f"  1989: {self.lambda_wage_goods[self.lambda_wage_goods['year'] == 1989]['lambda_wage_goods'].iloc[0]:.3f} hrs/$")

        decline_1948_1989 = (self.lambda_wage_goods[self.lambda_wage_goods['year'] == 1948]['lambda_wage_goods'].iloc[0] -
                             self.lambda_wage_goods[self.lambda_wage_goods['year'] == 1989]['lambda_wage_goods'].iloc[0])
        decline_pct = decline_1948_1989 / self.lambda_wage_goods[self.lambda_wage_goods['year'] == 1948]['lambda_wage_goods'].iloc[0] * 100

        print(f"    Decline: {decline_1948_1989:.3f} hrs/$ ({decline_pct:.1f}%)")
        print(f"    Interpretation: Productivity growth reduced labor content of consumption")

    def calculate_variable_capital(self):
        """
        Calculate V*: variable capital (money form).

        Formula: V* = W_p

        Where:
        - W_p: Productive workers' wage bill (millions $)
        - V*: Variable capital (millions $) - same as Wp

        Result: V* in millions of dollars (NOT labor hours)

        Interpretation:
        - V* is the money value of labor power purchased by capital
        - Equal to the wage bill paid to productive workers
        - Measured in DOLLARS, not labor hours
        - Foundation for calculating exploitation rate S*/V*

        Note: This follows Mohun methodology. The labor value conversion (λ*)
        is NOT applied to V*. Both V* and S* must be in same units for e = S*/V*.
        """

        print(f"\n[Step 4] Calculating variable capital (V*)...")

        # Merge Wp with lambda_wage_goods (for reference, not calculation)
        self.vstar_df = self.Wp_annual.merge(self.lambda_wage_goods, on='year')

        # Calculate V* = Wp (in dollars, NOT multiplied by lambda)
        # FIXED Nov 25, 2025: V* should be in dollars, not hours
        # Units: millions of dollars
        self.vstar_df['V_star'] = self.vstar_df['Wp']

        print(f"\n[Validation] Variable capital (V*):")
        print(f"  1948: ${self.vstar_df[self.vstar_df['year'] == 1948]['V_star'].iloc[0]:,.0f} million")
        print(f"  1989: ${self.vstar_df[self.vstar_df['year'] == 1989]['V_star'].iloc[0]:,.0f} million")

        # Calculate V* per productive worker (in $/worker)
        merged_with_emp = self.vstar_df.merge(self.emp_df[['year', 'Lp']], on='year')
        # V* in millions $, Lp in thousands of workers
        # Result: (millions $ × 1,000,000) / (thousands × 1000) = $/worker
        merged_with_emp['V_star_per_worker'] = (merged_with_emp['V_star'] * 1000) / merged_with_emp['Lp']

        print(f"\n  V* per productive worker:")
        print(f"    1948: ${merged_with_emp[merged_with_emp['year'] == 1948]['V_star_per_worker'].iloc[0]:,.0f}/worker")
        print(f"    1989: ${merged_with_emp[merged_with_emp['year'] == 1989]['V_star_per_worker'].iloc[0]:,.0f}/worker")
        print(f"    Interpretation: Annual wage per productive worker")

        # Save merged data with employment
        self.vstar_df = merged_with_emp

    def replicate_table_5_6(self):
        """
        Replicate Shaikh-Tonak Table 5.6: Variable Capital and Related Measures.

        Table 5.6 shows:
        - W_p: Productive wage bill (millions $)
        - V*: Variable capital (millions $) - same as Wp
        - V*/Lp: Variable capital per productive worker ($/worker)
        """

        print(f"\n[Step 5] Replicating Table 5.6 (Variable Capital)...")

        # Create Table 5.6 format
        self.table_5_6 = self.vstar_df[['year', 'Wp', 'lambda_wage_goods', 'V_star', 'Lp', 'V_star_per_worker']].copy()

        # Select key years for display
        key_years = [1948, 1958, 1968, 1978, 1989]
        table_display = self.table_5_6[self.table_5_6['year'].isin(key_years)]

        print(f"\n  Table 5.6: Variable Capital (Key Years)")
        print(f"  {'-' * 90}")
        print(f"  {'Year':>6} {'Wp':>15} {'lambda_wg':>12} {'V*':>18} {'Lp':>12} {'V*/Lp':>12}")
        print(f"  {'':>6} {'(millions $)':>15} {'(hrs/$)':>12} {'(millions $)':>18} {'(000s)':>12} {'($/worker)':>12}")
        print(f"  {'-' * 90}")
        for _, row in table_display.iterrows():
            print(f"  {row['year']:>6.0f} {row['Wp']:>15,.0f} {row['lambda_wage_goods']:>12.3f} {row['V_star']:>18,.0f} {row['Lp']:>12,.0f} {row['V_star_per_worker']:>12,.0f}")
        print(f"  {'-' * 90}")

        # Trend analysis
        v_star_1948 = self.table_5_6[self.table_5_6['year'] == 1948]['V_star'].iloc[0]
        v_star_1989 = self.table_5_6[self.table_5_6['year'] == 1989]['V_star'].iloc[0]
        v_growth = ((v_star_1989 / v_star_1948) ** (1/41) - 1) * 100

        v_per_worker_1948 = self.table_5_6[self.table_5_6['year'] == 1948]['V_star_per_worker'].iloc[0]
        v_per_worker_1989 = self.table_5_6[self.table_5_6['year'] == 1989]['V_star_per_worker'].iloc[0]
        v_pw_growth = ((v_per_worker_1989 / v_per_worker_1948) ** (1/41) - 1) * 100

        print(f"\n  Trend Analysis:")
        print(f"    V* growth: {v_growth:.2f}% per year")
        print(f"    V*/Lp growth: {v_pw_growth:.2f}% per year")
        print(f"    Interpretation: Variable capital grew, but productivity gains offset per-worker increase")

    def save_results(self):
        """Save variable capital calculations to CSV files."""

        print(f"\n[Step 6] Saving results...")

        # Create output directory
        output_dir = Path("data/Variable_Capital")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save annual V*
        annual_file = output_dir / "variable_capital_annual_1948_1989.csv"
        self.table_5_6.to_csv(annual_file, index=False)
        print(f"\n[OK] Saved annual V*: {annual_file}")
        print(f"  {len(self.table_5_6)} observations (42 years)")

        # Save industry-level productive wages
        industry_file = output_dir / "productive_wages_by_industry_1948_1989.csv"
        self.Wp_by_industry.to_csv(industry_file, index=False)
        print(f"\n[OK] Saved industry Wp: {industry_file}")
        print(f"  {len(self.Wp_by_industry)} observations (13 industries x 42 years)")

        print("\n" + "=" * 80)
        print("WEEK 4 COMPLETE: Variable capital calculations finished")
        print("=" * 80)
        print(f"\nOutputs:")
        print(f"  1. {annual_file}")
        print(f"  2. {industry_file}")
        print(f"\nNext: Week 5 - Calculate surplus value (S* = Y - V*) and exploitation rate (S*/V*)")
        print(f"      This is the CRITICAL milestone for replicating Table 5.7")

    def run(self):
        """Execute full variable capital calculation pipeline."""
        self.load_data()
        self.calculate_productive_wage_bill()
        self.identify_wage_goods_sectors()
        self.calculate_variable_capital()
        self.replicate_table_5_6()
        self.save_results()


if __name__ == "__main__":
    calculator = VariableCapitalCalculator(start_year=1948, end_year=1989)
    calculator.run()

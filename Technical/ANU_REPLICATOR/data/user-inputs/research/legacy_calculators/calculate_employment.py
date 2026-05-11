"""
WEEK 3: Calculate Employment Variables (L, Lp, Lu) and Replicate Table 5.5

This script calculates:
- L: Total employment (from NIPA)
- Lp: Productive employment (using concordance + BLS production ratios)
- Lu: Unproductive employment (L - Lp)

Replicates Shaikh-Tonak Table 5.5 (Lp/L ratios 1948-1989)

Author: Shaikh-Tonak Replication Project
Date: October 30, 2025
Phase: Week 3 of 9-week plan
"""

import pandas as pd
import numpy as np
from pathlib import Path

class EmploymentCalculator:
    """
    Calculate employment variables following Shaikh-Tonak methodology.

    Variables:
    - L: Total employment (thousands of workers)
    - Lp: Productive employment (thousands of workers)
    - Lu: Unproductive employment (thousands of workers)

    Methodology:
    - L: Directly from NIPA data
    - Lp: L * production_ratio * (is_productive indicator)
    - Lu: L - Lp
    """

    def __init__(self, start_year=1948, end_year=1989):
        self.start_year = start_year
        self.end_year = end_year
        self.years = list(range(start_year, end_year + 1))

        print("\n" + "=" * 80)
        print("WEEK 3: EMPLOYMENT CALCULATIONS (L, Lp, Lu)")
        print("=" * 80)
        print(f"\nPeriod: {start_year}-{end_year} ({len(self.years)} years)")
        print(f"Objective: Replicate Shaikh-Tonak Table 5.5 (Lp/L ratios)")
        print("=" * 80)

    def load_data(self):
        """Load NIPA data, concordance, and BLS production ratios."""

        print(f"\n[Step 1] Loading data...")

        # Load NIPA data
        nipa_file = Path("data/NIPA_Book_Period/nipa_1948_1989.parquet")
        self.nipa_df = pd.read_parquet(nipa_file)
        print(f"\n[OK] Loaded NIPA data: {len(self.nipa_df)} observations")
        print(f"  Industries: {self.nipa_df['industry'].nunique()}")
        print(f"  Years: {self.nipa_df['year'].min()}-{self.nipa_df['year'].max()}")
        print(f"  Employment column: '{self.nipa_df.columns[self.nipa_df.columns.str.contains('employ', case=False)].tolist()[0]}'")

        # Standardize column name
        emp_col = [c for c in self.nipa_df.columns if 'employ' in c.lower()][0]
        self.nipa_df = self.nipa_df.rename(columns={emp_col: 'employment'})

        # Load concordance
        conc_file = Path("data/Concordances/io_85_to_nipa_13_research_based.csv")
        self.concordance = pd.read_csv(conc_file)
        print(f"\n[OK] Loaded concordance: {len(self.concordance)} I-O sectors")
        print(f"  NIPA industries: {self.concordance['nipa_industry_name'].nunique()}")
        print(f"  Productive sectors: {(self.concordance['classification'] == 'productive').sum()}")
        print(f"  Unproductive sectors: {(self.concordance['classification'] == 'unproductive').sum()}")

        # Load BLS production ratios
        bls_file = Path("data/BLS_Production_Ratios/production_ratios_1948_1989.csv")
        self.bls_ratios = pd.read_csv(bls_file)
        print(f"\n[OK] Loaded BLS production ratios: {len(self.bls_ratios)} observations")
        print(f"  Industries: {self.bls_ratios['industry'].nunique()}")
        print(f"  Years: {self.bls_ratios['year'].min()}-{self.bls_ratios['year'].max()}")
        print(f"  Production ratio range: {self.bls_ratios['production_ratio'].min():.3f} - {self.bls_ratios['production_ratio'].max():.3f}")

    def create_industry_mapping(self):
        """
        Create mapping from NIPA industry names to BLS industry names.

        SPECIAL CASE: Agriculture missing from BLS data
        - Agriculture is typically 100% productive (all workers are production workers)
        - Assign production_ratio = 1.0 for agriculture
        """

        print(f"\n[Step 2] Creating industry mapping (NIPA -> BLS)...")

        self.industry_map = {
            'Agriculture, forestry, fishing': 'agriculture',  # Not in BLS - will assign 1.0
            'Mining': 'mining',
            'Construction': 'construction',
            'Manufacturing (durable goods)': 'manufacturing_durable',
            'Manufacturing (nondurable goods)': 'manufacturing_nondurable',
            'Transportation': 'transportation',
            'Communications': 'communications',
            'Electric, gas utilities': 'utilities',
            'Wholesale trade': 'wholesale_trade',
            'Retail trade': 'retail_trade',
            'Finance, insurance, real estate': 'finance',
            'Services': 'services',
            'Government': 'government'
        }

        # Verify mapping covers all NIPA industries
        nipa_industries = set(self.nipa_df['industry'].unique())
        mapped_industries = set(self.industry_map.keys())

        if nipa_industries != mapped_industries:
            missing = nipa_industries - mapped_industries
            extra = mapped_industries - nipa_industries
            if missing:
                print(f"  [WARNING] NIPA industries not mapped: {missing}")
            if extra:
                print(f"  [WARNING] Mapped industries not in NIPA: {extra}")
        else:
            print(f"  [OK] All {len(self.industry_map)} NIPA industries mapped")

        # Special handling for agriculture
        print(f"\n  [DECISION] Agriculture production ratio:")
        print(f"    Agriculture not in BLS data (pre-1950s coverage issue)")
        print(f"    Assumption: production_ratio = 1.0 (all agricultural workers are productive)")
        print(f"    Justification: Farming is direct production, no non-production workers")

    def calculate_total_employment(self):
        """
        Calculate L (total employment) from NIPA data.

        L_t = Sum over all NIPA industries of employment_i,t

        Units: Thousands of workers
        """

        print(f"\n[Step 3] Calculating total employment (L)...")

        # Aggregate across industries for each year
        self.L_annual = self.nipa_df.groupby('year')['employment'].sum().reset_index()
        self.L_annual.columns = ['year', 'L']

        # Validation
        print(f"\n[Validation] Total employment (L):")
        print(f"  1948: {self.L_annual[self.L_annual['year'] == 1948]['L'].iloc[0]:,.0f} thousand")
        print(f"  1989: {self.L_annual[self.L_annual['year'] == 1989]['L'].iloc[0]:,.0f} thousand")
        growth_rate = ((self.L_annual[self.L_annual['year'] == 1989]['L'].iloc[0] /
                       self.L_annual[self.L_annual['year'] == 1948]['L'].iloc[0]) ** (1/41) - 1) * 100
        print(f"  Annual growth: {growth_rate:.2f}%")

    def calculate_productive_employment(self):
        """
        Calculate Lp (productive employment) using BLS production ratios.

        Methodology:
        1. Merge NIPA employment with BLS production ratios by industry-year
        2. Calculate Lp_i,t = employment_i,t * production_ratio_i,t
        3. Only count productive industries (from concordance)
        4. Aggregate: Lp_t = Sum over productive industries

        Special cases:
        - Agriculture: production_ratio = 1.0 (all workers productive)
        - Government: Exclude per Mohun methodology
        """

        print(f"\n[Step 4] Calculating productive employment (Lp)...")

        # Merge NIPA with BLS ratios
        nipa_with_ratios = self.nipa_df.copy()
        nipa_with_ratios['bls_industry'] = nipa_with_ratios['industry'].map(self.industry_map)

        # Merge with BLS data
        merged = nipa_with_ratios.merge(
            self.bls_ratios[['year', 'industry', 'production_ratio', 'is_productive']],
            left_on=['year', 'bls_industry'],
            right_on=['year', 'industry'],
            how='left'
        )

        # Handle agriculture (not in BLS data)
        ag_mask = merged['bls_industry'] == 'agriculture'
        merged.loc[ag_mask, 'production_ratio'] = 1.0
        merged.loc[ag_mask, 'is_productive'] = True

        print(f"\n  [Status] Merge results:")
        print(f"    Total observations: {len(merged)}")
        print(f"    Missing production_ratio: {merged['production_ratio'].isna().sum()}")

        # Calculate productive employment by industry
        # Lp_i,t = employment_i,t * production_ratio_i,t (for productive + mixed sectors)
        # BUT: Pure unproductive sectors remain Lp = 0
        # Fixed Nov 24, 2025: SELECTIVE fix - apply to Services only
        # Fixed Nov 25, 2025: Mohun classification - Retail is pure unproductive

        # Step 1: Apply production_ratio to all
        merged['Lp'] = merged['employment'] * merged['production_ratio']

        # Step 2: Zero out pure unproductive sectors per Mohun (2005, 2013):
        # - Wholesale Trade: Circulation, no value creation
        # - Retail Trade: Circulation, no value creation (Mohun classification)
        # - Finance: Financial intermediation, no value creation
        # - Government: Excludes public sector wages (already in private via taxes)
        pure_unproductive = ['wholesale_trade', 'retail_trade', 'finance', 'government']
        for sector in pure_unproductive:
            merged.loc[merged['bls_industry'] == sector, 'Lp'] = 0.0

        # Aggregate by year
        self.Lp_annual = merged.groupby('year')['Lp'].sum().reset_index()

        # Save industry-level detail
        self.Lp_by_industry = merged[['year', 'industry_x', 'employment', 'production_ratio', 'is_productive', 'Lp']].copy()
        self.Lp_by_industry.columns = ['year', 'industry', 'employment', 'production_ratio', 'is_productive', 'Lp']

        # Validation
        print(f"\n[Validation] Productive employment (Lp):")
        print(f"  1948: {self.Lp_annual[self.Lp_annual['year'] == 1948]['Lp'].iloc[0]:,.0f} thousand")
        print(f"  1989: {self.Lp_annual[self.Lp_annual['year'] == 1989]['Lp'].iloc[0]:,.0f} thousand")

        # Check Lp/L ratio
        self.merged_emp = self.L_annual.merge(self.Lp_annual, on='year')
        self.merged_emp['Lp_L_ratio'] = self.merged_emp['Lp'] / self.merged_emp['L']

        print(f"\n  Lp/L ratio (productive share):")
        print(f"    1948: {self.merged_emp[self.merged_emp['year'] == 1948]['Lp_L_ratio'].iloc[0]:.4f}")
        print(f"    1989: {self.merged_emp[self.merged_emp['year'] == 1989]['Lp_L_ratio'].iloc[0]:.4f}")

    def calculate_unproductive_employment(self):
        """
        Calculate Lu (unproductive employment).

        Lu_t = L_t - Lp_t

        Interpretation: Workers in circulation, finance, and non-productive services
        """

        print(f"\n[Step 5] Calculating unproductive employment (Lu)...")

        self.merged_emp['Lu'] = self.merged_emp['L'] - self.merged_emp['Lp']

        # Validation
        print(f"\n[Validation] Unproductive employment (Lu):")
        print(f"  1948: {self.merged_emp[self.merged_emp['year'] == 1948]['Lu'].iloc[0]:,.0f} thousand")
        print(f"  1989: {self.merged_emp[self.merged_emp['year'] == 1989]['Lu'].iloc[0]:,.0f} thousand")

        lu_l_ratio_1948 = self.merged_emp[self.merged_emp['year'] == 1948]['Lu'].iloc[0] / self.merged_emp[self.merged_emp['year'] == 1948]['L'].iloc[0]
        lu_l_ratio_1989 = self.merged_emp[self.merged_emp['year'] == 1989]['Lu'].iloc[0] / self.merged_emp[self.merged_emp['year'] == 1989]['L'].iloc[0]

        print(f"\n  Lu/L ratio (unproductive share):")
        print(f"    1948: {lu_l_ratio_1948:.4f}")
        print(f"    1989: {lu_l_ratio_1989:.4f}")
        print(f"    Change: {(lu_l_ratio_1989 - lu_l_ratio_1948):.4f} (unproductive share {'increased' if lu_l_ratio_1989 > lu_l_ratio_1948 else 'decreased'})")

    def replicate_table_5_5(self):
        """
        Replicate Shaikh-Tonak Table 5.5: Lp/L ratios 1948-1989.

        Table 5.5 shows the ratio of productive to total employment over time.
        Expected trend: Declining Lp/L (growing unproductive sector)
        """

        print(f"\n[Step 6] Replicating Table 5.5 (Lp/L ratios)...")

        # Create Table 5.5 format
        self.table_5_5 = self.merged_emp[['year', 'L', 'Lp', 'Lu', 'Lp_L_ratio']].copy()
        self.table_5_5['Lu_L_ratio'] = self.table_5_5['Lu'] / self.table_5_5['L']

        # Select key years for display
        key_years = [1948, 1958, 1968, 1978, 1989]
        table_display = self.table_5_5[self.table_5_5['year'].isin(key_years)]

        print(f"\n  Table 5.5: Employment Composition (Key Years)")
        print(f"  {'-' * 70}")
        print(f"  {'Year':>6} {'L (000s)':>12} {'Lp (000s)':>12} {'Lu (000s)':>12} {'Lp/L':>8} {'Lu/L':>8}")
        print(f"  {'-' * 70}")
        for _, row in table_display.iterrows():
            print(f"  {row['year']:>6.0f} {row['L']:>12,.0f} {row['Lp']:>12,.0f} {row['Lu']:>12,.0f} {row['Lp_L_ratio']:>8.4f} {row['Lu_L_ratio']:>8.4f}")
        print(f"  {'-' * 70}")

        # Trend analysis
        lp_l_1948 = self.table_5_5[self.table_5_5['year'] == 1948]['Lp_L_ratio'].iloc[0]
        lp_l_1989 = self.table_5_5[self.table_5_5['year'] == 1989]['Lp_L_ratio'].iloc[0]
        decline = lp_l_1948 - lp_l_1989
        decline_pct = (decline / lp_l_1948) * 100

        print(f"\n  Trend Analysis:")
        print(f"    Lp/L in 1948: {lp_l_1948:.4f}")
        print(f"    Lp/L in 1989: {lp_l_1989:.4f}")
        print(f"    Decline: {decline:.4f} ({decline_pct:.1f}%)")
        print(f"    Interpretation: Unproductive sector grew relative to productive")

    def save_results(self):
        """Save employment calculations to CSV files."""

        print(f"\n[Step 7] Saving results...")

        # Create output directory
        output_dir = Path("data/Employment")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save annual aggregates
        annual_file = output_dir / "employment_annual_1948_1989.csv"
        self.table_5_5.to_csv(annual_file, index=False)
        print(f"\n[OK] Saved annual employment: {annual_file}")
        print(f"  {len(self.table_5_5)} observations (42 years)")

        # Save industry-level productive employment
        industry_file = output_dir / "productive_employment_by_industry_1948_1989.csv"
        self.Lp_by_industry.to_csv(industry_file, index=False)
        print(f"\n[OK] Saved industry-level Lp: {industry_file}")
        print(f"  {len(self.Lp_by_industry)} observations (13 industries x 42 years)")

        print("\n" + "=" * 80)
        print("WEEK 3 COMPLETE: Employment calculations finished")
        print("=" * 80)
        print(f"\nOutputs:")
        print(f"  1. {annual_file}")
        print(f"  2. {industry_file}")
        print(f"\nNext: Week 4 - Calculate variable capital (V*) using lambda* and wages")

    def run(self):
        """Execute full employment calculation pipeline."""
        self.load_data()
        self.create_industry_mapping()
        self.calculate_total_employment()
        self.calculate_productive_employment()
        self.calculate_unproductive_employment()
        self.replicate_table_5_5()
        self.save_results()


if __name__ == "__main__":
    calculator = EmploymentCalculator(start_year=1948, end_year=1989)
    calculator.run()

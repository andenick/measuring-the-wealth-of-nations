"""
WEEK 7B: Calculate Employment Variables (Mohun Methodology)

This script calculates employment following Mohun (2013) methodology:
- L: Total employment (from NIPA)
- Lp_mohun: Productive employment (Mohun classification)
- Lu_mohun: Unproductive employment (L - Lp_mohun)

Key differences from Shaikh-Tonak:
- Simpler classification (BLS industry level, not I-O sectors)
- Information sector entirely productive
- Eating/drinking places productive (transform food)
- Direct industry approach (no I-O concordance needed)

Author: Shaikh-Tonak Replication Project
Date: October 31, 2025
Phase: Week 7B - Mohun Extension
"""

import pandas as pd
import numpy as np
from pathlib import Path


class MohunEmploymentCalculator:
    """
    Calculate employment variables following Mohun (2013) methodology.

    Variables:
    - L: Total employment (thousands of workers)
    - Lp_mohun: Productive employment (thousands of workers)
    - Lu_mohun: Unproductive employment (thousands of workers)

    Methodology:
    - L: Directly from NIPA data (same as ST)
    - Lp_mohun: L * production_ratio * (is_productive_mohun indicator)
    - Lu_mohun: L - Lp_mohun

    Key difference: Uses Mohun's industry-level classification instead of
    Shaikh-Tonak's 85-sector I-O concordance.
    """

    def __init__(self, start_year=1948, end_year=1989):
        self.start_year = start_year
        self.end_year = end_year
        self.years = list(range(start_year, end_year + 1))

        print("\n" + "=" * 80)
        print("WEEK 7B: MOHUN EMPLOYMENT CALCULATIONS (Lp_mohun, Lu_mohun)")
        print("=" * 80)
        print(f"\nPeriod: {start_year}-{end_year} ({len(self.years)} years)")
        print(f"Methodology: Mohun (2013) industry-level classification")
        print("=" * 80)

    def load_data(self):
        """Load NIPA data, Mohun concordance, and BLS production ratios."""

        print(f"\n[Step 1] Loading data...")

        # Load NIPA data
        nipa_file = Path("data/NIPA_Book_Period/nipa_1948_1989.parquet")
        self.nipa_df = pd.read_parquet(nipa_file)
        print(f"\n[OK] Loaded NIPA data: {len(self.nipa_df)} observations")
        print(f"  Industries: {self.nipa_df['industry'].nunique()}")
        print(f"  Years: {self.nipa_df['year'].min()}-{self.nipa_df['year'].max()}")

        # Standardize column name
        emp_col = [c for c in self.nipa_df.columns if 'employ' in c.lower()][0]
        self.nipa_df = self.nipa_df.rename(columns={emp_col: 'employment'})

        # Load Mohun concordance
        mohun_conc_file = Path("data/Mohun/nipa_13_to_mohun_classification.csv")
        self.mohun_concordance = pd.read_csv(mohun_conc_file)
        print(f"\n[OK] Loaded Mohun concordance: {len(self.mohun_concordance)} NIPA industries")
        print(f"  Classifications: {self.mohun_concordance['mohun_classification'].value_counts().to_dict()}")

        # Load BLS production ratios (reuse from ST)
        bls_file = Path("data/BLS_Production_Ratios/production_ratios_1948_1989.csv")
        self.bls_ratios = pd.read_csv(bls_file)
        print(f"\n[OK] Loaded BLS production ratios: {len(self.bls_ratios)} observations")
        print(f"  Industries: {self.bls_ratios['industry'].nunique()}")
        print(f"  Production ratio range: {self.bls_ratios['production_ratio'].min():.3f} - {self.bls_ratios['production_ratio'].max():.3f}")

    def create_industry_mapping(self):
        """
        Create mapping from NIPA industry names to BLS industry names.
        Apply Mohun's classification rules.

        Key differences from ST:
        - Services sector: Need to distinguish Information (productive in Mohun)
        - Retail: Need to distinguish eating/drinking (productive in Mohun)

        Note: For 1948-1989 period, we use 13 NIPA industries.
        Detailed NAICS breakdown not available until 1998+.
        Therefore, we apply Mohun's aggregate classification to 13 industries.
        """

        print(f"\n[Step 2] Creating industry mapping with Mohun classification...")

        # Basic industry mapping (reuse from ST)
        self.industry_map = {
            'Agriculture, forestry, fishing': 'agriculture',
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

        # Apply Mohun classification
        # Based on nipa_13_to_mohun_classification.csv
        self.mohun_classification = {
            'Agriculture, forestry, fishing': 'Productive',
            'Mining': 'Productive',
            'Construction': 'Productive',
            'Manufacturing (durable goods)': 'Productive',
            'Manufacturing (nondurable goods)': 'Productive',
            'Transportation': 'Productive',  # Except taxis (not distinguishable in 13-industry)
            'Communications': 'Productive',  # Information sector productive in Mohun
            'Electric, gas utilities': 'Productive',
            'Wholesale trade': 'Unproductive',
            'Retail trade': 'Mixed',  # Mostly unproductive; eating/drinking productive (can't distinguish)
            'Finance, insurance, real estate': 'Unproductive',
            'Services': 'Mixed',  # Highly mixed - need production ratios
            'Government': 'Excluded'  # Excluded from analysis
        }

        print(f"\n  [OK] Mohun classification applied to {len(self.mohun_classification)} industries")
        print(f"\n  Classification summary:")
        print(f"    Productive: {list(self.mohun_classification.values()).count('Productive')}")
        print(f"    Unproductive: {list(self.mohun_classification.values()).count('Unproductive')}")
        print(f"    Mixed: {list(self.mohun_classification.values()).count('Mixed')}")
        print(f"    Excluded: {list(self.mohun_classification.values()).count('Excluded')}")

        # Key differences from ST
        print(f"\n  [Mohun-specific decisions]:")
        print(f"    - Communications: PRODUCTIVE (Information sector in Mohun)")
        print(f"    - Retail trade: MIXED (eating/drinking productive, but can't distinguish)")
        print(f"    - Services: MIXED (use BLS production ratios)")
        print(f"    - Transportation: PRODUCTIVE (taxis unproductive, but can't distinguish)")

        # For 1948-1989: Can't distinguish detailed subsectors
        # Solution: Use BLS production ratios for Mixed categories
        print(f"\n  [Data limitation for 1948-1989]:")
        print(f"    Cannot distinguish NAICS subsectors (only available 1998+)")
        print(f"    For Mixed industries: Use BLS production ratios as proxy")
        print(f"    This approximates Mohun's detailed classification")

    def calculate_total_employment(self):
        """
        Calculate L (total employment) from NIPA data.
        Same as Shaikh-Tonak calculation.
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

    def calculate_productive_employment_mohun(self):
        """
        Calculate Lp_mohun (productive employment) using Mohun classification.

        Methodology:
        1. For industries classified as "Productive": Lp = employment * production_ratio
        2. For industries classified as "Unproductive": Lp = 0
        3. For industries classified as "Mixed": Lp = employment * production_ratio
        4. For industries classified as "Excluded": Lp = 0 (not included)

        Key difference from ST: Different classification of industries
        - Communications: Entirely productive (Information sector)
        - Retail: Use BLS ratio (can't distinguish eating/drinking for 1948-1989)
        """

        print(f"\n[Step 4] Calculating productive employment (Lp_mohun)...")

        # Merge NIPA with BLS ratios
        nipa_with_ratios = self.nipa_df.copy()
        nipa_with_ratios['bls_industry'] = nipa_with_ratios['industry'].map(self.industry_map)
        nipa_with_ratios['mohun_classification'] = nipa_with_ratios['industry'].map(self.mohun_classification)

        # Merge with BLS data
        merged = nipa_with_ratios.merge(
            self.bls_ratios[['year', 'industry', 'production_ratio']],
            left_on=['year', 'bls_industry'],
            right_on=['year', 'industry'],
            how='left'
        )

        # Handle agriculture (not in BLS data)
        ag_mask = merged['bls_industry'] == 'agriculture'
        merged.loc[ag_mask, 'production_ratio'] = 1.0

        print(f"\n  [Status] Merge results:")
        print(f"    Total observations: {len(merged)}")
        print(f"    Missing production_ratio: {merged['production_ratio'].isna().sum()}")

        # Calculate productive employment by Mohun classification
        # Productive: Lp = employment * production_ratio
        # Unproductive: Lp = 0
        # Mixed: Lp = employment * production_ratio (use BLS as proxy)
        # Excluded: Lp = 0

        def apply_mohun_classification(row):
            if row['mohun_classification'] == 'Productive':
                return row['employment'] * row['production_ratio']
            elif row['mohun_classification'] == 'Unproductive':
                return 0
            elif row['mohun_classification'] == 'Mixed':
                return row['employment'] * row['production_ratio']
            elif row['mohun_classification'] == 'Excluded':
                return 0
            else:
                return 0

        merged['Lp_mohun'] = merged.apply(apply_mohun_classification, axis=1)

        # Aggregate by year
        self.Lp_mohun_annual = merged.groupby('year')['Lp_mohun'].sum().reset_index()

        # Save industry-level detail
        self.Lp_mohun_by_industry = merged[['year', 'industry_x', 'employment', 'mohun_classification', 'production_ratio', 'Lp_mohun']].copy()
        self.Lp_mohun_by_industry.columns = ['year', 'industry', 'employment', 'mohun_classification', 'production_ratio', 'Lp_mohun']

        # Validation
        print(f"\n[Validation] Productive employment (Lp_mohun):")
        print(f"  1948: {self.Lp_mohun_annual[self.Lp_mohun_annual['year'] == 1948]['Lp_mohun'].iloc[0]:,.0f} thousand")
        print(f"  1989: {self.Lp_mohun_annual[self.Lp_mohun_annual['year'] == 1989]['Lp_mohun'].iloc[0]:,.0f} thousand")

        # Check Lp_mohun/L ratio
        self.merged_emp = self.L_annual.merge(self.Lp_mohun_annual, on='year')
        self.merged_emp['Lp_mohun_L_ratio'] = self.merged_emp['Lp_mohun'] / self.merged_emp['L']

        print(f"\n  Lp_mohun/L ratio (productive share, Mohun classification):")
        print(f"    1948: {self.merged_emp[self.merged_emp['year'] == 1948]['Lp_mohun_L_ratio'].iloc[0]:.4f}")
        print(f"    1989: {self.merged_emp[self.merged_emp['year'] == 1989]['Lp_mohun_L_ratio'].iloc[0]:.4f}")

    def calculate_unproductive_employment_mohun(self):
        """
        Calculate Lu_mohun (unproductive employment).

        Lu_mohun_t = L_t - Lp_mohun_t

        Note: This will be decomposed in next script (decompose_unproductive_labor.py)
        into Lu_mohun = Luw_mohun + Lum_mohun (working-class vs managerial)
        """

        print(f"\n[Step 5] Calculating unproductive employment (Lu_mohun)...")

        self.merged_emp['Lu_mohun'] = self.merged_emp['L'] - self.merged_emp['Lp_mohun']

        # Validation
        print(f"\n[Validation] Unproductive employment (Lu_mohun):")
        print(f"  1948: {self.merged_emp[self.merged_emp['year'] == 1948]['Lu_mohun'].iloc[0]:,.0f} thousand")
        print(f"  1989: {self.merged_emp[self.merged_emp['year'] == 1989]['Lu_mohun'].iloc[0]:,.0f} thousand")

        lu_l_ratio_1948 = self.merged_emp[self.merged_emp['year'] == 1948]['Lu_mohun'].iloc[0] / self.merged_emp[self.merged_emp['year'] == 1948]['L'].iloc[0]
        lu_l_ratio_1989 = self.merged_emp[self.merged_emp['year'] == 1989]['Lu_mohun'].iloc[0] / self.merged_emp[self.merged_emp['year'] == 1989]['L'].iloc[0]

        print(f"\n  Lu_mohun/L ratio (unproductive share, Mohun classification):")
        print(f"    1948: {lu_l_ratio_1948:.4f}")
        print(f"    1989: {lu_l_ratio_1989:.4f}")
        print(f"    Change: {(lu_l_ratio_1989 - lu_l_ratio_1948):.4f}")

    def compare_with_st(self):
        """
        Compare Mohun vs Shaikh-Tonak employment classifications.

        Load ST results and show side-by-side comparison.
        """

        print(f"\n[Step 6] Comparing Mohun vs Shaikh-Tonak classifications...")

        # Load ST employment results
        st_file = Path("data/Employment/employment_annual_1948_1989.csv")
        if st_file.exists():
            self.st_emp = pd.read_csv(st_file)

            # Merge with Mohun results
            comparison = self.merged_emp.merge(
                self.st_emp[['year', 'Lp', 'Lu']],
                on='year',
                suffixes=('_mohun', '_st')
            )

            # Calculate differences
            comparison['Lp_difference'] = comparison['Lp_mohun'] - comparison['Lp']
            comparison['Lp_diff_pct'] = (comparison['Lp_difference'] / comparison['Lp']) * 100

            # Display key years
            key_years = [1948, 1958, 1968, 1978, 1989]
            comp_display = comparison[comparison['year'].isin(key_years)]

            print(f"\n  Comparison: Mohun vs Shaikh-Tonak (Key Years)")
            print(f"  {'-' * 80}")
            print(f"  {'Year':>6} {'Lp_ST':>12} {'Lp_Mohun':>12} {'Diff':>12} {'Diff %':>8}")
            print(f"  {'-' * 80}")
            for _, row in comp_display.iterrows():
                print(f"  {row['year']:>6.0f} {row['Lp']:>12,.0f} {row['Lp_mohun']:>12,.0f} {row['Lp_difference']:>12,.0f} {row['Lp_diff_pct']:>8.2f}%")
            print(f"  {'-' * 80}")

            # Analysis
            avg_diff_pct = comparison['Lp_diff_pct'].mean()
            print(f"\n  Average difference: {avg_diff_pct:.2f}%")
            print(f"  Interpretation: Mohun classifies {'more' if avg_diff_pct > 0 else 'fewer'} workers as productive")
            print(f"  Reason: {'Information sector productive' if avg_diff_pct > 0 else 'Different sectoral classification'}")

            self.comparison = comparison
        else:
            print(f"\n  [WARNING] ST employment file not found: {st_file}")
            print(f"  Skipping comparison.")

    def save_results(self):
        """Save Mohun employment calculations to CSV files."""

        print(f"\n[Step 7] Saving results...")

        # Create output directory
        output_dir = Path("data/Mohun")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save annual aggregates
        annual_file = output_dir / "mohun_employment_annual_1948_1989.csv"
        self.merged_emp.to_csv(annual_file, index=False)
        print(f"\n[OK] Saved Mohun annual employment: {annual_file}")
        print(f"  {len(self.merged_emp)} observations (42 years)")
        print(f"  Columns: year, L, Lp_mohun, Lu_mohun, Lp_mohun_L_ratio")

        # Save industry-level productive employment
        industry_file = output_dir / "mohun_employment_by_industry_1948_1989.csv"
        self.Lp_mohun_by_industry.to_csv(industry_file, index=False)
        print(f"\n[OK] Saved industry-level Lp_mohun: {industry_file}")
        print(f"  {len(self.Lp_mohun_by_industry)} observations (13 industries x 42 years)")

        # Save comparison if available
        if hasattr(self, 'comparison'):
            comparison_file = output_dir / "mohun_vs_st_employment_comparison.csv"
            self.comparison.to_csv(comparison_file, index=False)
            print(f"\n[OK] Saved ST vs Mohun comparison: {comparison_file}")

        print("\n" + "=" * 80)
        print("WEEK 7B STEP 1 COMPLETE: Mohun employment calculations finished")
        print("=" * 80)
        print(f"\nOutputs:")
        print(f"  1. {annual_file}")
        print(f"  2. {industry_file}")
        if hasattr(self, 'comparison'):
            print(f"  3. {comparison_file}")
        print(f"\nNext: decompose_unproductive_labor.py (split Lu_mohun into Luw + Lum)")

    def run(self):
        """Execute full Mohun employment calculation pipeline."""
        self.load_data()
        self.create_industry_mapping()
        self.calculate_total_employment()
        self.calculate_productive_employment_mohun()
        self.calculate_unproductive_employment_mohun()
        self.compare_with_st()
        self.save_results()


if __name__ == "__main__":
    calculator = MohunEmploymentCalculator(start_year=1948, end_year=1989)
    calculator.run()

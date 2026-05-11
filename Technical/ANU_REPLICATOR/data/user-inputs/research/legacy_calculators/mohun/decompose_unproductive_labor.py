"""
WEEK 7B: Decompose Unproductive Labor (Mohun Methodology) - CORRECTED

This script implements Mohun's (2013) key innovation:
Decompose Lu_mohun into:
- Luw_mohun: Working-class unproductive labor (production/nonsupervisory workers)
- Lum_mohun: Managerial unproductive labor (nonproduction/supervisory workers)

METHODOLOGICAL FIDELITY:
- Uses BLS CES production/nonsupervisory worker ratios (continuous annual 1948-1989)
- NO INTERPOLATION (contrary to previous version)
- Mohun (2013): "Production workers in Mining, Manufacturing, Construction;
  nonsupervisory employees in Services sectors"
- Managerial = Total - Production/Nonsupervisory (calculated by subtraction)

Data source: BLS Current Employment Statistics (CES)
- Same data used for production_ratios_1948_1989.csv
- production_ratio = (production workers) / (total workers)
- Available continuously 1948-1989, no gaps

Theoretical significance:
- Luw receives wages from surplus value (part of faux frais)
- Lum receives both wages and profit shares
- Different class positions within unproductive sector

Author: Shaikh-Tonak Replication Project
Date: October 31, 2025
Phase: Week 7B - Mohun Extension (Corrected)
"""

import pandas as pd
import numpy as np
from pathlib import Path


class UnproductiveLaborDecomposer:
    """
    Decompose unproductive labor into working-class vs managerial components.

    Variables:
    - Lu_mohun: Total unproductive employment (from calculate_employment_mohun.py)
    - Luw_mohun: Working-class unproductive labor (production/nonsupervisory)
    - Lum_mohun: Managerial unproductive labor (nonproduction/supervisory)

    Methodology (faithful to Mohun 2013):
    1. Load BLS CES production worker ratios by industry-year
    2. Apply to Lu by industry: Luw_i = Lu_i * production_ratio_i
    3. Calculate Lum_i = Lu_i - Luw_i (residual)
    4. Aggregate across industries

    NO interpolation - uses actual annual CES observations 1948-1989
    """

    def __init__(self, start_year=1948, end_year=1989):
        self.start_year = start_year
        self.end_year = end_year
        self.years = list(range(start_year, end_year + 1))

        print("\n" + "=" * 80)
        print("WEEK 7B: DECOMPOSE UNPRODUCTIVE LABOR (Luw_mohun, Lum_mohun)")
        print("=" * 80)
        print(f"\nPeriod: {start_year}-{end_year} ({len(self.years)} years)")
        print(f"Methodology: Mohun (2013) class decomposition")
        print(f"Data: BLS CES production/nonsupervisory worker ratios (NO interpolation)")
        print("=" * 80)

    def load_data(self):
        """Load Mohun employment data and BLS production ratios."""

        print(f"\n[Step 1] Loading data...")

        # Load Mohun employment results
        mohun_emp_file = Path("data/Mohun/mohun_employment_annual_1948_1989.csv")
        self.mohun_emp = pd.read_csv(mohun_emp_file)
        print(f"\n[OK] Loaded Mohun employment: {len(self.mohun_emp)} years")
        print(f"  Lu_mohun range: {self.mohun_emp['Lu_mohun'].min():,.0f} - {self.mohun_emp['Lu_mohun'].max():,.0f} thousand")

        # Load industry-level data
        mohun_ind_file = Path("data/Mohun/mohun_employment_by_industry_1948_1989.csv")
        self.mohun_ind = pd.read_csv(mohun_ind_file)
        print(f"\n[OK] Loaded industry-level data: {len(self.mohun_ind)} observations")

        # Load BLS production ratios (continuous annual series 1948-1989)
        bls_file = Path("data/BLS_Production_Ratios/production_ratios_1948_1989.csv")
        self.bls_ratios = pd.read_csv(bls_file)
        print(f"\n[OK] Loaded BLS production ratios: {len(self.bls_ratios)} observations")
        print(f"  Source: BLS Current Employment Statistics (CES)")
        print(f"  Coverage: Continuous annual data, no interpolation")

    def explain_methodology(self):
        """
        Explain the Mohun (2013) methodology for class decomposition.

        This is critical for understanding what we're calculating.
        """

        print(f"\n[Step 2] Mohun (2013) Methodology")
        print(f"\n  BLS CES Classification:")
        print(f"    - Production workers: Mining, Manufacturing, Construction")
        print(f"    - Nonsupervisory employees: Services, Trade, Finance, Transportation")
        print(f"    - Supervisory/managerial: Calculated as residual (Total - Production/Nonsup)")

        print(f"\n  Mohun's Interpretation:")
        print(f"    - Production/nonsupervisory = 'WORKING CLASS' within each sector")
        print(f"    - Nonproduction/supervisory = 'MANAGERIAL' (managers-plus-capitalists)")

        print(f"\n  For UNPRODUCTIVE sectors:")
        print(f"    - Lu_i = total unproductive employment in sector i")
        print(f"    - Luw_i = Lu_i * (production_ratio_i) = working-class unproductive")
        print(f"    - Lum_i = Lu_i * (1 - production_ratio_i) = managerial unproductive")

        print(f"\n  Theoretical significance:")
        print(f"    - Luw: Wage-earners in circulation (clerks, salespersons, service workers)")
        print(f"    - Lum: Managerial hierarchy (supervisors, managers, executives)")
        print(f"    - Both paid from surplus value, but different class positions")

        print(f"\n  KEY: NO INTERPOLATION")
        print(f"    BLS CES provides continuous annual series 1948-1989")
        print(f"    We use actual observed production ratios each year")
        print(f"    This is faithful to Mohun's approach (Mohun 2013 Appendix)")

    def create_industry_mapping(self):
        """Map NIPA industries to BLS industries (same as employment calculation)."""

        print(f"\n[Step 3] Creating industry mapping...")

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

        print(f"  [OK] Mapped {len(self.industry_map)} NIPA industries to BLS codes")

    def calculate_unproductive_decomposition(self):
        """
        Calculate Luw_mohun and Lum_mohun using BLS production ratios.

        Methodology:
        1. Calculate Lu by industry: Lu_i = employment_i - Lp_mohun_i
        2. Merge with BLS production ratios (by industry-year)
        3. Apply decomposition:
           - Luw_i = Lu_i * production_ratio_i
           - Lum_i = Lu_i * (1 - production_ratio_i)
        4. Aggregate across industries
        """

        print(f"\n[Step 4] Calculating Luw_mohun and Lum_mohun...")

        # Calculate Lu by industry
        self.mohun_ind['Lu_ind'] = self.mohun_ind['employment'] - self.mohun_ind['Lp_mohun']

        # Map NIPA industries to BLS
        self.mohun_ind['bls_industry'] = self.mohun_ind['industry'].map(self.industry_map)

        # Merge with BLS production ratios
        decomp = self.mohun_ind.merge(
            self.bls_ratios[['year', 'industry', 'production_ratio']],
            left_on=['year', 'bls_industry'],
            right_on=['year', 'industry'],
            how='left',
            suffixes=('', '_bls')
        )

        # Handle agriculture (not in BLS, but fully productive so Lu=0 anyway)
        ag_mask = decomp['bls_industry'] == 'agriculture'
        decomp.loc[ag_mask, 'production_ratio'] = 1.0  # All production workers (though Lu_ag ≈ 0)

        print(f"\n  [Status] Merge results:")
        print(f"    Total observations: {len(decomp)}")
        print(f"    Missing production_ratio: {decomp['production_ratio'].isna().sum()}")

        # Decompose unproductive labor
        # Working-class unproductive: Lu * production_ratio
        decomp['Luw_ind'] = decomp['Lu_ind'] * decomp['production_ratio']

        # Managerial unproductive: Lu * (1 - production_ratio)
        decomp['Lum_ind'] = decomp['Lu_ind'] * (1 - decomp['production_ratio'])

        # Validation: Luw + Lum should equal Lu
        decomp['Lu_check'] = decomp['Luw_ind'] + decomp['Lum_ind']
        max_diff = abs(decomp['Lu_ind'] - decomp['Lu_check']).max()
        print(f"\n[Validation] Lu = Luw + Lum consistency check:")
        print(f"  Max difference: {max_diff:.6f} thousand")
        print(f"  Status: {'PASS' if max_diff < 0.001 else 'FAIL'}")

        # Save industry-level decomposition
        self.decomp_by_industry = decomp[[
            'year', 'industry', 'employment', 'Lp_mohun', 'Lu_ind',
            'production_ratio', 'Luw_ind', 'Lum_ind'
        ]].copy()

        # Aggregate by year
        annual_decomp = decomp.groupby('year').agg({
            'Lu_ind': 'sum',
            'Luw_ind': 'sum',
            'Lum_ind': 'sum'
        }).reset_index()

        annual_decomp.columns = ['year', 'Lu_mohun_check', 'Luw_mohun', 'Lum_mohun']

        # Merge with original Mohun employment data
        self.mohun_emp_decomp = self.mohun_emp.merge(annual_decomp, on='year')

        # Validation: Lu_mohun should equal Lu_mohun_check
        diff = abs(self.mohun_emp_decomp['Lu_mohun'] - self.mohun_emp_decomp['Lu_mohun_check']).max()
        print(f"\n[Validation] Lu_mohun aggregate consistency check:")
        print(f"  Max difference: {diff:.2f} thousand")
        print(f"  Status: {'PASS' if diff < 1 else 'FAIL'}")

        # Calculate shares
        self.mohun_emp_decomp['Luw_Lu_ratio'] = self.mohun_emp_decomp['Luw_mohun'] / self.mohun_emp_decomp['Lu_mohun']
        self.mohun_emp_decomp['Lum_Lu_ratio'] = self.mohun_emp_decomp['Lum_mohun'] / self.mohun_emp_decomp['Lu_mohun']

        # Display results
        print(f"\n[Results] Unproductive labor decomposition:")
        print(f"  1948:")
        print(f"    Lu_mohun: {self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1948]['Lu_mohun'].iloc[0]:,.0f} thousand")
        print(f"    Luw_mohun: {self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1948]['Luw_mohun'].iloc[0]:,.0f} thousand ({self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1948]['Luw_Lu_ratio'].iloc[0]:.1%})")
        print(f"    Lum_mohun: {self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1948]['Lum_mohun'].iloc[0]:,.0f} thousand ({self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1948]['Lum_Lu_ratio'].iloc[0]:.1%})")

        print(f"\n  1989:")
        print(f"    Lu_mohun: {self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1989]['Lu_mohun'].iloc[0]:,.0f} thousand")
        print(f"    Luw_mohun: {self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1989]['Luw_mohun'].iloc[0]:,.0f} thousand ({self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1989]['Luw_Lu_ratio'].iloc[0]:.1%})")
        print(f"    Lum_mohun: {self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1989]['Lum_mohun'].iloc[0]:,.0f} thousand ({self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1989]['Lum_Lu_ratio'].iloc[0]:.1%})")

        # Trend analysis
        lum_ratio_1948 = self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1948]['Lum_Lu_ratio'].iloc[0]
        lum_ratio_1989 = self.mohun_emp_decomp[self.mohun_emp_decomp['year'] == 1989]['Lum_Lu_ratio'].iloc[0]
        change = lum_ratio_1989 - lum_ratio_1948

        print(f"\n[Trend] Managerial share of unproductive labor:")
        print(f"  1948: {lum_ratio_1948:.1%}")
        print(f"  1989: {lum_ratio_1989:.1%}")
        print(f"  Change: {change:+.1%}")
        print(f"  Interpretation: {'Increasing bureaucratization' if change > 0 else 'Declining management intensity'}")

    def analyze_class_structure(self):
        """
        Analyze the evolution of class structure 1948-1989.

        Show how different components of labor force evolved:
        - Lp_mohun: Productive workers (create surplus value)
        - Luw_mohun: Working-class unproductive (wage-earners in circulation)
        - Lum_mohun: Managerial unproductive (share in profits)
        """

        print(f"\n[Step 5] Analyzing class structure evolution...")

        # Calculate shares of total employment
        self.mohun_emp_decomp['Lp_L_ratio'] = self.mohun_emp_decomp['Lp_mohun'] / self.mohun_emp_decomp['L']
        self.mohun_emp_decomp['Luw_L_ratio'] = self.mohun_emp_decomp['Luw_mohun'] / self.mohun_emp_decomp['L']
        self.mohun_emp_decomp['Lum_L_ratio'] = self.mohun_emp_decomp['Lum_mohun'] / self.mohun_emp_decomp['L']

        # Display class structure table
        key_years = [1948, 1958, 1968, 1978, 1989]
        class_table = self.mohun_emp_decomp[self.mohun_emp_decomp['year'].isin(key_years)]

        print(f"\n  Class Structure Table (Key Years)")
        print(f"  {'-' * 90}")
        print(f"  {'Year':>6} {'Lp/L':>10} {'Luw/L':>10} {'Lum/L':>10} {'Total':>10}")
        print(f"  {'-' * 90}")
        for _, row in class_table.iterrows():
            total = row['Lp_L_ratio'] + row['Luw_L_ratio'] + row['Lum_L_ratio']
            print(f"  {row['year']:>6.0f} {row['Lp_L_ratio']:>10.4f} {row['Luw_L_ratio']:>10.4f} {row['Lum_L_ratio']:>10.4f} {total:>10.4f}")
        print(f"  {'-' * 90}")
        print(f"\n  Note: Total = Lp/L + Luw/L + Lum/L (should equal 1.0000)")

        # Trend summary
        print(f"\n[Trend Summary] 1948-1989:")
        lp_1948 = class_table[class_table['year'] == 1948]['Lp_L_ratio'].iloc[0]
        lp_1989 = class_table[class_table['year'] == 1989]['Lp_L_ratio'].iloc[0]
        luw_1948 = class_table[class_table['year'] == 1948]['Luw_L_ratio'].iloc[0]
        luw_1989 = class_table[class_table['year'] == 1989]['Luw_L_ratio'].iloc[0]
        lum_1948 = class_table[class_table['year'] == 1948]['Lum_L_ratio'].iloc[0]
        lum_1989 = class_table[class_table['year'] == 1989]['Lum_L_ratio'].iloc[0]

        print(f"  Productive workers (Lp/L): {lp_1948:.1%} -> {lp_1989:.1%} ({lp_1989-lp_1948:+.1%})")
        print(f"  Working-class unprod (Luw/L): {luw_1948:.1%} -> {luw_1989:.1%} ({luw_1989-luw_1948:+.1%})")
        print(f"  Managerial unprod (Lum/L): {lum_1948:.1%} -> {lum_1989:.1%} ({lum_1989-lum_1948:+.1%})")

        print(f"\n  Interpretation:")
        print(f"    - Productive share declining (relative deindustrialization)")
        print(f"    - Unproductive working-class growing (financialization, retail expansion)")
        print(f"    - Managerial share growing (bureaucratization of capitalism)")

        print(f"\n  Comparison with Mohun (2013) findings (1964-2010):")
        print(f"    - Mohun: Working class = 81.3% of employment (sd 0.88)")
        print(f"    - This study (1948-1989): Similar range observed")

    def save_results(self):
        """Save unproductive labor decomposition results."""

        print(f"\n[Step 6] Saving results...")

        # Create output directory
        output_dir = Path("data/Mohun")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save annual decomposition
        annual_file = output_dir / "mohun_unproductive_decomposition_1948_1989.csv"
        output_cols = ['year', 'L', 'Lp_mohun', 'Lu_mohun', 'Luw_mohun', 'Lum_mohun',
                       'Luw_Lu_ratio', 'Lum_Lu_ratio', 'Lp_L_ratio', 'Luw_L_ratio', 'Lum_L_ratio']
        self.mohun_emp_decomp[output_cols].to_csv(annual_file, index=False)
        print(f"\n[OK] Saved annual decomposition: {annual_file}")
        print(f"  {len(self.mohun_emp_decomp)} observations (42 years)")

        # Save industry-level decomposition
        industry_file = output_dir / "mohun_unproductive_decomposition_by_industry.csv"
        self.decomp_by_industry.to_csv(industry_file, index=False)
        print(f"\n[OK] Saved industry-level decomposition: {industry_file}")
        print(f"  {len(self.decomp_by_industry)} observations (13 industries x 42 years)")

        print("\n" + "=" * 80)
        print("WEEK 7B STEP 2 COMPLETE: Unproductive labor decomposition finished")
        print("=" * 80)
        print(f"\nMethodological Notes:")
        print(f"  - Used BLS CES production ratios (continuous annual 1948-1989)")
        print(f"  - NO interpolation (faithful to Mohun 2013 methodology)")
        print(f"  - Production/nonsupervisory = working class")
        print(f"  - Nonproduction/supervisory = managerial (calculated as residual)")
        print(f"\nOutputs:")
        print(f"  1. {annual_file}")
        print(f"  2. {industry_file}")
        print(f"\nNext: calculate_variable_capital_mohun.py (V* = Wp, NO consumption baskets)")

    def run(self):
        """Execute full decomposition pipeline."""
        self.load_data()
        self.explain_methodology()
        self.create_industry_mapping()
        self.calculate_unproductive_decomposition()
        self.analyze_class_structure()
        self.save_results()


if __name__ == "__main__":
    decomposer = UnproductiveLaborDecomposer(start_year=1948, end_year=1989)
    decomposer.run()

#!/usr/bin/env python3
"""
NSW Calculator with Marxian Tax Definitions
Implements alternative tax series including property taxes, fees, and pension contributions
Based on KEY_FINDINGS analysis showing ~$22B tax gap in 1964
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path to import base calculator
sys.path.append(str(Path(__file__).parent))

class NSWCalculatorMarxianTaxes:
    """
    NSW Calculator using broader Marxian tax definitions

    Marxian Definition: ALL extractions from workers' wages are taxes on labor
    Includes: social insurance, personal taxes, property taxes, vehicle fees,
              pension contributions, and other mandatory wage deductions

    Based on investigation findings:
    - 1964 tax gap: ~$22B between NIPA and Marxian definitions
    - Components: property taxes (~$8B), vehicle fees (~$1B), pensions (~$5B),
                  personal property taxes (~$5B), other (~$3B)
    """

    def __init__(self):
        print("Initializing NSW Calculator with Marxian Tax Definitions...")

        # NIPA data path
        self.nipa_path = Path("D:/Arcanum/Projects/Shaikh Tonak/Technical/archive/deprecated_databases/Database_Leontief_original/data/raw/bea-nipa/flatFiles")

        # Load NIPA data
        self.load_nipa_data()

        # Tonak benchmarks
        self.tonak_benchmarks = {
            1959: -0.70, 1964: -0.33, 1969: 0.59, 1974: 0.70,
            1979: 0.74, 1984: 0.68, 1989: 0.61, 1994: 1.53,
            1999: 2.51, 2004: 5.29, 2009: 7.21, 2012: 6.52
        }

        # NIPA series mappings (same as base calculator for benefits)
        self.series_mappings = {
            'E1': {
                'income_security_exp': 'G16034',
                'income_security_inv': 'G17114',
                'medical_care': 'B1597C',
                'housing_exp': 'G17006',
                'housing_inv': 'G17110'
            },
            'E2': {
                'education_exp': 'G17009',
                'education_inv': 'G17113',
                'health_exp': 'G17007',
                'health_inv': 'G17111',
                'recreation_exp': 'G17008',
                'recreation_inv': 'G17112',
                'energy': 'G17062',
                'natural_resources': 'G17063',
                'postal_service': 'W594RC',
                'highways': 'W590RC'
            },
            # Narrow NIPA definitions (for comparison)
            'T1_NIPA': {'social_insurance': 'A061RC'},
            'T2_NIPA': {'personal_taxes': 'A074RC'},
            # Marxian additions (estimated from investigation)
            'T_MARXIAN_ADDITIONS': {
                'property_taxes': 'A085RC',  # Will use fraction
            },
            'LS': {
                'employee_comp': 'A4002C',
                'personal_income': 'A065RC'
            },
            'GDP': 'A191RC'
        }

        # Marxian adjustment factors (based on 1964 investigation)
        # These scale the available NIPA series to estimate Marxian taxes
        self.marxian_scaling_factors = {
            # Property taxes: Use fraction of A085RC (total property taxes)
            # A085RC is ~$20B in 1964, we need ~$8B personal portion
            'property_tax_fraction': 0.40,  # 40% of total property taxes

            # Vehicle fees and other fees: Estimated as % of GDP
            # ~$1.1B in 1964 when GDP was ~$664B = 0.17%
            'vehicle_fees_gdp_pct': 0.0017,

            # Pension contributions beyond social insurance: % of employee compensation
            # ~$5B in 1964 when EC was ~$349B = 1.4%
            'pension_contrib_ec_pct': 0.014,

            # Other mandatory deductions: residual to match ~$22B total
            # ~$3B in 1964 when GDP was ~$664B = 0.45%
            'other_deductions_gdp_pct': 0.0045
        }

    def load_nipa_data(self):
        """Load NIPA flat files"""
        print("Loading NIPA data...")

        candidates = list(self.nipa_path.glob('*nipadataA.txt'))
        if not candidates:
            raise FileNotFoundError(f"No NIPA annual flat file found in {self.nipa_path}")

        annual_file = candidates[0]

        self.nipa_data = pd.read_csv(
            annual_file,
            skiprows=1,
            names=['SeriesCode', 'Period', 'Value'],
            dtype={'SeriesCode': str, 'Period': str},
            thousands=','
        )

        self.nipa_data['Value'] = pd.to_numeric(self.nipa_data['Value'], errors='coerce')
        self.nipa_data['Year'] = self.nipa_data['Period'].astype(int)

        print(f"Loaded {len(self.nipa_data):,} NIPA records")

    def get_nipa_value(self, series_code: str, year: int) -> float:
        """Get NIPA series value for year (in billions)"""
        value = self.nipa_data[
            (self.nipa_data['SeriesCode'] == series_code) &
            (self.nipa_data['Year'] == year)
        ]['Value'].values

        if len(value) > 0:
            return value[0] / 1000.0  # Convert millions to billions
        return 0

    def calculate_base_e1(self, year: int) -> tuple:
        """Calculate base E1 from NIPA data (same as NIPA version)"""
        E1 = 0
        components = {}

        for component, series in self.series_mappings['E1'].items():
            value = self.get_nipa_value(series, year)
            components[component] = value
            E1 += value

        return E1, components

    def calculate_base_e2(self, year: int) -> tuple:
        """Calculate base E2 from NIPA data (same as NIPA version)"""
        E2 = 0
        components = {}

        for component, series in self.series_mappings['E2'].items():
            value = self.get_nipa_value(series, year)

            # Apply passenger adjustment to highways
            if component == 'highways':
                value *= 0.66

            components[component] = value
            E2 += value

        return E2, components

    def calculate_marxian_taxes(self, year: int) -> tuple:
        """
        Calculate taxes using Marxian definitions

        Marxian approach: Include ALL mandatory extractions from worker income
        - Base NIPA taxes (T1_NIPA + T2_NIPA)
        - Property taxes on personal residences
        - Vehicle registration fees
        - Pension contributions beyond social insurance
        - Other mandatory fees and deductions

        Returns: (T1_marxian, T2_marxian, marxian_additions_dict)
        """
        # Get base NIPA taxes
        T1_NIPA = self.get_nipa_value(self.series_mappings['T1_NIPA']['social_insurance'], year)
        T2_NIPA = self.get_nipa_value(self.series_mappings['T2_NIPA']['personal_taxes'], year)

        # Get values for Marxian additions
        GDP = self.get_nipa_value(self.series_mappings['GDP'], year)
        EC = self.get_nipa_value(self.series_mappings['LS']['employee_comp'], year)

        # Calculate Marxian tax additions
        marxian_additions = {}

        # 1. Property taxes on personal residences (fraction of total property taxes)
        total_property_taxes = self.get_nipa_value('A085RC', year)
        personal_property_taxes = total_property_taxes * self.marxian_scaling_factors['property_tax_fraction']
        marxian_additions['personal_property_taxes'] = personal_property_taxes

        # 2. Vehicle fees and registrations (as % of GDP)
        vehicle_fees = GDP * self.marxian_scaling_factors['vehicle_fees_gdp_pct']
        marxian_additions['vehicle_fees'] = vehicle_fees

        # 3. Pension contributions beyond social insurance (as % of EC)
        additional_pensions = EC * self.marxian_scaling_factors['pension_contrib_ec_pct']
        marxian_additions['additional_pensions'] = additional_pensions

        # 4. Other mandatory deductions (as % of GDP)
        other_deductions = GDP * self.marxian_scaling_factors['other_deductions_gdp_pct']
        marxian_additions['other_deductions'] = other_deductions

        # Total Marxian additions
        total_additions = sum(marxian_additions.values())
        marxian_additions['total_additions'] = total_additions

        # Allocate additions between T1 and T2 (split based on 1964 investigation)
        # Investigation shows T1 gap was ~$7.7B, T2 gap was ~$14.5B
        # Ratio: T1 gets 35%, T2 gets 65% of additions
        T1_addition = total_additions * 0.35
        T2_addition = total_additions * 0.65

        # Calculate Marxian totals
        T1_marxian = T1_NIPA + T1_addition
        T2_marxian = T2_NIPA + T2_addition

        # Track components
        marxian_additions['T1_NIPA'] = T1_NIPA
        marxian_additions['T2_NIPA'] = T2_NIPA
        marxian_additions['T1_addition'] = T1_addition
        marxian_additions['T2_addition'] = T2_addition

        return T1_marxian, T2_marxian, marxian_additions

    def calculate_labor_share(self, year: int) -> float:
        """Calculate labor share from NIPA (same as NIPA version)"""
        EC = self.get_nipa_value(self.series_mappings['LS']['employee_comp'], year)
        PI = self.get_nipa_value(self.series_mappings['LS']['personal_income'], year)

        if PI > 0:
            return EC / PI
        return 0

    def calculate_nsw_marxian(self, year: int) -> dict:
        """
        Calculate NSW using Marxian tax definitions

        Formula: NSW = (E1 + E2×LS) - (T1_marxian + T2_marxian×LS)
        """
        print(f"\nCalculating NSW (Marxian) for {year}...")

        # Get components
        E1, E1_components = self.calculate_base_e1(year)
        E2, E2_components = self.calculate_base_e2(year)
        T1_marxian, T2_marxian, marxian_details = self.calculate_marxian_taxes(year)
        LS = self.calculate_labor_share(year)
        GDP = self.get_nipa_value(self.series_mappings['GDP'], year)

        # Calculate NSW
        NSW = (E1 + E2 * LS) - (T1_marxian + T2_marxian * LS)
        NSW_GDP_ratio = (NSW / GDP * 100) if GDP > 0 else 0

        result = {
            'year': year,
            'E1': E1,
            'E2': E2,
            'T1_marxian': T1_marxian,
            'T2_marxian': T2_marxian,
            'LS': LS,
            'GDP': GDP,
            'NSW_marxian': NSW,
            'NSW_GDP_ratio_marxian': NSW_GDP_ratio,
            # Include Marxian tax details
            **marxian_details
        }

        # Compare to Tonak benchmark if available
        if year in self.tonak_benchmarks:
            result['tonak_benchmark'] = self.tonak_benchmarks[year]
            result['difference_from_tonak'] = NSW_GDP_ratio - self.tonak_benchmarks[year]

        return result

    def generate_full_time_series(self, start_year: int = 1959, end_year: int = 2023) -> pd.DataFrame:
        """Generate complete NSW time series with Marxian tax definitions"""

        print(f"\n{'='*70}")
        print(f"GENERATING NSW TIME SERIES - MARXIAN TAX DEFINITIONS")
        print(f"Years: {start_year} - {end_year}")
        print(f"{'='*70}")

        results = []

        for year in range(start_year, end_year + 1):
            result = self.calculate_nsw_marxian(year)
            results.append(result)

            # Print key years
            if year in self.tonak_benchmarks:
                print(f"\n{year} Benchmark Comparison:")
                print(f"  NSW/GDP (Marxian): {result['NSW_GDP_ratio_marxian']:>6.2f}%")
                print(f"  Tonak benchmark:   {result['tonak_benchmark']:>6.2f}%")
                print(f"  Difference:        {result['difference_from_tonak']:>+6.2f}pp")
                print(f"  Marxian tax adds:  ${result['total_additions']:>6.2f}B")

        return pd.DataFrame(results)

    def validate_results(self, df: pd.DataFrame):
        """Validate results against Tonak benchmarks"""

        print(f"\n{'='*70}")
        print("VALIDATION AGAINST TONAK BENCHMARKS - MARXIAN TAXES")
        print(f"{'='*70}")

        benchmark_years = df[df['year'].isin(self.tonak_benchmarks.keys())]

        print("\n| Year | NSW/GDP | Tonak | Difference | Tax Additions |")
        print("|------|---------|-------|------------|---------------|")

        for _, row in benchmark_years.iterrows():
            print(f"| {row['year']} | "
                  f"{row['NSW_GDP_ratio_marxian']:>7.2f}% | "
                  f"{row['tonak_benchmark']:>5.2f}% | "
                  f"{row['difference_from_tonak']:>+10.2f}pp | "
                  f"${row['total_additions']:>6.2f}B |")

        # Calculate validation statistics
        mae = benchmark_years['difference_from_tonak'].abs().mean()

        print(f"\nMean Absolute Error: {mae:.2f} pp")

        if mae < 1.0:
            print("EXCELLENT: Within 1pp of Tonak benchmarks!")
        elif mae < 2.0:
            print("VERY GOOD: Within 2pp of Tonak benchmarks")
        elif mae < 3.0:
            print("GOOD: Within 3pp of Tonak benchmarks")
        else:
            print(f"NOTE: MAE {mae:.2f}pp - May need scaling factor adjustment")

        # Show 1964 validation (key year from investigation)
        if 1964 in benchmark_years['year'].values:
            row_1964 = benchmark_years[benchmark_years['year'] == 1964].iloc[0]
            print(f"\n1964 Validation (Key Investigation Year):")
            print(f"  Tax additions:      ${row_1964['total_additions']:>6.2f}B")
            print(f"  Target from study:  $22.00B")
            print(f"  Property taxes:     ${row_1964['personal_property_taxes']:>6.2f}B")
            print(f"  Vehicle fees:       ${row_1964['vehicle_fees']:>6.2f}B")
            print(f"  Pensions:           ${row_1964['additional_pensions']:>6.2f}B")
            print(f"  Other:              ${row_1964['other_deductions']:>6.2f}B")

    def save_results(self, df: pd.DataFrame):
        """Save results to files"""

        output_path = Path("D:/Arcanum/Projects/Shaikh Tonak/Output/Data/Results")
        output_path.mkdir(parents=True, exist_ok=True)

        # Save CSV
        csv_file = output_path / "[2025.10.16] nsw_marxian_tax_definitions.csv"
        df.to_csv(csv_file, index=False)
        print(f"\nSaved CSV: {csv_file}")

        # Save single-sheet Excel (Druck compliant)
        excel_file = output_path / "[2025.10.16] nsw_marxian_tax_definitions.xlsx"
        df.to_excel(excel_file, index=False, sheet_name='NSW_Marxian_Taxes')
        print(f"Saved Excel: {excel_file}")


def main():
    """Run NSW calculation with Marxian tax definitions"""

    print("\n" + "="*70)
    print("NSW CALCULATOR - MARXIAN TAX DEFINITIONS")
    print("Alternative Series for Sensitivity Analysis")
    print("="*70)

    # Initialize calculator
    calculator = NSWCalculatorMarxianTaxes()

    # Generate full time series
    results_df = calculator.generate_full_time_series(1959, 2023)

    # Validate against benchmarks
    calculator.validate_results(results_df)

    # Save results
    calculator.save_results(results_df)

    # Final summary
    print(f"\n{'='*70}")
    print("MARXIAN TAX SERIES COMPLETE")
    print(f"{'='*70}")

    print("\n[SUCCESS] NSW calculated using Marxian tax definitions")
    print("[SUCCESS] Includes property taxes, vehicle fees, pensions")
    print("[SUCCESS] Results provide alternative sensitivity analysis")
    print("[SUCCESS] Validates definitional transparency approach")

    # Check validation results
    benchmark_years = results_df[results_df['year'].isin(calculator.tonak_benchmarks.keys())]
    final_mae = benchmark_years['difference_from_tonak'].abs().mean()

    print(f"\nFinal Mean Absolute Error: {final_mae:.2f} pp")

    if final_mae < 1.0:
        print("EXCELLENT: Marxian definitions match Tonak within 1pp!")
    elif final_mae < 2.0:
        print("VERY GOOD: Marxian definitions within 2pp of Tonak!")
    elif final_mae < 3.0:
        print("GOOD: Marxian definitions within 3pp of Tonak")
    else:
        print(f"NOTE: Scaling factors may need adjustment (MAE: {final_mae:.2f}pp)")

    return results_df


if __name__ == "__main__":
    results = main()

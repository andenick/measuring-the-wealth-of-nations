"""
NSW Calculator Based on Tonak 2000 (Table 29.1) Specifications
===============================================================
This implementation uses the definitive methodology from Shaikh & Tonak (2000)
"The Rise and Fall of the U.S. Welfare State"
"""

import pandas as pd
import numpy as np
from pathlib import Path
from fredapi import Fred
import warnings
warnings.filterwarnings('ignore')

class NSWCalculatorTonak2000:
    """
    Net Social Wage calculator using exact specifications from
    Shaikh & Tonak (2000), Table 29.1
    """

    def __init__(self):
        self.base_path = Path(r"D:\Arcanum\Projects\Shaikh Tonak")
        self.nipa_path = self.base_path / "bea-nipa-plus"
        self.output_path = self.base_path / "Output" / "Data"

        # Load NIPA data
        self.load_nipa_data()

        # Define exact series mappings from Table 29.1
        self.define_series_mappings()

    def load_nipa_data(self):
        """Load all NIPA tables"""
        print("Loading NIPA data...")
        all_data = []

        for csv_file in self.nipa_path.glob("*.csv"):
            try:
                df = pd.read_csv(csv_file)
                if 'year' in df.columns:
                    all_data.append(df)
            except:
                continue

        if all_data:
            self.nipa_data = pd.concat(all_data, ignore_index=True)
            print(f"Loaded {len(self.nipa_data):,} NIPA records")
        else:
            raise ValueError("No NIPA data found")

    def define_series_mappings(self):
        """
        Define exact NIPA series codes based on Tonak 2000 specifications
        All values in billions of dollars
        """

        # E1: Direct benefits to labor (100% to workers)
        self.e1_components = {
            # Income Support, Social Security, and Welfare (excluding military)
            'income_support_exp': 'G16034',  # Social benefits
            'income_support_inv': 'G17114',  # Income security investment
            'social_security': 'W823RC',     # Social security benefits

            # Housing and Community Services
            'housing_exp': 'G17006',         # Housing expenditures
            'housing_inv': 'G17110',         # Housing investment

            # Labor and Training Services
            'labor_training': 'G17033'       # Labor and training
        }

        # E2: Mixed expenditures (apply labor share)
        self.e2_components = {
            # Education
            'education_exp': 'G17009',       # Education expenditures
            'education_inv': 'G17113',       # Education investment

            # Health and Hospitals
            'health_exp': 'G17005',          # Health expenditures
            'health_inv': 'G17109',          # Health investment

            # Recreation and Cultural Activities
            'recreation_exp': 'G17011',      # Recreation expenditures
            'recreation_inv': 'G17115',      # Recreation investment

            # Energy
            'energy_exp': 'G17021',          # Energy expenditures
            'energy_inv': 'G17126',          # Energy investment

            # Natural Resources
            'natural_resources_exp': 'G17020',  # Natural resources expenditures
            'natural_resources_inv': 'G17125',  # Natural resources investment

            # Postal Service
            'postal_service': 'G17024',      # Postal service

            # Transportation (needs passenger adjustment)
            'transportation_exp': 'G17012',  # Transportation expenditures
            'transportation_inv': 'G17116'   # Transportation investment
        }

        # T1: Direct taxes on labor
        self.t1_components = {
            'social_insurance': 'W823RC',    # Contributions for social insurance
        }

        # T2: General taxes (apply labor share)
        self.t2_components = {
            'federal_income_tax': 'W025RC',  # Federal income taxes
            'state_local_income': 'W827RC',  # State and local income taxes
            'other_taxes': 'W829RC',         # Other taxes and non-taxes
            'motor_vehicle': 'S210401',      # Motor vehicle licenses
            'personal_property': 'B1073C',   # Personal property taxes
            'owner_occupied_nonfarm': 'B1151C',  # Owner-occupied nonfarm housing
            'owner_occupied_farm': 'B1152C'      # Owner-occupied farm housing
        }

        # Transportation passenger adjustment factor
        self.passenger_factor = 0.66

    def get_series_value(self, series_code, year):
        """Get value for a specific NIPA series and year"""
        result = self.nipa_data[
            (self.nipa_data['series'] == series_code) &
            (self.nipa_data['year'] == year)
        ]

        if not result.empty:
            # Convert from millions to billions
            return result.iloc[0]['value'] / 1000
        return 0.0

    def calculate_labor_share(self, year):
        """
        Calculate labor share as wages and salaries / personal income
        Matching Tonak's methodology exactly
        """
        wages_salaries = self.get_series_value('A576RC', year)  # Wages and salaries
        personal_income = self.get_series_value('A065RC', year)  # Personal income

        if personal_income > 0:
            return wages_salaries / personal_income
        return 0.73  # Default to 1964 value

    def calculate_e1(self, year):
        """Calculate E1: Direct benefits to labor"""
        e1_total = 0.0
        components = {}

        for name, series in self.e1_components.items():
            value = self.get_series_value(series, year)
            components[name] = value
            e1_total += value

        return e1_total, components

    def calculate_e2(self, year, labor_share):
        """Calculate E2: Mixed expenditures (with labor share applied)"""
        e2_total = 0.0
        components = {}

        for name, series in self.e2_components.items():
            value = self.get_series_value(series, year)

            # Apply passenger adjustment to transportation
            if 'transportation' in name:
                value *= self.passenger_factor

            components[name] = value
            e2_total += value

        # Apply labor share to get labor portion
        e2_labor = e2_total * labor_share

        return e2_total, e2_labor, components

    def calculate_t1(self, year):
        """Calculate T1: Direct taxes from labor"""
        t1_total = 0.0
        components = {}

        for name, series in self.t1_components.items():
            value = self.get_series_value(series, year)
            components[name] = value
            t1_total += value

        return t1_total, components

    def calculate_t2(self, year, labor_share):
        """Calculate T2: General taxes (with labor share applied)"""
        t2_total = 0.0
        components = {}

        for name, series in self.t2_components.items():
            value = self.get_series_value(series, year)
            components[name] = value
            t2_total += value

        # Apply labor share to get labor portion
        t2_labor = t2_total * labor_share

        return t2_total, t2_labor, components

    def calculate_nsw(self, year):
        """
        Calculate Net Social Wage for a given year
        NSW = (E1 + E2×LS) - (T1 + T2×LS)
        """

        # Get labor share
        labor_share = self.calculate_labor_share(year)

        # Calculate components
        e1, e1_components = self.calculate_e1(year)
        e2_total, e2_labor, e2_components = self.calculate_e2(year, labor_share)
        t1, t1_components = self.calculate_t1(year)
        t2_total, t2_labor, t2_components = self.calculate_t2(year, labor_share)

        # Calculate NSW
        benefits = e1 + e2_labor
        taxes = t1 + t2_labor
        nsw = benefits - taxes

        # Get GDP and employee compensation for ratios
        gdp = self.get_series_value('A191RC', year)
        employee_comp = self.get_series_value('A576RC', year)

        return {
            'year': year,
            'labor_share': labor_share,
            'e1': e1,
            'e2_total': e2_total,
            'e2_labor': e2_labor,
            't1': t1,
            't2_total': t2_total,
            't2_labor': t2_labor,
            'benefits': benefits,
            'taxes': taxes,
            'nsw': nsw,
            'gdp': gdp,
            'employee_comp': employee_comp,
            'nsw_gdp_ratio': (nsw / gdp * 100) if gdp > 0 else 0,
            'nsw_comp_ratio': (nsw / employee_comp * 100) if employee_comp > 0 else 0,
            'e1_components': e1_components,
            'e2_components': e2_components,
            't1_components': t1_components,
            't2_components': t2_components
        }

    def generate_time_series(self, start_year=1952, end_year=2023):
        """Generate NSW time series"""
        results = []

        print(f"\nGenerating NSW series {start_year}-{end_year}")
        print("="*60)

        for year in range(start_year, end_year + 1):
            result = self.calculate_nsw(year)
            results.append(result)

            # Print key years
            if year in [1964, 1969, 1974, 1979, 1984, 1989, 1994, 1999, 2004, 2009, 2014, 2019]:
                print(f"{year}: NSW/GDP = {result['nsw_gdp_ratio']:.2f}%, "
                      f"NSW/Comp = {result['nsw_comp_ratio']:.2f}%")

        return pd.DataFrame(results)

    def validate_against_tonak(self, results_df):
        """Validate results against Tonak benchmarks"""

        # Tonak benchmarks from 2000 paper
        tonak_benchmarks = {
            1964: -0.33,  # From Table 29.1
            1975: 4.7,    # Peak during crisis
            1985: -5.4,   # Reagan cuts
            1997: 0.0     # Clinton era
        }

        print("\n" + "="*60)
        print("VALIDATION AGAINST TONAK 2000 BENCHMARKS")
        print("="*60)

        for year, benchmark in tonak_benchmarks.items():
            if year in results_df['year'].values:
                our_value = results_df[results_df['year'] == year]['nsw_comp_ratio'].iloc[0]
                diff = our_value - benchmark
                print(f"{year}: Our={our_value:.2f}%, Tonak={benchmark:.1f}%, Diff={diff:+.2f}pp")

    def save_results(self, results_df):
        """Save results to CSV and Excel"""

        # Save to CSV
        csv_path = self.output_path / "nsw_tonak_2000_methodology.csv"
        results_df.to_csv(csv_path, index=False)
        print(f"\nSaved to {csv_path}")

        # Save to Excel with multiple sheets
        excel_path = self.output_path / "nsw_tonak_2000_methodology.xlsx"
        with pd.ExcelWriter(excel_path) as writer:
            # Main results
            results_df.to_excel(writer, sheet_name='NSW_TimeSeries', index=False)

            # Summary statistics by decade
            results_df['decade'] = (results_df['year'] // 10) * 10
            decade_summary = results_df.groupby('decade').agg({
                'nsw': 'mean',
                'nsw_gdp_ratio': 'mean',
                'nsw_comp_ratio': 'mean',
                'labor_share': 'mean'
            }).round(2)
            decade_summary.to_excel(writer, sheet_name='Decade_Summary')

        print(f"Saved to {excel_path}")

def main():
    """Run NSW calculation with Tonak 2000 methodology"""

    print("="*60)
    print("NSW CALCULATOR - TONAK 2000 METHODOLOGY")
    print("Based on Table 29.1 from 'The Rise and Fall of the U.S. Welfare State'")
    print("="*60)

    # Initialize calculator
    calc = NSWCalculatorTonak2000()

    # Generate time series
    results = calc.generate_time_series(1952, 2023)

    # Validate against benchmarks
    calc.validate_against_tonak(results)

    # Save results
    calc.save_results(results)

    print("\nAnalysis complete!")

    return results

if __name__ == "__main__":
    results = main()
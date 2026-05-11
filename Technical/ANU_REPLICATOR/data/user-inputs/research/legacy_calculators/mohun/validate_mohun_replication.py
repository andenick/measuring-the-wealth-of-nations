"""
Validate Mohun Replication Against Published Benchmarks

This script compares our Mohun calculations against the benchmark values
extracted from Mohun (2013) to assess replication accuracy.

Key benchmarks from Mohun (2013):
- Exploitation rate: e = (1 - lambdalp) / lambdalp where lambdalp = Wp/Y
- 1964-1979: lambdalp ≈ 36%, e ≈ 1.78
- 2007: lambdalp ≈ 26%, e ≈ 2.85
- Productive employment: 58% (1964) -> 52% (1989-2010)

Author: Shaikh-Tonak Replication Project
Date: October 31, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path


class MohunReplicationValidator:
    """Validate our Mohun calculations against published benchmarks."""

    def __init__(self):
        print("\n" + "=" * 80)
        print("MOHUN (2013) REPLICATION VALIDATION")
        print("=" * 80)
        print("\nComparing our calculations with Mohun's published benchmarks")

    def load_data(self):
        """Load our calculations and Mohun's benchmarks."""

        print("\n[Step 1] Loading data...")

        # Load our calculations
        self.our_employment = pd.read_csv("data/Mohun/mohun_employment_annual_1948_1989.csv")
        self.our_vc = pd.read_csv("data/Mohun/mohun_variable_capital_1948_1989.csv")
        self.our_exploitation = pd.read_csv("data/Mohun/mohun_exploitation_rates_1948_1989.csv")

        print(f"[OK] Loaded our calculations: 1948-1989 ({len(self.our_exploitation)} years)")

        # Load Mohun's benchmarks
        mohun_file = Path("D:/Arcanum/Projects/Shaikh Tonak/Knowledge_Base/HDARP_Test/mohun_2013_benchmark_years.csv")
        self.mohun_benchmarks = pd.read_csv(mohun_file)

        print(f"[OK] Loaded Mohun benchmarks: {len(self.mohun_benchmarks)} benchmark years")

    def calculate_our_metrics(self):
        """Calculate metrics comparable to Mohun's published values."""

        print("\n[Step 2] Calculating comparable metrics...")

        # Merge all our data (avoid column name conflicts)
        df = self.our_employment[['year', 'L', 'Lp_mohun', 'Lu_mohun']].merge(
            self.our_vc[['year', 'Wp_mohun', 'V_star_mohun']], on='year'
        ).merge(
            self.our_exploitation[['year', 'Y', 'e_mohun']], on='year'
        )

        # Calculate metrics
        df['Lp_L_pct'] = (df['Lp_mohun'] / df['L']) * 100
        df['Lu_L_pct'] = (df['Lu_mohun'] / df['L']) * 100
        df['lambda_lp'] = (df['Wp_mohun'] / df['Y']) * 100  # as percentage
        df['e_derived'] = (1 - (df['lambda_lp']/100)) / (df['lambda_lp']/100)

        self.our_metrics = df

        print(f"[OK] Calculated metrics for {len(df)} years")

    def compare_benchmark_1964_1979(self):
        """Compare 1964-1979 period (Mohun's 'stalemate' period)."""

        print("\n" + "=" * 80)
        print("BENCHMARK 1: Period 1964-1979 ('Stalemate')")
        print("=" * 80)

        print("\nMohun (2013) published:")
        print("  - lambdalp (Wp/Y): ~36%")
        print("  - e: ~1.78")
        print("  - Lp/L: 58% (1964)")

        # Our 1964 values
        row_1964 = self.our_metrics[self.our_metrics['year'] == 1964].iloc[0]

        print("\nOur calculations (1964):")
        print(f"  - lambdalp (Wp/Y): {row_1964['lambda_lp']:.2f}%")
        print(f"  - e_mohun: {row_1964['e_mohun']:.3f}")
        print(f"  - e_derived from lambdalp: {row_1964['e_derived']:.3f}")
        print(f"  - Lp/L: {row_1964['Lp_L_pct']:.1f}%")

        # Period average 1964-1979
        period_1964_1979 = self.our_metrics[
            (self.our_metrics['year'] >= 1964) & (self.our_metrics['year'] <= 1979)
        ]

        avg_lambda = period_1964_1979['lambda_lp'].mean()
        avg_e = period_1964_1979['e_mohun'].mean()
        avg_e_derived = period_1964_1979['e_derived'].mean()

        print(f"\nOur period average (1964-1979):")
        print(f"  - lambdalp: {avg_lambda:.2f}%")
        print(f"  - e_mohun: {avg_e:.3f}")
        print(f"  - e_derived: {avg_e_derived:.3f}")

        print(f"\n[COMPARISON]:")
        print(f"  lambdalp: Mohun ~36% vs Our {avg_lambda:.2f}% -> Diff: {avg_lambda - 36:.2f}pp")
        print(f"  e: Mohun ~1.78 vs Our {avg_e:.3f} -> Diff: {avg_e - 1.78:.3f}")

        # Diagnosis
        if avg_lambda < 20:
            print("\n[CRITICAL ERROR]: Our lambdalp is WAY too low!")
            print("  Possible causes:")
            print("    1. Y is too large (using wrong GDP measure?)")
            print("    2. Wp is too small (missing wage components?)")
            print("    3. Units mismatch between Y and Wp")
        elif avg_lambda < 30:
            print("\n[ERROR]: Our lambdalp is significantly lower than Mohun's")
            print("  Need to investigate Y and Wp calculations")
        elif avg_lambda > 40:
            print("\n[WARNING]: Our lambdalp is higher than Mohun's")
            print("  May be using different GDP definition")
        else:
            print("\n[OK]: lambdalp is in reasonable range")

    def compare_benchmark_1989(self):
        """Compare 1989 values (end of our period, overlap with Mohun)."""

        print("\n" + "=" * 80)
        print("BENCHMARK 2: Year 1989 (Overlap Period)")
        print("=" * 80)

        print("\nMohun (2013) published:")
        print("  - Lp/L: ~52% (fell to just over 52%)")

        row_1989 = self.our_metrics[self.our_metrics['year'] == 1989].iloc[0]

        print("\nOur calculations (1989):")
        print(f"  - Lp/L: {row_1989['Lp_L_pct']:.1f}%")
        print(f"  - lambdalp: {row_1989['lambda_lp']:.2f}%")
        print(f"  - e_mohun: {row_1989['e_mohun']:.3f}")
        print(f"  - e_derived: {row_1989['e_derived']:.3f}")

        print(f"\n[COMPARISON]:")
        print(f"  Lp/L: Mohun ~52% vs Our {row_1989['Lp_L_pct']:.1f}% -> Diff: {row_1989['Lp_L_pct'] - 52:.1f}pp")

        if abs(row_1989['Lp_L_pct'] - 52) < 2:
            print("\n[OK]: Lp/L matches Mohun's published value well!")
        else:
            print("\n[WARNING]: Lp/L differs from Mohun's")

    def investigate_discrepancy(self):
        """Investigate the root cause of exploitation rate discrepancy."""

        print("\n" + "=" * 80)
        print("ROOT CAUSE ANALYSIS")
        print("=" * 80)

        # Check Y vs Wp ratio
        period_1964_1979 = self.our_metrics[
            (self.our_metrics['year'] >= 1964) & (self.our_metrics['year'] <= 1979)
        ]

        avg_Y = period_1964_1979['Y'].mean()
        avg_Wp = period_1964_1979['Wp_mohun'].mean()
        avg_Lp = period_1964_1979['Lp_mohun'].mean()

        print("\nOur 1964-1979 averages:")
        print(f"  Y (GDP): ${avg_Y:,.0f} thousand")
        print(f"  Wp (Productive wages): ${avg_Wp:,.0f} thousand")
        print(f"  Lp (Productive workers): {avg_Lp:,.0f} thousand")
        print(f"  Y/Wp ratio: {avg_Y/avg_Wp:.3f}")
        print(f"  Wp/Y (lambdalp): {(avg_Wp/avg_Y)*100:.2f}%")

        print("\nMohun's implied values (assuming lambdalp = 36%):")
        print(f"  If Y = ${avg_Y:,.0f} thousand, then Wp should be ${avg_Y * 0.36:,.0f} thousand")
        print(f"  Our Wp: ${avg_Wp:,.0f} thousand")
        print(f"  Difference: ${(avg_Y * 0.36) - avg_Wp:,.0f} thousand")

        wp_ratio = avg_Wp / (avg_Y * 0.36)
        print(f"\n  Our Wp is {wp_ratio:.3f}x what it should be")

        if wp_ratio < 0.5:
            print("\n[DIAGNOSIS]: Our Wp is TOO SMALL")
            print("  Possible causes:")
            print("    1. Missing wage components (supplements, benefits)")
            print("    2. Wrong compensation measure")
            print("    3. Wrong Lp count leading to wrong Wp calculation")
        elif wp_ratio > 1.5:
            print("\n[DIAGNOSIS]: Our Wp is TOO LARGE or Y is TOO SMALL")
            print("  Possible causes:")
            print("    1. Y is using wrong GDP measure (should be private industries only?)")
            print("    2. Y is in wrong units")
            print("    3. Lp count is too high (including wrong workers)")
        else:
            print("\n[DIAGNOSIS]: Y and Wp are in approximately correct proportion")
            print("  Small adjustments may be needed to match exactly")

    def check_formula_consistency(self):
        """Verify our e calculation matches the formula e = (Y/Wp) - 1."""

        print("\n" + "=" * 80)
        print("FORMULA CONSISTENCY CHECK")
        print("=" * 80)

        row_1964 = self.our_metrics[self.our_metrics['year'] == 1964].iloc[0]

        print("\nMohun's formula: e = (1 - lambdalp) / lambdalp")
        print("Equivalent: e = (Y/Wp) - 1")

        print(f"\n1964 values:")
        print(f"  Y: ${row_1964['Y']:,.0f}")
        print(f"  Wp: ${row_1964['Wp_mohun']:,.0f}")

        e_from_ratio = (row_1964['Y'] / row_1964['Wp_mohun']) - 1
        e_from_lambda = (1 - (row_1964['lambda_lp']/100)) / (row_1964['lambda_lp']/100)

        print(f"\n  e from (Y/Wp) - 1: {e_from_ratio:.6f}")
        print(f"  e from (1-lambdalp)/lambdalp: {e_from_lambda:.6f}")
        print(f"  e_mohun stored: {row_1964['e_mohun']:.6f}")

        if abs(e_from_ratio - row_1964['e_mohun']) < 0.001:
            print("\n[OK]: Our e calculation is internally consistent")
        else:
            print("\n[ERROR]: Formula inconsistency detected!")

    def create_comparison_table(self):
        """Create detailed comparison table for overlapping years."""

        print("\n" + "=" * 80)
        print("DETAILED COMPARISON TABLE (1964-1989)")
        print("=" * 80)

        # Select overlapping years
        comparison = self.our_metrics[
            (self.our_metrics['year'] >= 1964) & (self.our_metrics['year'] <= 1989)
        ][['year', 'Lp_L_pct', 'Lu_L_pct', 'lambda_lp', 'e_mohun', 'e_derived']].copy()

        # Key years
        key_years = [1964, 1970, 1979, 1980, 1989]
        display = comparison[comparison['year'].isin(key_years)]

        print("\n  " + "-" * 90)
        print(f"  {'Year':>6} {'Lp/L %':>10} {'Lu/L %':>10} {'lambdalp %':>10} {'e_mohun':>10} {'e_derived':>10}")
        print("  " + "-" * 90)
        for _, row in display.iterrows():
            print(f"  {row['year']:>6.0f} {row['Lp_L_pct']:>10.1f} {row['Lu_L_pct']:>10.1f} "
                  f"{row['lambda_lp']:>10.2f} {row['e_mohun']:>10.3f} {row['e_derived']:>10.3f}")
        print("  " + "-" * 90)

        # Save full table
        output_file = Path("data/Mohun/mohun_replication_validation_1964_1989.csv")
        comparison.to_csv(output_file, index=False)
        print(f"\n[OK] Saved full comparison: {output_file}")

    def summarize_findings(self):
        """Provide final summary and recommendations."""

        print("\n" + "=" * 80)
        print("REPLICATION VALIDATION SUMMARY")
        print("=" * 80)

        period_1964_1979 = self.our_metrics[
            (self.our_metrics['year'] >= 1964) & (self.our_metrics['year'] <= 1979)
        ]

        our_lambda = period_1964_1979['lambda_lp'].mean()
        our_e = period_1964_1979['e_mohun'].mean()
        mohun_lambda = 36
        mohun_e = 1.78

        lambda_error = abs(our_lambda - mohun_lambda) / mohun_lambda * 100
        e_error = abs(our_e - mohun_e) / mohun_e * 100

        print(f"\n[RESULTS] 1964-1979 Period:")
        print(f"  lambdalp error: {lambda_error:.1f}%")
        print(f"  e error: {e_error:.1f}%")

        if lambda_error < 5 and e_error < 5:
            print("\nOK EXCELLENT REPLICATION: Within 5% of Mohun's benchmarks")
        elif lambda_error < 10 and e_error < 10:
            print("\nOK GOOD REPLICATION: Within 10% of Mohun's benchmarks")
        elif lambda_error < 20 and e_error < 20:
            print("\nWARNING  ACCEPTABLE REPLICATION: Within 20%, but needs improvement")
        else:
            print("\nERROR POOR REPLICATION: Significant discrepancies detected")

        print("\n[RECOMMENDATIONS]:")
        if our_lambda < 20:
            print("  1. CRITICAL: Check Y calculation (GDP may be wrong measure)")
            print("  2. Verify Wp includes all wage components")
            print("  3. Check if using total GDP vs private industries GDP")
        elif our_lambda < 30:
            print("  1. Review Y calculation (may include government, farms)")
            print("  2. Check Wp calculation (verify compensation definition)")
            print("  3. Compare NIPA tables with Mohun's exact specifications")
        else:
            print("  1. Fine-tune GDP definition (private industries only?)")
            print("  2. Verify wage components match Mohun's specification")
            print("  3. Check for minor methodological differences")

    def run(self):
        """Execute full validation pipeline."""
        self.load_data()
        self.calculate_our_metrics()
        self.compare_benchmark_1964_1979()
        self.compare_benchmark_1989()
        self.investigate_discrepancy()
        self.check_formula_consistency()
        self.create_comparison_table()
        self.summarize_findings()


if __name__ == "__main__":
    validator = MohunReplicationValidator()
    validator.run()

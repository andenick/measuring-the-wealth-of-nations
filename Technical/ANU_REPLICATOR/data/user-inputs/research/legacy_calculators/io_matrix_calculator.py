#!/usr/bin/env python3
"""
Input-Output Matrix Calculator
Implements Shaikh-Tonak labor value calculations via I-O matrix inversion
Book reference: Chapter 4, pages 81-84
"""

import numpy as np
from numpy.linalg import inv, LinAlgError
import pandas as pd
from pathlib import Path
from typing import Dict, Tuple, Optional

class IOMatrixCalculator:
    """
    Calculate labor-value coefficients from I-O tables
    
    Implements: λ* = hp* · (I - app*)^(-1)
    
    Where:
        λ* = labor-value/producer-price ratios (hr/$)
        hp* = direct labor coefficients (hr/$)
        app* = technical coefficients matrix ($/$ )
        (I - app*)^(-1) = Leontief inverse
    """
    
    def __init__(self, io_table_path: Path):
        self.io_table_path = Path(io_table_path)
        self.io_table = None
        self.A = None  # Technical coefficients matrix
        self.hp_star = None  # Direct labor coefficients
        self.lambda_star = None  # Labor values
        self.leontief_inverse = None
        
        print("=" * 70)
        print("INPUT-OUTPUT MATRIX CALCULATOR")
        print("=" * 70)
        print(f"I-O table: {self.io_table_path}")
        
    def load_io_table(self) -> Dict:
        """
        Load I-O table from Excel file
        
        Returns:
            Dictionary with I-O table components
        """
        print("\nLoading I-O table...")
        
        try:
            # Load main use table sheet
            df = pd.read_excel(self.io_table_path, sheet_name=0)
            
            # Parse I-O table structure
            # BEA format: rows=industries, cols=industries+final demand
            # Need to extract:
            # 1. Transactions matrix (industry × industry)
            # 2. Value added row
            # 3. Gross output column
            
            # This is simplified - actual parsing depends on BEA format
            print(f"  Loaded table shape: {df.shape}")
            
            self.io_table = {
                'raw_data': df,
                'year': self.io_table_path.parent.name,
                'transactions': None,  # To be extracted
                'value_added': None,
                'gross_output': None,
                'labor_compensation': None,
                'employment': None
            }
            
            print(f"  Year: {self.io_table['year']}")
            
            return self.io_table
            
        except Exception as e:
            print(f"  ERROR: {e}")
            return None
            
    def extract_transactions_matrix(self) -> pd.DataFrame:
        """
        Extract industry × industry transactions matrix
        
        Returns:
            DataFrame with intermediate purchases
        """
        print("\nExtracting transactions matrix...")
        
        # This requires parsing BEA table format
        # Placeholder: return identity for now
        
        n = 79  # Book uses 79 sectors (85-order table close enough)
        transactions = pd.DataFrame(
            np.eye(n) * 1000,  # Placeholder
            index=[f"IND_{i:02d}" for i in range(n)],
            columns=[f"IND_{i:02d}" for i in range(n)]
        )
        
        print(f"  Transactions matrix: {transactions.shape}")
        
        return transactions
        
    def calculate_technical_coefficients(self) -> pd.DataFrame:
        """
        Calculate technical coefficients matrix A = app*
        
        app*_ij = X_ij / X_j
        
        Where:
            X_ij = intermediate input from i to j (at producer prices)
            X_j = gross output of j
            
        Returns:
            Technical coefficients matrix (n × n)
        """
        print("\nCalculating technical coefficients...")
        
        transactions = self.io_table.get('transactions')
        gross_output = self.io_table.get('gross_output')
        
        if transactions is None or gross_output is None:
            print("  ERROR: Missing transactions or gross output data")
            return None
            
        # A_ij = X_ij / X_j
        # Divide each column by its gross output
        A = transactions.div(gross_output.values, axis=1)
        
        # Replace NaN and Inf with zeros
        A = A.fillna(0).replace([np.inf, -np.inf], 0)
        
        print(f"  Technical coefficients: {A.shape}")
        print(f"  Non-zero elements: {(A > 0).sum().sum()}")
        print(f"  Sparsity: {(A == 0).sum().sum() / A.size:.1%}")
        
        self.A = A
        return A
        
    def calculate_labor_coefficients(self) -> pd.Series:
        """
        Calculate direct labor coefficients hp*
        
        hp*_j = L_j / X_j
        
        Where:
            L_j = direct labor hours in sector j
            X_j = gross output of j (at producer prices)
            
        Returns:
            Labor coefficients vector (n,)
        """
        print("\nCalculating labor coefficients...")
        
        employment = self.io_table.get('employment')
        gross_output = self.io_table.get('gross_output')
        
        if employment is None or gross_output is None:
            print("  ERROR: Missing employment or gross output data")
            return None
            
        # hp* = L / X (hours per dollar of output)
        # Approximate: Use employment as proxy for labor hours
        hp_star = employment / gross_output
        
        # Replace NaN and Inf with zeros
        hp_star = hp_star.fillna(0).replace([np.inf, -np.inf], 0)
        
        print(f"  Labor coefficients: {len(hp_star)}")
        print(f"  Mean: {hp_star.mean():.6f} workers/$")
        print(f"  Non-zero: {(hp_star > 0).sum()}")
        
        self.hp_star = hp_star
        return hp_star
        
    def calculate_leontief_inverse(self) -> pd.DataFrame:
        """
        Calculate Leontief inverse (I - A)^(-1)
        
        This captures both direct and indirect requirements
        
        Returns:
            Leontief inverse matrix
        """
        print("\nCalculating Leontief inverse...")
        
        if self.A is None:
            print("  ERROR: Technical coefficients not calculated")
            return None
            
        try:
            # Identity matrix
            I = np.eye(self.A.shape[0])
            
            # (I - A)
            I_minus_A = I - self.A.values
            
            # Check invertibility (all eigenvalues of A should be < 1)
            eigenvalues = np.linalg.eigvals(self.A.values)
            max_eigenvalue = np.max(np.abs(eigenvalues))
            print(f"  Max eigenvalue of A: {max_eigenvalue:.4f}")
            
            if max_eigenvalue >= 1:
                print(f"  WARNING: Matrix may be non-productive (max eigenvalue >= 1)")
                
            # Invert
            L = inv(I_minus_A)
            
            # Convert back to DataFrame
            L_df = pd.DataFrame(
                L,
                index=self.A.index,
                columns=self.A.columns
            )
            
            print(f"  Leontief inverse: {L_df.shape}")
            print(f"  Condition number: {np.linalg.cond(I_minus_A):.2e}")
            
            self.leontief_inverse = L_df
            return L_df
            
        except LinAlgError as e:
            print(f"  ERROR: Matrix inversion failed - {e}")
            return None
            
    def calculate_labor_values(self) -> pd.Series:
        """
        Calculate labor-value coefficients λ*
        
        λ* = hp* · (I - A)^(-1)
        
        This gives the total labor embodied in one dollar of output
        (direct + indirect labor requirements)
        
        Returns:
            Labor values vector
        """
        print("\nCalculating labor values...")
        
        if self.hp_star is None or self.leontief_inverse is None:
            print("  ERROR: hp* or Leontief inverse not calculated")
            return None
            
        # Matrix multiplication: hp* · L
        lambda_star = self.hp_star.values @ self.leontief_inverse.values
        
        # Convert to Series
        lambda_star = pd.Series(
            lambda_star,
            index=self.leontief_inverse.columns,
            name='lambda_star'
        )
        
        print(f"  Labor values: {len(lambda_star)}")
        print(f"  Mean: {lambda_star.mean():.6f} workers/$ output")
        print(f"  Range: [{lambda_star.min():.6f}, {lambda_star.max():.6f}]")
        
        # Labor values should be positive
        negative_count = (lambda_star < 0).sum()
        if negative_count > 0:
            print(f"  WARNING: {negative_count} negative labor values")
            
        self.lambda_star = lambda_star
        return lambda_star
        
    def run_full_calculation(self) -> Dict:
        """
        Run complete I-O calculation pipeline
        
        Returns:
            Dictionary with all results
        """
        print("\n" + "=" * 70)
        print("RUNNING FULL I-O CALCULATION")
        print("=" * 70)
        
        # Load data
        if not self.load_io_table():
            print("FAILED: Could not load I-O table")
            return None
            
        # Calculate components
        self.calculate_technical_coefficients()
        self.calculate_labor_coefficients()
        self.calculate_leontief_inverse()
        self.calculate_labor_values()
        
        results = {
            'year': self.io_table['year'],
            'A': self.A,
            'hp_star': self.hp_star,
            'leontief_inverse': self.leontief_inverse,
            'lambda_star': self.lambda_star
        }
        
        print("\n" + "=" * 70)
        print("CALCULATION COMPLETE")
        print("=" * 70)
        
        return results
        
    def interpolate_non_benchmark_years(self, 
                                       benchmark_results: Dict[int, pd.Series]
                                       ) -> Dict[int, pd.Series]:
        """
        Linear interpolation for non-benchmark years
        
        Args:
            benchmark_results: Dict mapping year -> lambda_star
            
        Returns:
            Dict with annual lambda_star for 1948-1989
        """
        print("\nInterpolating non-benchmark years...")
        
        years = sorted(benchmark_results.keys())
        annual_lambda = {}
        
        # Interpolate between each pair of benchmarks
        for i in range(len(years) - 1):
            y1, y2 = years[i], years[i + 1]
            lambda1 = benchmark_results[y1]
            lambda2 = benchmark_results[y2]
            
            # Add benchmark year
            annual_lambda[y1] = lambda1
            
            # Interpolate intermediate years
            for year in range(y1 + 1, y2):
                weight = (year - y1) / (y2 - y1)
                annual_lambda[year] = lambda1 * (1 - weight) + lambda2 * weight
                
        # Add final benchmark year
        annual_lambda[years[-1]] = benchmark_results[years[-1]]
        
        print(f"  Interpolated: {len(annual_lambda)} years")
        print(f"  Coverage: {min(annual_lambda.keys())}-{max(annual_lambda.keys())}")
        
        return annual_lambda


def process_all_benchmarks(data_dir: str = "Data/Historical_IO") -> Dict[int, Dict]:
    """
    Process all benchmark I-O tables
    
    Args:
        data_dir: Directory containing I-O tables
        
    Returns:
        Dictionary mapping year to results
    """
    data_path = Path(data_dir)
    benchmark_years = [1947, 1958, 1963, 1967, 1972, 1977, 1982]
    
    all_results = {}
    
    print("=" * 70)
    print("PROCESSING ALL BENCHMARK I-O TABLES")
    print("=" * 70)
    
    for year in benchmark_years:
        print(f"\n{'=' * 70}")
        print(f"YEAR: {year}")
        print(f"{'=' * 70}")
        
        io_file = data_path / str(year) / f"use_table_{year}.xlsx"
        
        if not io_file.exists():
            print(f"SKIPPED: File not found - {io_file}")
            continue
            
        calculator = IOMatrixCalculator(io_file)
        results = calculator.run_full_calculation()
        
        if results:
            all_results[year] = results
            
    print("\n" + "=" * 70)
    print("ALL BENCHMARKS PROCESSED")
    print("=" * 70)
    print(f"Successful: {len(all_results)}/{len(benchmark_years)}")
    
    return all_results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process single file
        io_file = Path(sys.argv[1])
        calculator = IOMatrixCalculator(io_file)
        results = calculator.run_full_calculation()
    else:
        # Process all benchmarks
        results = process_all_benchmarks()

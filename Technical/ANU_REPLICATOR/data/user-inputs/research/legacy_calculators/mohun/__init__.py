"""
Mohun Methodology Extension

This module implements Simon Mohun's (2005, 2013) methodology for calculating
productive/unproductive labor and exploitation rates, applied backwards to the
Shaikh-Tonak period (1948-1989).

Key differences from Shaikh-Tonak:
- Simpler classification (BLS industry level, not I-O sectors)
- Class decomposition of unproductive labor (working-class vs managerial)
- Conservation-based calculation of labor value of money
- Direct NIPA approach (less reliance on Leontief inverse)

Modules:
- calculate_employment_mohun: Employment classification
- decompose_unproductive_labor: Class analysis of Lu
- calculate_variable_capital_mohun: Enhanced V* calculation
- calculate_exploitation_mohun: Mohun-style exploitation rate

Author: Shaikh-Tonak Replication Project
Date: October 31, 2025
"""

__version__ = '1.0.0'
__author__ = 'Shaikh-Tonak Replication Project'


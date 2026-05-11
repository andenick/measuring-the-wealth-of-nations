#!/usr/bin/env python3
"""Quick test of Wave 3 components."""
import sys
sys.path.insert(0, ".")

print("Testing L13...")
from scripts.loading.L13_load_comparison import load as l13
r = l13()
print(f"L13: {r['status']} - {r['message']}")

print("Testing L14...")
from scripts.loading.L14_load_gfp_measures import load as l14
r = l14()
print(f"L14: {r['status']} - {r['message']}")

print("Testing P15...")
from scripts.processing.P15_process_comparison import process as p15
r = p15()
print(f"P15: {r['status']}")
for s in r.get("steps", []):
    print(f"  {s}")
print(f"Outputs: {r.get('outputs', [])}")
print("DONE")

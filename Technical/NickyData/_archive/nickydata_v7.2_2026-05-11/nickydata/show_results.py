"""Display final Marxian national accounts results."""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "computed"

t506 = pd.read_csv(DATA / "T506.csv", index_col="year")
t504 = pd.read_csv(DATA / "T504.csv", index_col="year")
t505 = pd.read_csv(DATA / "T505.csv", index_col="year")
t501 = pd.read_csv(DATA / "T501.csv", index_col="year")
t503 = pd.read_csv(DATA / "T503.csv", index_col="year")

print("MARXIAN NATIONAL ACCOUNTS — FINAL RESULTS")
print("=" * 80)
print(f"  {'Year':<6} {'TP*':>10} {'GFP*':>10} {'V*':>9} {'S*':>10} {'e=S*/V*':>8} {'Book e':>8}")
print("-" * 80)
book_e = {1948: 1.70, 1958: 2.01, 1963: 2.07, 1967: 2.10, 1972: 1.99,
           1977: 2.10, 1980: 2.07, 1985: 2.33, 1989: 2.44}
for yr in [1948, 1953, 1958, 1963, 1967, 1972, 1977, 1980, 1985, 1989,
           1997, 2000, 2005, 2007, 2010, 2015, 2017, 2020, 2024]:
    tp = t501.loc[yr, "value"] if yr in t501.index else 0
    gfp = t503.loc[yr, "value"] if yr in t503.index else 0
    v = t504.loc[yr, "value"] if yr in t504.index else 0
    s = t505.loc[yr, "value"] if yr in t505.index else 0
    e = t506.loc[yr, "value"] if yr in t506.index else 0
    be = book_e.get(yr, 0)
    be_str = f"{be:.2f}" if be else "  -"
    print(f"  {yr:<6} {tp:>10,.1f} {gfp:>10,.1f} {v:>9,.1f} {s:>10,.1f} {e:>8.3f} {be_str:>8}")

print()
e48 = t506.loc[1948, "value"] if 1948 in t506.index else 0
e89 = t506.loc[1989, "value"] if 1989 in t506.index else 0
e97 = t506.loc[1997, "value"] if 1997 in t506.index else 0
e24 = t506.loc[2024, "value"] if 2024 in t506.index else 0
v48 = t504.loc[1948, "value"] if 1948 in t504.index else 0
s48 = t505.loc[1948, "value"] if 1948 in t505.index else 0
print(f"  Exploitation rate trajectory:")
print(f"    1948-1989: {e48:.2f} -> {e89:.2f}  (book: 1.70 -> 2.44)")
print(f"    1997-2024: {e97:.2f} -> {e24:.2f}")
print(f"  V*(1948) = {v48:.1f}bn  (book: 88.4)")
print(f"  S*(1948) = {s48:.1f}bn  (book: 149.9)")
print(f"  GFP* source: integrated detail-level IO (412 industries for GO, summary for VA)")

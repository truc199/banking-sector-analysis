import pandas as pd
import numpy as np

bs_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")

for col in inc_df.columns:
    if col not in ['Công ty', 'Năm']:
        inc_df[col] = pd.to_numeric(inc_df[col], errors='coerce').fillna(0)

for col in bs_df.columns:
    if col not in ['Công ty', 'Năm']:
        bs_df[col] = pd.to_numeric(bs_df[col], errors='coerce').fillna(0)

m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm'])

# Filter 2024
gd3_24 = m_df[m_df['Năm'] == 2024].copy()

# Compute ROA
gd3_24['ROA'] = gd3_24['B22'] / gd3_24['A1'] * 100

# Compute Fee/TOI: B6 (Fee Income) / B14 (TOI) * 100
gd3_24['Fee_TOI'] = np.where(gd3_24['B14'] > 0, gd3_24['B6'] / gd3_24['B14'] * 100, 0)
gd3_24['Fee_Assets'] = gd3_24['B6'] / gd3_24['A1'] * 100

print("Correlations in 2024:")
print(f"  Fee/TOI vs ROA: {gd3_24['Fee_TOI'].corr(gd3_24['ROA']):.4f}")
print(f"  Fee/Assets vs ROA: {gd3_24['Fee_Assets'].corr(gd3_24['ROA']):.4f}")

# Excluding NH22
gd3_24_no22 = gd3_24[gd3_24['Công ty'] != 22]
print("\nCorrelations in 2024 (Excluding NH22):")
print(f"  Fee/TOI vs ROA: {gd3_24_no22['Fee_TOI'].corr(gd3_24_no22['ROA']):.4f}")
print(f"  Fee/Assets vs ROA: {gd3_24_no22['Fee_Assets'].corr(gd3_24_no22['ROA']):.4f}")

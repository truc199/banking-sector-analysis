import pandas as pd
import numpy as np
import glob

# Find files
BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
IS_FILE   = glob.glob(r'd:\uni\gcontest\*Income*')[0]
NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]

bs = pd.read_csv(BS_FILE)
ic = pd.read_csv(IS_FILE)
note = pd.read_csv(NOTE_FILE)

# Merge
m = bs.merge(ic, on=['Công ty', 'Năm'], how='inner')
m = m.merge(note, on=['Công ty', 'Năm'], how='inner')

for c in m.columns:
    if c not in ['Công ty', 'Năm']:
        m[c] = pd.to_numeric(m[c], errors='coerce')

# Filter 2024
m24 = m[m['Năm'] == 2024].copy()

# Calculate NPL
npl_sum = m24[['C35','C36','C37']].sum(axis=1)
m24['NPL'] = (npl_sum / m24['A13']) * 100

# Calculate LLR Coverage
m24['LLR'] = (m24['A14'].abs() / npl_sum) * 100

# Calculate Fee/TOI
m24['Fee_TOI'] = (m24['B6'] / m24['B14']) * 100

# Print info
print("=== NPL vs LLR Coverage in 2024 ===")
coverage_info = m24[['Công ty', 'NPL', 'LLR']].sort_values('LLR').reset_index(drop=True)
print(coverage_info)
num_cov_under_100 = (coverage_info['LLR'] < 100).sum()
print(f"Number of banks with LLR Coverage < 100%: {num_cov_under_100}")

print("\n=== Fee/TOI in 2024 ===")
fee_info = m24[['Công ty', 'Fee_TOI']].sort_values('Fee_TOI', ascending=False).reset_index(drop=True)
print(fee_info)
print(f"Simple average Fee/TOI: {m24['Fee_TOI'].mean():.2f}%")
weighted_average_fee = (m24['B6'].sum() / m24['B14'].sum()) * 100
print(f"Weighted average Fee/TOI: {weighted_average_fee:.2f}%")

# Save data for reference
m24[['Công ty', 'NPL', 'LLR', 'Fee_TOI']].to_csv(r'C:\Users\trucf\.gemini\antigravity\brain\b0209876-ba40-47cd-abaa-b115042dc623\scratch\slide_15_data.csv', index=False)

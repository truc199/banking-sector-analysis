import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
n_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]

bs = pd.read_csv(bs_file)
note = pd.read_csv(n_file)

years = [2020, 2021, 2022, 2023, 2024]
bs_y = bs[bs['Năm'].isin(years)]
note_y = note[note['Năm'].isin(years)]

df = pd.merge(bs_y[['Công ty', 'Năm', 'A14', 'A12']], note_y[['Công ty', 'Năm', 'C32', 'C35', 'C36', 'C37']], on=['Công ty', 'Năm'])
df['NPL_Amount'] = df['C35'] + df['C36'] + df['C37']
df['NPL_Ratio'] = df['NPL_Amount'] / df['C32'] * 100
df['LLR'] = abs(df['A14']) / df['NPL_Amount'] * 100

print("--- 5.1 NPL Trend ---")
print("System average NPL Ratio:")
for y in years:
    sub = df[df['Năm'] == y]
    mean_val = sub['NPL_Ratio'].mean()
    print(f"  {y}: {mean_val:.2f}%")

print("System weighted average NPL Ratio:")
for y in years:
    sub = df[df['Năm'] == y]
    weighted_val = sub['NPL_Amount'].sum() / sub['C32'].sum() * 100
    print(f"  {y}: {weighted_val:.2f}%")

print("\n--- 5.2 LLR Dispersion (2024) ---")
df_2024 = df[df['Năm'] == 2024].dropna(subset=['LLR'])

under_100 = len(df_2024[df_2024['LLR'] < 100])
over_150 = len(df_2024[df_2024['LLR'] > 150])
total_banks = len(df_2024)

print(f"Total banks with LLR data in 2024: {total_banks}")
print(f"Banks with LLR < 100%: {under_100}")
print(f"Banks with LLR > 150%: {over_150}")

# Also let's prepare the scorecard values
# We need 2024 means for ROA, ROE, NIM, CIR, NPL, LDR, CASA
inc_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
inc = pd.read_csv(inc_file)
inc_24 = inc[inc['Năm'] == 2024]
bs_24 = bs[bs['Năm'] == 2024]
note_24 = note[note['Năm'] == 2024]

# Merge all
m24 = pd.merge(bs_24[['Công ty', 'A50', 'A73', 'A12', 'A55']], inc_24[['Công ty', 'B22', 'B3', 'B14', 'B15']], on='Công ty')
m24 = pd.merge(m24, note_24[['Công ty', 'C32', 'C35', 'C36', 'C37', 'C68']], on='Công ty')

m24['ROA'] = m24['B22'] / m24['A50'] * 100 # Approx A50 total assets
# Wait, Total Asset is A1. A50 is Total Liabilities. A73 is Total Equity.
m24_bs = bs_24[['Công ty', 'A1']]
m24 = pd.merge(m24, m24_bs, on='Công ty')
m24['ROA'] = m24['B22'] / m24['A1'] * 100
m24['ROE'] = m24['B22'] / m24['A73'] * 100
m24['NIM'] = m24['B3'] / m24['A1'] * 100 # Should use avg earning assets, A1 is proxy
m24['CIR'] = abs(m24['B15']) / m24['B14'] * 100
m24['NPL'] = (m24['C35'] + m24['C36'] + m24['C37']) / m24['C32'] * 100
m24['LDR'] = m24['A12'] / m24['A55'] * 100
m24['CASA'] = m24['C68'] / m24['A55'] * 100

print("\n--- Key Takeaway Scorecard (2024 System Mean) ---")
print(f"ROA: {m24['ROA'].mean():.2f}%")
print(f"ROE: {m24['ROE'].mean():.2f}%")
print(f"NIM: {m24['NIM'].mean():.2f}%")
# CIR excluding NH22
cir_val = m24[m24['Công ty'] != 22]['CIR'].mean()
print(f"CIR: {cir_val:.2f}%")
print(f"NPL: {m24['NPL'].mean():.2f}%")
print(f"LDR: {m24['LDR'].mean():.2f}%")
print(f"CASA: {m24['CASA'].mean():.2f}%")

import pandas as pd
import numpy as np
import glob
import scipy.stats as stats

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
n_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]
inc_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]

bs = pd.read_csv(bs_file)
note = pd.read_csv(n_file)
inc = pd.read_csv(inc_file)

# We analyze year 2021 for Giai đoạn 1
y21_bs = bs[bs['Năm'] == 2021]
y21_note = note[note['Năm'] == 2021]
y21_inc = inc[inc['Năm'] == 2021]

df = pd.merge(y21_bs[['Công ty', 'A1', 'A55', 'A50']], y21_inc[['Công ty', 'B3', 'B4', 'B22']], on='Công ty')
df = pd.merge(df, y21_note[['Công ty', 'C68']], on='Công ty')

# Calculations
df['CASA'] = df['C68'] / df['A55'] * 100
df['NIM'] = df['B3'] / df['A1'] * 100
df['ROA'] = df['B22'] / df['A1'] * 100
df['CoF'] = abs(df['B4']) / df['A50'] * 100 # Approx using Total Liabilities A50

print("--- Data Check for 2021 ---")
print(f"CASA Range: {df['CASA'].min():.2f}% to {df['CASA'].max():.2f}%")
print(f"CoF Range: {df['CoF'].min():.2f}% to {df['CoF'].max():.2f}%")
print(f"NIM Range: {df['NIM'].min():.2f}% to {df['NIM'].max():.2f}%")

# Correlation
r_casa_cof, p1 = stats.pearsonr(df['CASA'], df['CoF'])
r_casa_nim, p2 = stats.pearsonr(df['CASA'], df['NIM'])
r_casa_roa, p3 = stats.pearsonr(df['CASA'], df['ROA'])

print(f"CASA vs CoF: r = {r_casa_cof:.3f}, R2 = {r_casa_cof**2:.3f}")
print(f"CASA vs NIM: r = {r_casa_nim:.3f}, p = {p2:.3f}")
print(f"CASA vs ROA: r = {r_casa_roa:.3f}, p = {p3:.3f}")

print("\n--- Specific Banks ---")
for b in [7, 6, 4, 20, 24, 21]:
    b_data = df[df['Công ty'] == b]
    if not b_data.empty:
        print(f"NH{b}: CASA {b_data['CASA'].values[0]:.1f}%, CoF {b_data['CoF'].values[0]:.2f}%, NIM {b_data['NIM'].values[0]:.1f}%, ROA {b_data['ROA'].values[0]:.1f}%")

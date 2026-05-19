import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
is_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)

years = [2020, 2021, 2022, 2023, 2024]

# ── Slide 3.1: Income Diversification ──
# Non-interest income = TOI (B14) - Net Interest Income (B3)
# Fee Income (net) = B6
inc_y = inc[inc['Năm'].isin(years)].copy()

# System aggregates per year
agg = inc_y.groupby('Năm').agg({
    'B3': 'sum',   # Net Interest Income
    'B6': 'sum',   # Net Fee Income
    'B14': 'sum',  # TOI
    'B15': 'sum',  # Operating Expenses (OPEX)
}).reindex(years)

agg['Non_Interest'] = agg['B14'] - agg['B3']
agg['Non_Interest_Ratio'] = agg['Non_Interest'] / agg['B14'] * 100
agg['Fee_Ratio'] = agg['B6'] / agg['B14'] * 100
agg['Interest_Ratio'] = agg['B3'] / agg['B14'] * 100

print('=== Thu nhập ngoài lãi / TOI ===')
for y in years:
    print(f'  {y}: Non-Interest Ratio = {agg.loc[y,"Non_Interest_Ratio"]:.2f}%, Fee Ratio = {agg.loc[y,"Fee_Ratio"]:.2f}%, Interest Ratio = {agg.loc[y,"Interest_Ratio"]:.2f}%')

# ── Slide 3.2: CIR ──
# CIR per bank = OPEX (B15) / TOI (B14) * 100
merged = inc_y[['Công ty', 'Năm', 'B14', 'B15']].copy()
merged['CIR'] = merged['B15'] / merged['B14'] * 100

cir_avg = merged.groupby('Năm')['CIR'].mean().reindex(years)
print('\n=== CIR trung bình hệ thống ===')
for y in years:
    print(f'  {y}: {cir_avg[y]:.2f}%')

# CIR dispersion 2024
cir_2024 = merged[merged['Năm'] == 2024][['Công ty', 'CIR']].sort_values('CIR')
print(f'\n=== CIR Dispersion (2024) ===')
print(f'  Max: {cir_2024["CIR"].max():.2f}% | Min: {cir_2024["CIR"].min():.2f}%')
print(f'  Gap: {cir_2024["CIR"].max() - cir_2024["CIR"].min():.2f}pp')

print(f'\n=== Top 5 CIR (worst) ===')
for _, row in cir_2024.tail(5).iloc[::-1].iterrows():
    print(f'  NH {int(row["Công ty"])}: {row["CIR"]:.2f}%')
print(f'\n=== Bottom 5 CIR (best) ===')
for _, row in cir_2024.head(5).iterrows():
    print(f'  NH {int(row["Công ty"])}: {row["CIR"]:.2f}%')

# Check CIR gap by year
print(f'\n=== CIR Gap by year ===')
for y in years:
    cir_y = merged[merged['Năm'] == y]['CIR']
    print(f'  {y}: Gap = {cir_y.max() - cir_y.min():.2f}pp (Max={cir_y.max():.2f}%, Min={cir_y.min():.2f}%)')

# Breakdown: non-interest components
print('\n=== Non-interest components (system sum, by year) ===')
for y in years:
    inc_yr = inc_y[inc_y['Năm'] == y]
    toi = inc_yr['B14'].sum()
    fee = inc_yr['B6'].sum()
    fx = inc_yr['B7'].sum()
    sec_trade = inc_yr['B8'].sum()
    sec_inv = inc_yr['B9'].sum()
    other = inc_yr['B12'].sum()
    equity_inv = inc_yr['B13'].sum()
    print(f'  {y}: Fee={fee/toi*100:.2f}%, FX={fx/toi*100:.2f}%, SecTrade={sec_trade/toi*100:.2f}%, SecInv={sec_inv/toi*100:.2f}%, Other={other/toi*100:.2f}%, EquityInv={equity_inv/toi*100:.2f}%')

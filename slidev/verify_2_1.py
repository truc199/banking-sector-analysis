import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

# Load data
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
is_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)

years = [2020, 2021, 2022, 2023, 2024]

# Merge: Net Income (B22) from Income Statement, Total Assets (A1) & Equity (A64) from Balance Sheet
merged = pd.merge(
    bs[['Công ty', 'Năm', 'A1', 'A64']],
    inc[['Công ty', 'Năm', 'B22']],
    on=['Công ty', 'Năm']
)
merged = merged[merged['Năm'].isin(years)].copy()

# ROA = Net Income / Total Assets * 100
# ROE = Net Income / Equity * 100
merged['ROA'] = merged['B22'] / merged['A1'] * 100
merged['ROE'] = merged['B22'] / merged['A64'] * 100

# ── System average by year ──
roa_avg = merged.groupby('Năm')['ROA'].mean().reindex(years)
roe_avg = merged.groupby('Năm')['ROE'].mean().reindex(years)

print('=== ROA trung bình hệ thống ===')
for y in years:
    print(f'  {y}: {roa_avg[y]:.2f}%')
print(f'  Mean across years: {roa_avg.mean():.2f}%')

print('\n=== ROE trung bình hệ thống ===')
for y in years:
    print(f'  {y}: {roe_avg[y]:.2f}%')
print(f'  Mean across years: {roe_avg.mean():.2f}%')

# ── ROE Dispersion in 2024 ──
roe_2024 = merged[merged['Năm'] == 2024]['ROE']
roa_2024 = merged[merged['Năm'] == 2024]['ROA']
print(f'\n=== ROE Dispersion (2024) ===')
print(f'  Max: {roe_2024.max():.2f}% | Min: {roe_2024.min():.2f}%')
print(f'  Gap: {roe_2024.max() - roe_2024.min():.2f}pp')

# Check max ROE gap across all years
print(f'\n=== ROE Dispersion by year ===')
for y in years:
    roe_y = merged[merged['Năm'] == y]['ROE']
    gap = roe_y.max() - roe_y.min()
    print(f'  {y}: Max={roe_y.max():.2f}%, Min={roe_y.min():.2f}%, Gap={gap:.2f}pp')

# Top/Bottom banks by ROE in 2024
roe_banks = merged[merged['Năm'] == 2024][['Công ty', 'ROE']].sort_values('ROE')
print(f'\n=== Top 5 ROE (2024) ===')
for _, row in roe_banks.tail(5).iloc[::-1].iterrows():
    print(f'  NH {int(row["Công ty"])}: {row["ROE"]:.2f}%')
print(f'\n=== Bottom 5 ROE (2024) ===')
for _, row in roe_banks.head(5).iterrows():
    print(f'  NH {int(row["Công ty"])}: {row["ROE"]:.2f}%')

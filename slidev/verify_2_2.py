import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
is_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)

years = [2020, 2021, 2022, 2023, 2024]

merged = pd.merge(
    bs[['Công ty', 'Năm', 'A1']],
    inc[['Công ty', 'Năm', 'B3']],
    on=['Công ty', 'Năm']
)
merged = merged[merged['Năm'].isin(years)].copy()

# NIM = Net Interest Income / Total Assets * 100
merged['NIM'] = merged['B3'] / merged['A1'] * 100

# System average NIM per year
nim_avg = merged.groupby('Năm')['NIM'].mean().reindex(years)
print('=== NIM trung bình hệ thống ===')
for y in years:
    print(f'  {y}: {nim_avg[y]:.2f}%')

# Count banks with NIM decline 2022->2024
nim_2022 = merged[merged['Năm'] == 2022].set_index('Công ty')['NIM']
nim_2024 = merged[merged['Năm'] == 2024].set_index('Công ty')['NIM']
nim_change = nim_2024 - nim_2022
declined = (nim_change < 0).sum()
total = len(nim_change)
print(f'\nNIM decline 2022->2024: {declined}/{total} banks ({declined/total*100:.1f}%)')

# NIM per bank for all years (for grouped line chart)
print('\n=== NIM per bank (2024) ===')
nim_2024_df = merged[merged['Năm'] == 2024][['Công ty', 'NIM']].sort_values('NIM', ascending=False)
for _, row in nim_2024_df.iterrows():
    chg = nim_change.get(row['Công ty'], 0)
    flag = '▼' if chg < 0 else '▲'
    print(f'  NH {int(row["Công ty"]):2d}: {row["NIM"]:.2f}%  ({flag} {chg:+.2f}pp vs 2022)')

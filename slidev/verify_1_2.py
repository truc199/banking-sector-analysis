import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

years = [2020, 2021, 2022, 2023, 2024]

vdl_by_year  = bs_5y.groupby('Năm')['A66'].sum().reindex(years)
vcsh_by_year = bs_5y.groupby('Năm')['A64'].sum().reindex(years)
tts_by_year  = bs_5y.groupby('Năm')['A1'].sum().reindex(years)

bs_5y['equity_ratio'] = bs_5y['A64'] / bs_5y['A1'] * 100
mean_er_by_year = bs_5y.groupby('Năm')['equity_ratio'].mean().reindex(years)
weighted_er = (vcsh_by_year / tts_by_year * 100)

print('=== VDL (nghìn tỷ VND) ===')
for y in years:
    print(f'  {y}: {vdl_by_year[y]/1000:.2f}')

print('\n=== VCSH (nghìn tỷ VND) ===')
for y in years:
    print(f'  {y}: {vcsh_by_year[y]/1000:.2f}')

print('\n=== Equity/TTS - Simple Mean (%) ===')
for y in years:
    print(f'  {y}: {mean_er_by_year[y]:.2f}%')

print('\n=== Equity/TTS - Weighted (%) ===')
for y in years:
    print(f'  {y}: {weighted_er[y]:.2f}%')

bs_2024 = bs_5y[bs_5y['Năm'] == 2024]
low_equity = bs_2024[bs_2024['equity_ratio'] < 6.0]
print(f'\nBanks with Equity/TTS < 6% in 2024: {len(low_equity)}')
for _, row in low_equity.sort_values('equity_ratio').iterrows():
    bank_id = int(row['Công ty'])
    er = row['equity_ratio']
    print(f'  NH {bank_id}: {er:.2f}%')

# Also check 2020 data
bs_2020 = bs_5y[bs_5y['Năm'] == 2020]
low_equity_2020 = bs_2020[bs_2020['equity_ratio'] < 6.0]
print(f'\nBanks with Equity/TTS < 6% in 2020: {len(low_equity_2020)}')

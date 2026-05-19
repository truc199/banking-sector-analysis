import glob
import pandas as pd
import numpy as np

# Find Balance Sheet file
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

years = [2020, 2021, 2022, 2023, 2024]

vdl_by_year  = bs_5y.groupby('Năm')['A66'].sum().reindex(years)
vcsh_by_year = bs_5y.groupby('Năm')['A64'].sum().reindex(years)
tts_by_year  = bs_5y.groupby('Năm')['A1'].sum().reindex(years)

# Industry weighted average Equity/TTS
weighted_equity_ratio = (vcsh_by_year / tts_by_year * 100)

print("--- Weighted Equity/TTS ratio by year (Industry Total) ---")
for y in years:
    print(f"Year {y}: {weighted_equity_ratio[y]:.4f}%")

# Individual banks in 2024
bs_2024 = bs_5y[bs_5y['Năm'] == 2024].copy()
bs_2024['equity_ratio'] = bs_2024['A64'] / bs_2024['A1'] * 100

print("\n--- Individual Bank Equity/TTS ratios in 2024 ---")
sorted_2024 = bs_2024.sort_values('equity_ratio')
for idx, row in sorted_2024.iterrows():
    print(f"NH {int(row['Công ty'])}: {row['equity_ratio']:.4f}%")

below_6 = sorted_2024[sorted_2024['equity_ratio'] < 6.0]
print(f"\nNumber of banks with Equity/TTS < 6%: {len(below_6)}")
for idx, row in below_6.iterrows():
    print(f"  NH {int(row['Công ty'])}: {row['equity_ratio']:.4f}%")

max_er = sorted_2024['equity_ratio'].max()
min_er = sorted_2024['equity_ratio'].min()
spread = max_er - min_er
print(f"\nMax Equity/TTS: {max_er:.4f}%")
print(f"Min Equity/TTS: {min_er:.4f}%")
print(f"Spread (Max - Min): {spread:.4f} pp")

import pandas as pd
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Find files
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
note_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]
inc_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]

bs = pd.read_csv(bs_file)
note = pd.read_csv(note_file)
inc = pd.read_csv(inc_file)

# Merged dataset for 2020-2021
merged = bs.merge(inc, on=['Công ty', 'Năm']).merge(note, on=['Công ty', 'Năm'])
merged = merged[merged['Năm'].isin([2020, 2021])]

# Let's see VAMC columns (C64)
# Filter banks that have C64 > 0 in either 2020 or 2021
vamc_banks = merged[merged['C64'] > 0][['Công ty', 'Năm', 'C64']]
print("VAMC banks:")
print(vamc_banks.to_string())

# Calculate NPL and Watch-list (Nhóm 2)
# NPL = (C35 + C36 + C37) / A13 * 100
# Watchlist = C34 / A13 * 100
merged['npl_ratio'] = (merged['C35'] + merged['C36'] + merged['C37']) / merged['A13'] * 100
merged['watch_ratio'] = merged['C34'] / merged['A13'] * 100

print("\nYearly Averages:")
print(merged.groupby('Năm')[['npl_ratio', 'watch_ratio']].mean())

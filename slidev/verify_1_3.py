import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_2024 = bs[bs['Năm'] == 2024].copy()
bs_2024['equity_ratio'] = bs_2024['A64'] / bs_2024['A1'] * 100
bs_2024 = bs_2024.sort_values('equity_ratio', ascending=True)

print('=== EQUITY RATIO BY BANK (2024), sorted ascending ===')
for _, row in bs_2024.iterrows():
    bank_id = int(row['Công ty'])
    er = row['equity_ratio']
    flag = ' *** BELOW 6% ***' if er < 6.0 else ''
    print(f'  NH {bank_id:2d}: {er:6.2f}%{flag}')

max_er = bs_2024['equity_ratio'].max()
min_er = bs_2024['equity_ratio'].min()
spread = max_er - min_er
mean_er = bs_2024['equity_ratio'].mean()
median_er = bs_2024['equity_ratio'].median()

print(f'\nMax: {max_er:.2f}% | Min: {min_er:.2f}% | Spread: {spread:.2f}pp')
print(f'Mean: {mean_er:.2f}% | Median: {median_er:.2f}%')
print(f'Banks below 6%: {len(bs_2024[bs_2024["equity_ratio"] < 6.0])}')

# Check the top and bottom groups
print(f'\nTop 5 banks:')
for _, row in bs_2024.tail(5).iloc[::-1].iterrows():
    print(f'  NH {int(row["Công ty"]):2d}: {row["equity_ratio"]:.2f}%')

print(f'\nBottom 5 banks:')
for _, row in bs_2024.head(5).iterrows():
    print(f'  NH {int(row["Công ty"]):2d}: {row["equity_ratio"]:.2f}%')

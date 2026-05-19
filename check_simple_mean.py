import glob
import pandas as pd

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

bs_5y['equity_ratio'] = bs_5y['A64'] / bs_5y['A1'] * 100

for y in [2020, 2024]:
    sub = bs_5y[bs_5y['Năm'] == y]
    simple_mean = sub['equity_ratio'].mean()
    print(f"Simple Mean {y}: {simple_mean:.4f}%")

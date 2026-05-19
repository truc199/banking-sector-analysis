import pandas as pd
import numpy as np

bs_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")

for col in inc_df.columns:
    if col not in ['Công ty', 'Năm']:
        inc_df[col] = pd.to_numeric(inc_df[col], errors='coerce').fillna(0)

for col in bs_df.columns:
    if col not in ['Công ty', 'Năm']:
        bs_df[col] = pd.to_numeric(bs_df[col], errors='coerce').fillna(0)

m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm'])
gd2 = m_df[m_df['Năm'].isin([2022, 2023])].copy()

# Fee Ratio
gd2['Fee_Ratio'] = gd2['B6'] / gd2['B14'] * 100
gd2['ROA'] = gd2['B22'] / gd2['A1'] * 100

print("Fee_Ratio vs ROA correlation by year:")
for yr in [2022, 2023]:
    sub = gd2[gd2['Năm'] == yr]
    print(f"  {yr}: {sub['Fee_Ratio'].corr(sub['ROA']):.4f}")

# Excluding NH22
gd2_no22 = gd2[gd2['Công ty'] != 22].copy()
print("\nExcluding NH22 correlation by year:")
for yr in [2022, 2023]:
    sub = gd2_no22[gd2_no22['Năm'] == yr]
    print(f"  {yr}: {sub['Fee_Ratio'].corr(sub['ROA']):.4f}")
print(f"  GD2 overall without NH22: {gd2_no22['Fee_Ratio'].corr(gd2_no22['ROA']):.4f}")

# Let's check leverage and ROE excluding NH22
gd2_no22['Leverage'] = gd2_no22['A1'] / gd2_no22['A64']
gd2_no22['ROE'] = gd2_no22['B22'] / gd2_no22['A64'] * 100

gd2_no22_avg = gd2_no22.groupby('Công ty')[['Leverage', 'ROE']].mean().reset_index()
median_lev = gd2_no22_avg['Leverage'].median()
low_lev = gd2_no22_avg[gd2_no22_avg['Leverage'] <= median_lev]
high_lev = gd2_no22_avg[gd2_no22_avg['Leverage'] > median_lev]
print(f"\nWithout NH22 - Median Leverage: {median_lev:.2f}")
print(f"Low Leverage Group Mean ROE: {low_lev['ROE'].mean():.2f}%")
print(f"High Leverage Group Mean ROE: {high_lev['ROE'].mean():.2f}%")
print(f"Difference: {low_lev['ROE'].mean() - high_lev['ROE'].mean():.2f}pp")

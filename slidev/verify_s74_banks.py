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
gd2_23 = m_df[m_df['Năm'] == 2023].copy()

gd2_23['ROA'] = gd2_23['B22'] / gd2_23['A1'] * 100
gd2_23['Leverage'] = gd2_23['A1'] / gd2_23['A64']
gd2_23['ROE'] = gd2_23['B22'] / gd2_23['A64'] * 100
gd2_23['NII_Asset'] = gd2_23['B3'] / gd2_23['A1'] * 100
gd2_23['Fee_Asset'] = gd2_23['B6'] / gd2_23['A1'] * 100
gd2_23['OPEX_Asset'] = gd2_23['B15'] / gd2_23['A1'] * 100
gd2_23['Prov_Asset'] = gd2_23['B17'] / gd2_23['A1'] * 100
gd2_23['Other_Asset'] = gd2_23['B12'] / gd2_23['A1'] * 100  # Other net income (B12)

# Find banks with Leverage > 12.0 and ROE > 10%
candidates = gd2_23[(gd2_23['Leverage'] > 12.0) & (gd2_23['ROE'] > 8.0)].copy()
print(candidates[['Công ty', 'NII_Asset', 'Fee_Asset', 'Other_Asset', 'OPEX_Asset', 'Prov_Asset', 'ROA', 'Leverage', 'ROE']].sort_values('Leverage', ascending=False).to_string(index=False))

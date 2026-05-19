import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

note_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_3. Note.csv")
bs_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")

cols = ['C33', 'C34', 'C35', 'C36', 'C37']
for col in cols:
    note_df[col] = pd.to_numeric(note_df[col], errors='coerce').fillna(0)

note_df['Total_Loans'] = note_df[cols].sum(axis=1)
note_df['NPL_Amount'] = note_df['C35'] + note_df['C36'] + note_df['C37']
note_df['NPL_Ratio'] = note_df['NPL_Amount'] / note_df['Total_Loans'] * 100
note_df['C34_Ratio'] = note_df['C34'] / note_df['Total_Loans'] * 100

merged = note_df.merge(bs_df, on=['Công ty', 'Năm']).merge(inc_df, on=['Công ty', 'Năm'])
merged['ROA'] = merged['B22'] / merged['A1'] * 100

# Average over Phase 2 (2022-2023)
phase2 = merged[merged['Năm'].isin([2022, 2023])]
grouped = phase2.groupby('Công ty')[['NPL_Ratio', 'ROA']].mean().reset_index()
corr_p2 = grouped['NPL_Ratio'].corr(grouped['ROA'])
print(f"Correlation between Phase 2 average NPL and ROA: {corr_p2:.4f}")

# Average over Phase 1 (2020-2021)
phase1 = merged[merged['Năm'].isin([2020, 2021])]
grouped_p1 = phase1.groupby('Công ty')[['NPL_Ratio', 'ROA']].mean().reset_index()
corr_p1 = grouped_p1['NPL_Ratio'].corr(grouped_p1['ROA'])
print(f"Correlation between Phase 1 average NPL and ROA: {corr_p1:.4f}")

# NPL in 2023 for individual banks
note_2023 = note_df[note_df['Năm'] == 2023]
print("\nIndividual bank NPLs in 2023:")
for bank in [22, 8, 15, 4, 7, 20]:
    row = note_2023[note_2023['Công ty'] == bank]
    print(f"NH{bank}: NPL = {row['NPL_Ratio'].values[0]:.2f}%")

# NPL in Phase 2 average for individual banks
gd2 = note_df[note_df['Năm'].isin([2022, 2023])].copy()
grouped_gd2 = gd2.groupby('Công ty')[['NPL_Ratio', 'C34_Ratio']].mean().reset_index()
print("\nIndividual bank NPLs (Phase 2 averages):")
for bank in [22, 8, 15, 4, 7, 20]:
    row = grouped_gd2[grouped_gd2['Công ty'] == bank]
    print(f"NH{bank}: NPL = {row['NPL_Ratio'].values[0]:.2f}%")

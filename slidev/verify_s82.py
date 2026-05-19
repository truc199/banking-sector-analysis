import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

bs_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
note_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_3. Note.csv")

for df in [bs_df, inc_df, note_df]:
    for col in df.columns:
        if col not in ['Công ty', 'Năm']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Merge
m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm'])

# Clean note columns to compute NPL and CASA
# NPL Ratio
cols = ['C33', 'C34', 'C35', 'C36', 'C37']
note_df['Total_Loans'] = note_df[cols].sum(axis=1)
note_df['NPL_Amount'] = note_df['C35'] + note_df['C36'] + note_df['C37']
note_df['NPL_Ratio'] = np.where(note_df['Total_Loans'] > 0, note_df['NPL_Amount'] / note_df['Total_Loans'] * 100, 0)

# CASA Ratio = C68 / (C68 + C69 + C70 + C71 + C72) * 100
dep_cols = ['C68', 'C69', 'C70', 'C71', 'C72']
note_df['Total_Dep'] = note_df[dep_cols].sum(axis=1)
note_df['CASA_Ratio'] = np.where(note_df['Total_Dep'] > 0, note_df['C68'] / note_df['Total_Dep'] * 100, 0)

# Merge back
m_df = m_df.merge(note_df[['Công ty', 'Năm', 'NPL_Ratio', 'CASA_Ratio']], on=['Công ty', 'Năm'], how='left')
m_df['ROA'] = m_df['B22'] / m_df['A1'] * 100

# Compute for Phase 1 (2020-2021 avg), Phase 2 (2022-2023 avg), Phase 3 (2024)
p1 = m_df[m_df['Năm'].isin([2020, 2021])].groupby('Công ty')[['NPL_Ratio', 'CASA_Ratio', 'ROA']].mean().reset_index()
p2 = m_df[m_df['Năm'].isin([2022, 2023])].groupby('Công ty')[['NPL_Ratio', 'CASA_Ratio', 'ROA']].mean().reset_index()
p3 = m_df[m_df['Năm'] == 2024][['Công ty', 'NPL_Ratio', 'CASA_Ratio', 'ROA']].copy()

print("Phase 1 correlations:")
print(f"  CASA vs ROA: {p1['CASA_Ratio'].corr(p1['ROA']):.4f}")
print(f"  NPL vs ROA: {p1['NPL_Ratio'].corr(p1['ROA']):.4f}")

print("\nPhase 2 correlations:")
print(f"  CASA vs ROA: {p2['CASA_Ratio'].corr(p2['ROA']):.4f}")
print(f"  NPL vs ROA: {p2['NPL_Ratio'].corr(p2['ROA']):.4f}")

print("\nPhase 3 correlations:")
print(f"  CASA vs ROA: {p3['CASA_Ratio'].corr(p3['ROA']):.4f}")
print(f"  NPL vs ROA: {p3['NPL_Ratio'].corr(p3['ROA']):.4f}")

# Excluding NH22 in Phase 3
p3_no22 = p3[p3['Công ty'] != 22]
print("\nPhase 3 correlations (Excluding NH22):")
print(f"  CASA vs ROA: {p3_no22['CASA_Ratio'].corr(p3_no22['ROA']):.4f}")
print(f"  NPL vs ROA: {p3_no22['NPL_Ratio'].corr(p3_no22['ROA']):.4f}")

# Print NH22 values in 2024
print("\nNH22 in 2024:")
print(p3[p3['Công ty'] == 22])

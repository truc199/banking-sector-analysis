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

# Merge BS and Income
m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm'])

# Clean note columns to compute NPL
cols = ['C33', 'C34', 'C35', 'C36', 'C37']
note_df['Total_Loans'] = note_df[cols].sum(axis=1)
note_df['NPL_Amount'] = note_df['C35'] + note_df['C36'] + note_df['C37']
note_df['NPL_Ratio'] = np.where(note_df['Total_Loans'] > 0, note_df['NPL_Amount'] / note_df['Total_Loans'] * 100, 0)

# Merge Note NPL with m_df
m_df = m_df.merge(note_df[['Công ty', 'Năm', 'NPL_Ratio']], on=['Công ty', 'Năm'], how='left')

# Calculate ROA
m_df['ROA'] = m_df['B22'] / m_df['A1'] * 100

print("Yearly Simple Averages for 27 banks:")
for yr in [2020, 2021, 2022, 2023, 2024]:
    sub = m_df[m_df['Năm'] == yr]
    print(f"  {yr}: ROA={sub['ROA'].mean():.3f}%, NPL={sub['NPL_Ratio'].mean():.3f}%")

print("\nYearly Weighted Averages (System-wide):")
for yr in [2020, 2021, 2022, 2023, 2024]:
    sub = m_df[m_df['Năm'] == yr]
    total_assets = sub['A1'].sum()
    total_profit = sub['B22'].sum()
    
    sub_note = note_df[note_df['Năm'] == yr]
    total_loans = sub_note['Total_Loans'].sum()
    total_npl = sub_note['NPL_Amount'].sum()
    
    sys_roa = (total_profit / total_assets) * 100 if total_assets > 0 else 0
    sys_npl = (total_npl / total_loans) * 100 if total_loans > 0 else 0
    print(f"  {yr}: ROA={sys_roa:.3f}%, NPL={sys_npl:.3f}%")

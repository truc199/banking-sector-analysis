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

# Filter 2024
gd3_24 = m_df[m_df['Năm'] == 2024].copy()

gd3_24['ROA'] = gd3_24['B22'] / gd3_24['A1'] * 100
gd3_24['Leverage'] = gd3_24['A1'] / gd3_24['A64']
gd3_24['ROE'] = gd3_24['B22'] / gd3_24['A64'] * 100
gd3_24['Margin'] = np.where(gd3_24['B14'] > 0, gd3_24['B22'] / gd3_24['B14'] * 100, 0) # Net profit / TOI (Margin)

# Group by leverage median
med_lev = gd3_24['Leverage'].median()
low_lev = gd3_24[gd3_24['Leverage'] <= med_lev]
high_lev = gd3_24[gd3_24['Leverage'] > med_lev]

print(f"Leverage Median: {med_lev:.4f}")
print(f"Low Leverage Group Mean ROE: {low_lev['ROE'].mean():.2f}%")
print(f"High Leverage Group Mean ROE: {high_lev['ROE'].mean():.2f}%")
print(f"Difference: {low_lev['ROE'].mean() - high_lev['ROE'].mean():.2f}pp")

print("\nCorrelations:")
print(f"  Margin vs ROE: {gd3_24['Margin'].corr(gd3_24['ROE']):.4f}")
print(f"  ROA vs ROE: {gd3_24['ROA'].corr(gd3_24['ROE']):.4f}")
print(f"  Leverage vs ROE: {gd3_24['Leverage'].corr(gd3_24['ROE']):.4f}")
print(f"  NPL vs ROE: (NPL vs ROE correlation)")

# Let's calculate correlations with NPL
note_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_3. Note.csv")
for col in note_df.columns:
    if col not in ['Công ty', 'Năm']:
        note_df[col] = pd.to_numeric(note_df[col], errors='coerce').fillna(0)
cols = ['C33', 'C34', 'C35', 'C36', 'C37']
note_df['Total_Loans'] = note_df[cols].sum(axis=1)
note_df['NPL_Amount'] = note_df['C35'] + note_df['C36'] + note_df['C37']
note_df['NPL_Ratio'] = np.where(note_df['Total_Loans'] > 0, note_df['NPL_Amount'] / note_df['Total_Loans'] * 100, 0)

gd3_24 = gd3_24.merge(note_df[['Công ty', 'Năm', 'NPL_Ratio']], on=['Công ty', 'Năm'], how='left')
print(f"  NPL vs ROE: {gd3_24['NPL_Ratio'].corr(gd3_24['ROE']):.4f}")

# Excluding NH22
gd3_24_no22 = gd3_24[gd3_24['Công ty'] != 22]
print("\nWithout NH22:")
med_lev_no22 = gd3_24_no22['Leverage'].median()
low_lev_no22 = gd3_24_no22[gd3_24_no22['Leverage'] <= med_lev_no22]
high_lev_no22 = gd3_24_no22[gd3_24_no22['Leverage'] > med_lev_no22]
print(f"  Leverage Median: {med_lev_no22:.4f}")
print(f"  Low Leverage Group Mean ROE: {low_lev_no22['ROE'].mean():.2f}%")
print(f"  High Leverage Group Mean ROE: {high_lev_no22['ROE'].mean():.2f}%")
print(f"  Difference: {low_lev_no22['ROE'].mean() - high_lev_no22['ROE'].mean():.2f}pp")

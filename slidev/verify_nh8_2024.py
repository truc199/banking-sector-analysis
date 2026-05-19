import pandas as pd
import numpy as np

bs_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
note_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_3. Note.csv")

for df in [bs_df, inc_df, note_df]:
    for col in df.columns:
        if col not in ['Công ty', 'Năm']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm']).merge(note_df, on=['Công ty', 'Năm'])

# Filter 2024
m24 = m_df[m_df['Năm'] == 2024].copy()

m24['ROA'] = m24['B22'] / m24['A1'] * 100
cols = ['C33', 'C34', 'C35', 'C36', 'C37']
m24['Total_Loans'] = m24[cols].sum(axis=1)
m24['NPL_Ratio'] = (m24['C35'] + m24['C36'] + m24['C37']) / m24['Total_Loans'] * 100
m24['CASA_Ratio'] = m24['C68'] / m24['A55'] * 100
m24['CIR'] = m24['B15'] / m24['B14'] * 100
m24['NIM'] = m24['B3'] / m24['A1'] * 100
m24['LDR'] = m24['A13'] / m24['A55'] * 100

print(m24[m24['Công ty'] == 8][['Công ty', 'ROA', 'NPL_Ratio', 'CASA_Ratio', 'CIR', 'NIM', 'LDR']].to_string())
print(m24[m24['Công ty'] == 22][['Công ty', 'ROA', 'NPL_Ratio', 'CASA_Ratio', 'CIR', 'NIM', 'LDR']].to_string())

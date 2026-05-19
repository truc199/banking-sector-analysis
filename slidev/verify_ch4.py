import sys, io, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
is_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
n_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]

bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)
note = pd.read_csv(n_file)

years = [2020, 2021, 2022, 2023, 2024]
bs_y = bs[bs['Năm'].isin(years)].copy()
note_y = note[note['Năm'].isin(years)].copy()

print("--- 4.1 CASA Ratio ---")
# CASA = C68 (Tiền gửi không kỳ hạn) / A55 (Tiền gửi của khách hàng) * 100
# Alternatively, check C68 / C67
# Let's merge note (for C68) and bs (for A55)
casa_df = pd.merge(bs_y[['Công ty', 'Năm', 'A55']], note_y[['Công ty', 'Năm', 'C67', 'C68']], on=['Công ty', 'Năm'])
casa_df['CASA_Ratio_A55'] = casa_df['C68'] / casa_df['A55'] * 100
casa_df['CASA_Ratio_C67'] = casa_df['C68'] / casa_df['C67'] * 100

print("System average CASA Ratio (using A55):")
for y in years:
    sub = casa_df[casa_df['Năm'] == y]
    mean_val = sub['CASA_Ratio_A55'].mean()
    print(f"  {y}: {mean_val:.2f}%")

print("System weighted average CASA Ratio (using A55):")
for y in years:
    sub = casa_df[casa_df['Năm'] == y]
    weighted_val = sub['C68'].sum() / sub['A55'].sum() * 100
    print(f"  {y}: {weighted_val:.2f}%")

# Check gap in 2024
sub_2024 = casa_df[casa_df['Năm'] == 2024]['CASA_Ratio_A55']
print(f"2024 CASA Gap: {sub_2024.max() - sub_2024.min():.2f} pp")

print("\n--- 4.2 LDR ---")
# LDR = A12 (Cho vay khách hàng) / A55 (Tiền gửi của khách hàng) * 100
ldr_df = bs_y[['Công ty', 'Năm', 'A12', 'A55']].copy()
ldr_df['LDR'] = ldr_df['A12'] / ldr_df['A55'] * 100

print("System average LDR:")
for y in years:
    sub = ldr_df[ldr_df['Năm'] == y]
    mean_val = sub['LDR'].mean()
    print(f"  {y}: {mean_val:.2f}%")

print("System weighted average LDR:")
for y in years:
    sub = ldr_df[ldr_df['Năm'] == y]
    weighted_val = sub['A12'].sum() / sub['A55'].sum() * 100
    print(f"  {y}: {weighted_val:.2f}%")

# Check > 100% in 2024
ldr_2024 = ldr_df[ldr_df['Năm'] == 2024]
over_100 = len(ldr_2024[ldr_2024['LDR'] > 100])
print(f"Number of banks with LDR > 100% in 2024: {over_100}")

print("\n--- 4.3 Cấu trúc tín dụng (Bán lẻ hóa) ---")
# Cá nhân (C47) / Tổng cho vay (A12 or C4) * 100
# Let's merge note (for C47) and bs (for A12)
retail_df = pd.merge(bs_y[['Công ty', 'Năm', 'A12']], note_y[['Công ty', 'Năm', 'C42', 'C47']], on=['Công ty', 'Năm'])
retail_df['Retail_Ratio'] = retail_df['C47'] / retail_df['A12'] * 100

print("System average Retail Ratio:")
for y in years:
    sub = retail_df[retail_df['Năm'] == y]
    mean_val = sub['Retail_Ratio'].mean()
    print(f"  {y}: {mean_val:.2f}%")

print("System weighted average Retail Ratio:")
for y in years:
    sub = retail_df[retail_df['Năm'] == y]
    weighted_val = sub['C47'].sum() / sub['A12'].sum() * 100
    print(f"  {y}: {weighted_val:.2f}%")

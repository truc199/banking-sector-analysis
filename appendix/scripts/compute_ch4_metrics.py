"""Compute Chapter 4 metrics: CASA, LDR, Loan Structure by Customer."""
import pandas as pd
import numpy as np
import sys
import glob

# --- Đường dẫn tương đối theo vị trí file (không phụ thuộc máy) ---
import sys as _sys
from pathlib import Path as _Path
_sys.stdout.reconfigure(encoding="utf-8")
ROOT = _Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FIGURES = ROOT / "appendix" / "figures"
FIGURES_S = str(FIGURES)
FIGURES.mkdir(parents=True, exist_ok=True)
# ------------------------------------------------------------------

sys.stdout.reconfigure(encoding='utf-8')

bs   = pd.read_csv(glob.glob(str(DATA / "*Balance*"))[0])
inc  = pd.read_csv(glob.glob(str(DATA / "*Income*"))[0])
note = pd.read_csv(glob.glob(str(DATA / "*Note*"))[0])

YEARS = [2020, 2021, 2022, 2023, 2024]

bs5   = bs  [bs['Năm']  .isin(YEARS)].copy()
note5 = note[note['Năm'].isin(YEARS)].copy()
inc5  = inc [inc['Năm'] .isin(YEARS)].copy()

# Merge for LDR
merged = bs5.merge(inc5, on=['Công ty', 'Năm'])
merged_n = bs5.merge(note5, on=['Công ty', 'Năm'])

# ─────────────────────────────────────────────────────────────────
print("=" * 70)
print("SLIDE 4.1 – CASA RATIO (Nhóm 4)")
print("=" * 70)
# C68 = tiền gửi không kỳ hạn (demand)
# C69 = tiền gửi có kỳ hạn (term)
# C70 = tiết kiệm (savings)
# C71 = ký quỹ; C72 = mục đích riêng
# A55 = tiền gửi khách hàng (BS) — dùng làm mẫu

# CASA = C68 / (C68+C69+C70+C71+C72)
casa_cols_denom = ['C68','C69','C70','C71','C72']
merged_n['total_dep_note'] = merged_n[casa_cols_denom].sum(axis=1)
merged_n['CASA'] = merged_n['C68'] / merged_n['total_dep_note'] * 100

# Industry CASA (weighted)
casa_ind = merged_n.groupby('Năm').apply(
    lambda d: d['C68'].sum() / d['total_dep_note'].sum() * 100
)
print("\nCASA industry (wt avg, %):", {yr: f"{casa_ind[yr]:.2f}" for yr in YEARS})

# Per-bank CASA 2024
casa24 = merged_n[merged_n['Năm']==2024][['Công ty','CASA']].copy()
casa24 = casa24.sort_values('CASA', ascending=False)
print(f"\n2024 CASA: mean={casa24['CASA'].mean():.2f}%, median={casa24['CASA'].median():.2f}%")
print(f"  max={casa24['CASA'].max():.2f}% (NH {int(casa24.iloc[0]['Công ty'])})")
print(f"  min={casa24['CASA'].min():.2f}% (NH {int(casa24.iloc[-1]['Công ty'])})")
print(f"  spread (max-min)={casa24['CASA'].max()-casa24['CASA'].min():.2f}pp")
print("\nAll 2024 CASA by bank (sorted):")
for _, row in casa24.iterrows():
    print(f"  NH {int(row['Công ty'])}: {row['CASA']:.2f}%")

# For slide: CASA trend
print("\nCASA trend (industry wt avg):")
for yr in YEARS:
    print(f"  {yr}: {casa_ind[yr]:.2f}%")

# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SLIDE 4.2 – LDR (Nhóm 7)")
print("=" * 70)
# LDR = A13 (Gross loans) / A55 (Customer deposits)
merged['LDR'] = merged['A13'] / merged['A55'] * 100

ldr_ind = merged.groupby('Năm').apply(
    lambda d: d['A13'].sum() / d['A55'].sum() * 100
)
ldr_mean = merged.groupby('Năm')['LDR'].mean()
print("\nLDR industry wt avg (%):", {yr: f"{ldr_ind[yr]:.2f}" for yr in YEARS})
print("LDR simple mean (%):", {yr: f"{ldr_mean[yr]:.2f}" for yr in YEARS})

ldr24 = merged[merged['Năm']==2024]['LDR']
print(f"\n2024 LDR: mean={ldr24.mean():.2f}%, max={ldr24.max():.2f}%, min={ldr24.min():.2f}%")
print(f"  NH với LDR>100%: {(ldr24>100).sum()}")
print(f"  NH với LDR>120%: {(ldr24>120).sum()}")

# Loan growth vs deposit growth
loans   = merged.groupby('Năm')['A13'].sum()
deposits= merged.groupby('Năm')['A55'].sum()
loan_g  = loans.pct_change()*100
dep_g   = deposits.pct_change()*100
print("\nLoan growth YoY:", {yr: f"{loan_g[yr]:.2f}%" for yr in YEARS if yr!=2020})
print("Deposit growth YoY:", {yr: f"{dep_g[yr]:.2f}%" for yr in YEARS if yr!=2020})

# ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SLIDE 4.3 – LOAN STRUCTURE BY CUSTOMER (Nhóm 8)")
print("=" * 70)
# C42=total phân theo nhóm KH, C43=DNNN, C44=Cty TNHH&CP, C45=NN, C46=HTX&TN, C47=Cá nhân, C48=Khác
# Total cho vay = C43+C44+C45+C46+C47+C48
loan_cust_cols = ['C43','C44','C45','C46','C47','C48']
merged_n['total_loan_cust'] = merged_n[loan_cust_cols].sum(axis=1)
# Keep only rows where total matches reasonably
merged_n['ca_nhan_ratio'] = merged_n['C47'] / merged_n['total_loan_cust'] * 100

# Điền 0 cho NaN (ngân hàng không báo cáo)
merged_n[loan_cust_cols] = merged_n[loan_cust_cols].fillna(0)
merged_n['total_loan_cust'] = merged_n[loan_cust_cols].sum(axis=1)

# Industry-level loan structure
for yr in YEARS:
    d = merged_n[merged_n['Năm']==yr]
    total = d[loan_cust_cols].sum()
    grand = total.sum()
    print(f"\n{yr} loan mix:")
    labels = ['DNNN','Cty TNHH&CP','NN','HTX&TN','Cá nhân','Khác']
    for col, lbl in zip(loan_cust_cols, labels):
        print(f"  {lbl}: {total[col]/grand*100:.1f}%")

print("\nCá nhân ratio trend (industry wt avg):")
ca_nhan_ind = merged_n.groupby('Năm').apply(
    lambda d: d['C47'].sum() / d[loan_cust_cols].sum().sum() * 100
)
for yr in YEARS:
    print(f"  {yr}: {ca_nhan_ind[yr]:.1f}%")

# DNNh + Cty TNHH = corporate
print("\nCorporate (DNNN+TNHH+NN+HTX) ratio:")
corp_ind = merged_n.groupby('Năm').apply(
    lambda d: (d['C43']+d['C44']+d['C45']+d['C46']).sum() / d[loan_cust_cols].sum().sum() * 100
)
for yr in YEARS:
    print(f"  {yr}: {corp_ind[yr]:.1f}%")

# Per-bank 2024 ca nhan ratio
ca24 = merged_n[merged_n['Năm']==2024][['Công ty','ca_nhan_ratio']].dropna()
ca24 = ca24[ca24['ca_nhan_ratio']>0]
print(f"\n2024 Cá nhân ratio: mean={ca24['ca_nhan_ratio'].mean():.1f}%, max={ca24['ca_nhan_ratio'].max():.1f}%")

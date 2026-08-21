"""Compute NPL, CASA, Sector exposure, Coverage ratio from Note data."""
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

bs = pd.read_csv(glob.glob(str(DATA / "*Balance*"))[0])
inc = pd.read_csv(glob.glob(str(DATA / "*Income*"))[0])
note = pd.read_csv(glob.glob(str(DATA / "*Note*"))[0])

YEARS = [2020, 2021, 2022, 2023, 2024]

note5 = note[note['Năm'].isin(YEARS)].copy()
bs5 = bs[bs['Năm'].isin(YEARS)].copy()
inc5 = inc[inc['Năm'].isin(YEARS)].copy()
merged = bs5.merge(inc5, on=['Công ty','Năm']).merge(note5, on=['Công ty','Năm'])

# ── NPL ──────────────────────────────────────────────────────────────────────
# C32=Total loans for quality classification
# C33=Nợ đủ tiêu chuẩn, C34=Nợ cần chú ý, C35=NTChuẩn, C36=NNghi ngờ, C37=NKhả năng mất vốn
# NPL = (C35+C36+C37) / C32
# Watch-list (Nhóm 2) = C34 / C32
print("=" * 70)
print("NPL & ASSET QUALITY")
print("=" * 70)

merged['npl_abs'] = merged['C35'] + merged['C36'] + merged['C37']
merged['npl_ratio'] = merged['npl_abs'] / merged['C32'] * 100
merged['watch_ratio'] = merged['C34'] / merged['C32'] * 100

npl_ind = merged.groupby('Năm').apply(lambda d: (d['C35']+d['C36']+d['C37']).sum() / d['C32'].sum() * 100)
watch_ind = merged.groupby('Năm').apply(lambda d: d['C34'].sum() / d['C32'].sum() * 100)

print("\nNPL ratio (industry, %):", {yr: f"{npl_ind[yr]:.2f}%" for yr in YEARS})
print("Watch-list ratio (industry, %):", {yr: f"{watch_ind[yr]:.2f}%" for yr in YEARS})

# NPL per bank distribution 2024
npl24 = merged[merged['Năm']==2024]['npl_ratio']
print(f"\n2024 NPL: mean={npl24.mean():.2f}%, min={npl24.min():.2f}%, max={npl24.max():.2f}%")
print(f"NH NPL>3%: {(npl24>3).sum()}")
print(f"NH NPL>5%: {(npl24>5).sum()}")

# Coverage ratio = A14(provision) / npl_abs  [A14 is negative]
merged['coverage'] = abs(merged['A14']) / merged['npl_abs'] * 100
cov24 = merged[merged['Năm']==2024]['coverage']
print(f"\n2024 Coverage: mean={cov24.mean():.2f}%, min={cov24.min():.2f}%, max={cov24.max():.2f}%")
print(f"NH Coverage<100%: {(cov24<100).sum()}")
print(f"NH Coverage>150%: {(cov24>150).sum()}")

# VAMC bonds = C64 (Trái phiếu đặc biệt VAMC)
vamc24 = merged[(merged['Năm']==2024) & (merged['C64']>0)]['Công ty'].nunique()
vamc20 = merged[(merged['Năm']==2020) & (merged['C64']>0)]['Công ty'].nunique()
print(f"\nNH còn VAMC bonds: 2020={vamc20}, 2024={vamc24}")

# ── CASA ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("CASA")
print("=" * 70)

# C68=Demand deposits (TG không kỳ hạn), C55=total customer deposits (BS: A55)
# CASA = C68 / A55
merged['CASA'] = merged['C68'] / merged['A55'] * 100
casa_ind = merged.groupby('Năm').apply(lambda d: d['C68'].sum() / d['A55'].sum() * 100)
print("\nCASA ratio (industry, %):", {yr: f"{casa_ind[yr]:.2f}%" for yr in YEARS})
casa24 = merged[merged['Năm']==2024]['CASA']
print(f"\n2024 CASA: mean={casa24.mean():.2f}%, min={casa24.min():.2f}%, max={casa24.max():.2f}%, spread={casa24.max()-casa24.min():.2f}pp")

# ── LOAN STRUCTURE ────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("LOAN STRUCTURE")
print("=" * 70)

# C47=Individual loans, C42=Total loans by customer type
merged['retail_ratio'] = merged['C47'] / merged['C42'] * 100
retail_ind = merged.groupby('Năm').apply(lambda d: d['C47'].sum() / d['C42'].sum() * 100)
print("\nRetail loan ratio (individual/total, %):", {yr: f"{retail_ind[yr]:.2f}%" for yr in YEARS})

# C28=Real estate loans
re_ind = merged.groupby('Năm').apply(lambda d: d['C28'].sum() / d['C4'].sum() * 100)
print("Real estate loans ratio (%):", {yr: f"{re_ind[yr]:.2f}%" for yr in YEARS})

# Loan by maturity: C39=short, C40=mid, C41=long
st_ind = merged.groupby('Năm').apply(lambda d: d['C39'].sum() / d['C38'].sum() * 100)
lt_ind = merged.groupby('Năm').apply(lambda d: d['C41'].sum() / d['C38'].sum() * 100)
print("Short-term loan ratio:", {yr: f"{st_ind[yr]:.2f}%" for yr in YEARS})
print("Long-term loan ratio:", {yr: f"{lt_ind[yr]:.2f}%" for yr in YEARS})

# ── INCOME DETAILS ────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("INCOME STRUCTURE DETAILS")
print("=" * 70)

# Service fee income: C92=net service income
# NIM: need Cost of Funds
# CoF = C87 (interest expenses) / A55 (customer deposits)
merged['CoF'] = merged['C87'] / merged['A55'] * 100
cof_ind = merged.groupby('Năm').apply(lambda d: d['C87'].sum()/d['A55'].sum()*100)
print("\nCost of Funds (CoF, %):", {yr: f"{cof_ind[yr]:.2f}%" for yr in YEARS})

# Service income: B6 (net service income); C92 (detail)
svc_ind = merged.groupby('Năm').apply(lambda d: d['B6'].sum() / d['B14'].sum() * 100)
print("Net service income / TOI:", {yr: f"{svc_ind[yr]:.2f}%" for yr in YEARS})

# Bancassurance: C97 (Thu từ hoạt động bảo hiểm)
banca_banks = merged[(merged['Năm']==2024) & (merged['C97']>0)]['Công ty'].nunique()
print(f"\nNH có bancassurance income (2024): {banca_banks}")

# Personnel expense ratio
merged['staff_ratio'] = merged['C142'] / merged['B15'] * 100
staff24 = merged[merged['Năm']==2024]['staff_ratio']
print(f"\nStaff cost / total opex (2024): mean={staff24.mean():.1f}%, range={staff24.min():.1f}%-{staff24.max():.1f}%")

# Staff costs
staff_ind = merged.groupby('Năm').apply(lambda d: d['C142'].sum() / d['B15'].sum() * 100)
print("Staff / total opex by year:", {yr: f"{staff_ind[yr]:.1f}%" for yr in YEARS})

# ── DEPOSIT STRUCTURE ─────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("DEPOSIT STRUCTURE")
print("=" * 70)

# C73=deposits by customer type; C74=SOE, C75=Private corp, C76=FDI, C77=Individual
indiv_dep_ind = merged.groupby('Năm').apply(lambda d: d['C77'].sum() / d['C73'].sum() * 100)
print("Individual deposit ratio:", {yr: f"{indiv_dep_ind[yr]:.2f}%" for yr in YEARS})

# ── PROFITABILITY DECOMPOSITION ───────────────────────────────────────────────
print("\n" + "=" * 70)
print("DUPONT / PROFITABILITY")
print("=" * 70)

# Profit margin = B22/B14
merged['profit_margin'] = merged['B22'] / merged['B14'] * 100
# Asset turnover = B14/A1
merged['asset_turnover'] = merged['B14'] / merged['A1'] * 100
# Leverage = A1/A64
merged['leverage'] = merged['A1'] / merged['A64']

# 2024 correlations
d24 = merged[merged['Năm']==2024].copy()
d24['ROE'] = d24['B22'] / d24['A64'] * 100

# ROA correlation
from scipy import stats
r_pm_roe, p_pm_roe = stats.pearsonr(d24['profit_margin'].dropna(), d24['ROE'].dropna())
r_lev_roe, p_lev_roe = stats.pearsonr(d24['leverage'].dropna(), d24['ROE'].dropna())
r_casa_roa, p_casa_roa = stats.pearsonr(d24['CASA'].dropna(), (d24['B22']/d24['A1']*100).dropna())

print(f"\nProfit Margin ↔ ROE: r={r_pm_roe:.3f}, p={p_pm_roe:.4f}")
print(f"Leverage ↔ ROE: r={r_lev_roe:.3f}, p={p_lev_roe:.4f}")
print(f"CASA ↔ ROA: r={r_casa_roa:.3f}, p={p_casa_roa:.4f}")

# CoF vs NIM (2024)
d24['NIM'] = d24['B3'] / (d24['A12'] + d24['A18']) * 100
r_cof_nim, p_cof_nim = stats.pearsonr(d24['CoF'].dropna(), d24['NIM'].dropna())
print(f"CoF ↔ NIM: r={r_cof_nim:.3f}, p={p_cof_nim:.4f}")

r_casa_nim, p_casa_nim = stats.pearsonr(d24['CASA'].dropna(), d24['NIM'].dropna())
print(f"CASA ↔ NIM: r={r_casa_nim:.3f}, p={p_casa_nim:.4f}")

# NPL correlation
r_re_npl, p_re_npl = stats.pearsonr(d24['C28'].fillna(0) / d24['C4'].fillna(1) * 100, d24['npl_ratio'].dropna())
print(f"RE exposure ↔ NPL: r={r_re_npl:.3f}, p={p_re_npl:.4f}")

r_fee_roa, p_fee_roa = stats.pearsonr(d24['B6']/d24['B14']*100, d24['B22']/d24['A1']*100)
print(f"Fee income ratio ↔ ROA: r={r_fee_roa:.3f}, p={p_fee_roa:.4f}")

# Equity ratio vs ROA
r_eq_roa, p_eq_roa = stats.pearsonr(d24['er'] if 'er' in d24.columns else (d24['A64']/d24['A1']*100), d24['B22']/d24['A1']*100)
d24['er'] = d24['A64'] / d24['A1'] * 100
r_eq_roa, p_eq_roa = stats.pearsonr(d24['er'], d24['B22']/d24['A1']*100)
print(f"Equity Ratio ↔ ROA: r={r_eq_roa:.3f}, p={p_eq_roa:.4f}")

# Coverage vs ROA
r_cov_roa, p_cov_roa = stats.pearsonr(d24['coverage'].dropna(), (d24['B22']/d24['A1']*100).dropna())
print(f"Coverage ↔ ROA: r={r_cov_roa:.3f}, p={p_cov_roa:.4f}")

print("\n\nDONE.")

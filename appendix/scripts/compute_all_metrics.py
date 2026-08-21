"""Compute all key metrics needed for the storytelling flow."""
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

bs5 = bs[bs['Năm'].isin(YEARS)].copy()
inc5 = inc[inc['Năm'].isin(YEARS)].copy()
note5 = note[note['Năm'].isin(YEARS)].copy() if 'Năm' in note.columns else pd.DataFrame()

print("=== INC COLUMNS ===")
print(list(inc.columns[:10]))
print()

# ── 1. INDUSTRY TOTALS ────────────────────────────────────────────────────────
print("=" * 70)
print("SECTION 1: QUY MÔ & TĂNG TRƯỞNG")
print("=" * 70)

tts = bs5.groupby('Năm')['A1'].sum()
vcsh = bs5.groupby('Năm')['A64'].sum()
vdl = bs5.groupby('Năm')['A66'].sum()
tts_g = tts.pct_change() * 100

print("\nTTS (triệu tỷ):", {yr: f"{tts[yr]/1e6:.2f}" for yr in YEARS})
print("TTS growth (%):", {yr: f"{tts_g[yr]:.2f}" for yr in YEARS if not np.isnan(tts_g.get(yr, np.nan))})
print("VCSH (nghìn tỷ):", {yr: f"{vcsh[yr]/1000:.1f}" for yr in YEARS})
print("VĐL (nghìn tỷ):", {yr: f"{vdl[yr]/1000:.1f}" for yr in YEARS})

er_industry = vcsh / tts * 100
print("Equity Ratio (wt avg):", {yr: f"{er_industry[yr]:.2f}%" for yr in YEARS})

# Per-bank 2024 equity ratio
bs24 = bs5[bs5['Năm']==2024].copy()
bs24['er'] = bs24['A64'] / bs24['A1'] * 100
print(f"\n2024 ER: mean={bs24['er'].mean():.2f}%, min={bs24['er'].min():.2f}%, max={bs24['er'].max():.2f}%, spread={bs24['er'].max()-bs24['er'].min():.2f}pp")
print(f"NH ER<6%: {(bs24['er']<6).sum()} banks")
print(f"NH ER>10%: {(bs24['er']>10).sum()} banks")

# ── 2. PROFITABILITY ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SECTION 2: HIỆU QUẢ SINH LỜI")
print("=" * 70)

# Merge BS + Income for ROA/ROE
merged = bs5.merge(inc5, on=['Công ty', 'Năm'])
merged['ROA'] = merged['B22'] / merged['A1'] * 100
merged['ROE'] = merged['B22'] / merged['A64'] * 100

roa_ind = merged.groupby('Năm').apply(lambda d: d['B22'].sum() / d['A1'].sum() * 100)
roe_ind = merged.groupby('Năm').apply(lambda d: d['B22'].sum() / d['A64'].sum() * 100)
print("\nROA (industry wt avg):", {yr: f"{roa_ind[yr]:.2f}%" for yr in YEARS})
print("ROE (industry wt avg):", {yr: f"{roe_ind[yr]:.2f}%" for yr in YEARS})

roe24 = merged[merged['Năm']==2024]['ROE']
print(f"\n2024 ROE: min={roe24.min():.2f}%, max={roe24.max():.2f}%, spread={roe24.max()-roe24.min():.2f}pp")
roa24 = merged[merged['Năm']==2024]['ROA']
print(f"2024 ROA: min={roa24.min():.2f}%, max={roa24.max():.2f}%")

# NIM = (B1-B2)/A1*100 (using net interest margin proxy)
# NIM = B3 / avg earning assets; proxy: B3/A12
merged['NIM_proxy'] = merged['B3'] / ((merged['A12'] + merged['A18']) ) * 100
nim_ind = merged.groupby('Năm').apply(lambda d: d['B3'].sum() / (d['A12'].sum() + d['A18'].sum()) * 100)
print("\nNIM proxy (B3/(Loans+InvSec)) (%):", {yr: f"{nim_ind[yr]:.2f}%" for yr in YEARS})

# TOI = B14 (total operating income)
toi = merged.groupby('Năm')['B14'].sum()
nim_income = merged.groupby('Năm')['B3'].sum()
fee_income = merged.groupby('Năm')['B6'].sum()
print("\nNet interest income share of TOI:")
for yr in YEARS:
    print(f"  {yr}: NII/TOI={nim_income[yr]/toi[yr]*100:.1f}%, Fee/TOI={fee_income[yr]/toi[yr]*100:.1f}%")

# ── 3. INCOME STRUCTURE ───────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SECTION 3: CƠ CẤU THU NHẬP & CHI PHÍ")
print("=" * 70)

# B3=NII, B6=Fee net, B7=FX, B8=Trading sec, B9=InvSec, B12=Other, B13=Equity income
non_interest = toi - nim_income
print("\nNon-interest income / TOI:")
for yr in YEARS:
    print(f"  {yr}: {non_interest[yr]/toi[yr]*100:.2f}%")

# CIR = B15/B14
merged['CIR'] = merged['B15'] / merged['B14'] * 100
cir_ind = merged.groupby('Năm').apply(lambda d: d['B15'].sum()/d['B14'].sum()*100)
print("\nCIR (industry avg):", {yr: f"{cir_ind[yr]:.2f}%" for yr in YEARS})
cir24 = merged[merged['Năm']==2024]['CIR']
print(f"2024 CIR: min={cir24.min():.2f}%, max={cir24.max():.2f}%, spread={cir24.max()-cir24.min():.2f}pp")

# PPOP = B16, Provision = B17
merged['ProvisionRatio'] = merged['B17'] / merged['B16'] * 100
prov24 = merged[merged['Năm']==2024]
print(f"\nNH có dự phòng/PPOP>50%: {(prov24['ProvisionRatio']>50).sum()}")

# ── 4. DEPOSITS & CREDIT ─────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SECTION 4: HUY ĐỘNG & TÍN DỤNG")
print("=" * 70)

# LDR = A12 / A55  (loans / customer deposits)
merged['LDR'] = merged['A13'] / merged['A55'] * 100   # gross loans / deposits
ldr_ind = merged.groupby('Năm').apply(lambda d: d['A13'].sum()/d['A55'].sum()*100)
print("\nLDR (industry):", {yr: f"{ldr_ind[yr]:.2f}%" for yr in YEARS})
ldr24 = merged[merged['Năm']==2024]['LDR']
print(f"2024 NH LDR>100%: {(ldr24>100).sum()}")
print(f"2024 NH LDR>120%: {(ldr24>120).sum()}")

# Loan growth
loans = merged.groupby('Năm')['A13'].sum()
loan_g = loans.pct_change() * 100
print("\nLoan growth:", {yr: f"{loan_g[yr]:.2f}%" for yr in YEARS if not np.isnan(loan_g.get(yr, np.nan))})

deposits = merged.groupby('Năm')['A55'].sum()
dep_g = deposits.pct_change() * 100
print("Deposit growth:", {yr: f"{dep_g[yr]:.2f}%" for yr in YEARS if not np.isnan(dep_g.get(yr, np.nan))})

# GTCG = A58 (issued valuable papers)
gtcg = merged.groupby('Năm')['A58'].sum()
print("\nGTCG (nghìn tỷ):", {yr: f"{gtcg[yr]/1000:.1f}" for yr in YEARS})
gtcg_ratio = merged.copy()
gtcg_ratio['gtcg_r'] = gtcg_ratio['A58'] / gtcg_ratio['A55'] * 100
gtcg24 = gtcg_ratio[gtcg_ratio['Năm']==2024]
print(f"NH GTCG/TG>5%: {(gtcg24['gtcg_r']>5).sum()}")

# ── 5. NOTE DATA: NPL, CASA, Sector exposure ─────────────────────────────────
print("\n" + "=" * 70)
print("SECTION 5: NOTE DATA")
print("=" * 70)

print("Note columns:", list(note.columns[:15]))
print("Note shape:", note.shape)
print("Note first 3 rows:")
print(note.head(3).to_string())

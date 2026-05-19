import pandas as pd
import numpy as np
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]

bs = pd.read_csv(bs_file)
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

# ============================================================
# SLIDE 1.1: TTS toàn ngành + growth
# ============================================================
tts_by_year = bs_5y.groupby('Năm')['A1'].sum().sort_index()
growth = tts_by_year.pct_change() * 100

print("=== SLIDE 1.1 ===")
for yr, val in tts_by_year.items():
    g = growth.get(yr, np.nan)
    g_str = f", Growth: {g:.2f}%" if not np.isnan(g) else ""
    print(f"  {yr}: {val/1e6:.2f} triệu tỷ VND{g_str}")

# GDP data
gdp_data = {2020: 2.91, 2021: 2.58, 2022: 8.02, 2023: 5.05, 2024: 7.09}
print(f"\nGDP Growth: {gdp_data}")

# ============================================================
# SLIDE 1.2: VĐL + VCSH + Equity ratio
# ============================================================
print("\n=== SLIDE 1.2 ===")
vdl_by_year = bs_5y.groupby('Năm')['A66'].sum().sort_index()
vcsh_by_year = bs_5y.groupby('Năm')['A64'].sum().sort_index()

for yr in [2020, 2021, 2022, 2023, 2024]:
    vdl = vdl_by_year[yr]
    vcsh = vcsh_by_year[yr]
    tts = tts_by_year[yr]
    er = vcsh / tts * 100
    print(f"  {yr}: VĐL={vdl/1000:,.1f} nghìn tỷ, VCSH={vcsh/1000:,.1f} nghìn tỷ, Equity Ratio={er:.2f}%")

vdl_g = vdl_by_year.pct_change() * 100
vcsh_g = vcsh_by_year.pct_change() * 100
print(f"\nGrowth VĐL: {dict(zip(vdl_g.index, [f'{v:.2f}%' for v in vdl_g.values]))}")
print(f"Growth VCSH: {dict(zip(vcsh_g.index, [f'{v:.2f}%' for v in vcsh_g.values]))}")

# Equity ratio trend
er_trend = vcsh_by_year / tts_by_year * 100
print(f"Equity Ratio trend: {dict(zip(er_trend.index, [f'{v:.2f}%' for v in er_trend.values]))}")

# ============================================================
# SLIDE 1.3: Phân hóa Equity Ratio
# ============================================================
print("\n=== SLIDE 1.3 ===")
bs_2024 = bs_5y[bs_5y['Năm'] == 2024].copy()
bs_2024['equity_ratio'] = (bs_2024['A64'] / bs_2024['A1']) * 100
bs_2024 = bs_2024.sort_values('equity_ratio', ascending=False)

for _, row in bs_2024.iterrows():
    print(f"  NH {int(row['Công ty']):2d}: Equity Ratio = {row['equity_ratio']:.2f}%")

max_er = bs_2024['equity_ratio'].max()
min_er = bs_2024['equity_ratio'].min()
print(f"\n  Max: {max_er:.2f}%")
print(f"  Min: {min_er:.2f}%")
print(f"  Khoảng cách: {max_er - min_er:.2f}pp")
print(f"  Mean: {bs_2024['equity_ratio'].mean():.2f}%")

thin_cap = bs_2024[bs_2024['equity_ratio'] < 6]
print(f"\n  NH đệm vốn mỏng <6%: {len(thin_cap)}")
for _, row in thin_cap.iterrows():
    print(f"    NH {int(row['Công ty'])}: {row['equity_ratio']:.2f}%")

# Top 5 and Bottom 5
print(f"\n  Top 5:")
for _, row in bs_2024.head(5).iterrows():
    print(f"    NH {int(row['Công ty'])}: {row['equity_ratio']:.2f}%")
print(f"  Bottom 5:")
for _, row in bs_2024.tail(5).iterrows():
    print(f"    NH {int(row['Công ty'])}: {row['equity_ratio']:.2f}%")

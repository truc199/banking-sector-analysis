"""
Generate charts for Slides 1.2 and 1.3 — Chương 1: Quy mô & Tăng trưởng
"""
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

# ─── Setup ───────────────────────────────────────────────────────────────
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#334155'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Navy blue palette
NAVY_DARK    = '#003366'  # Dark Midnight Blue
NAVY_MID     = '#004C99'  # US Air Force Academy Blue
NAVY_BRIGHT  = '#0066CC'  # Bright Navy Blue
AZURE        = '#007FFF'  # Azure
DODGER       = '#3399FF'  # Dodger Blue
FRENCH_SKY   = '#66B2FF'  # French Sky Blue
BABY_BLUE    = '#99CCFF'  # Baby Blue Eyes

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

# ─── Load Data ───────────────────────────────────────────────────────────
bs = pd.read_csv(glob.glob(r'd:\uni\gcontest\*Balance*')[0])
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

years = [2020, 2021, 2022, 2023, 2024]
year_labels = ['2020', '2021', '2022', '2023', '2024']

# Aggregate industry totals
vdl_by_year  = bs_5y.groupby('Năm')['A66'].sum().reindex(years)
vcsh_by_year = bs_5y.groupby('Năm')['A64'].sum().reindex(years)
tts_by_year  = bs_5y.groupby('Năm')['A1'].sum().reindex(years)
equity_ratio = (vcsh_by_year / tts_by_year * 100).values

vdl_vals  = (vdl_by_year / 1000).values   # nghìn tỷ
vcsh_vals = (vcsh_by_year / 1000).values   # nghìn tỷ

# =====================================================================
# CHART 1 — Slide 1.2: Grouped Bar (VĐL & VCSH) + Line (Equity Ratio)
# =====================================================================
fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)

x = np.arange(len(years))
bar_w = 0.30

# Bars — VĐL (darker) and VCSH (medium)
bars1 = ax1.bar(x - bar_w/2, vdl_vals, bar_w, color=NAVY_DARK, alpha=0.90,
                edgecolor=NAVY_DARK, linewidth=0.8, label='Vốn điều lệ', zorder=3)
bars2 = ax1.bar(x + bar_w/2, vcsh_vals, bar_w, color=DODGER, alpha=0.85,
                edgecolor=NAVY_MID, linewidth=0.8, label='Vốn chủ sở hữu', zorder=3)

ax1.set_xlabel('Năm', fontsize=11, fontweight='bold', labelpad=10, color=TEXT_MID)
ax1.set_ylabel('Nghìn tỷ VND', fontsize=11, fontweight='bold', labelpad=10, color=TEXT_MID)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=10)
ax1.set_ylim(0, max(vcsh_vals) * 1.30)

# Equity Ratio line — secondary axis (contrasting orange-amber)
ax2 = ax1.twinx()

LINE_COLOR = '#E67300'  # High contrast amber-orange for line on navy bars

x_smooth = np.linspace(0, len(years)-1, 300)
pchip = PchipInterpolator(x, equity_ratio)
y_smooth = pchip(x_smooth)

ax2.plot(x_smooth, y_smooth, color=LINE_COLOR, linewidth=2.5,
         linestyle='--', label='Equity/TTS (%)', zorder=5)
ax2.plot(x, equity_ratio, color=LINE_COLOR, marker='o', markersize=7,
         markerfacecolor='white', markeredgewidth=2.5, linestyle='None', zorder=6)

ax2.set_ylabel('Equity / Tổng tài sản (%)', fontsize=11, fontweight='bold',
               labelpad=10, color=TEXT_MID)
ax2.set_ylim(5, 10)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))

# Value labels on bars
for bar in bars1:
    h = bar.get_height()
    ax1.annotate(f'{h:,.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                 xytext=(0, 4), textcoords='offset points',
                 ha='center', va='bottom', fontsize=8, fontweight='bold', color=NAVY_DARK)

for bar in bars2:
    h = bar.get_height()
    ax1.annotate(f'{h:,.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
                 xytext=(0, 4), textcoords='offset points',
                 ha='center', va='bottom', fontsize=8, fontweight='bold', color=NAVY_MID)

# Value labels on line
for i, val in enumerate(equity_ratio):
    ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 10),
                 textcoords='offset points', ha='center', va='bottom',
                 fontsize=9, fontweight='bold', color=LINE_COLOR)

# Grid & spines
ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# Title
plt.title('TĂNG TRƯỞNG VỐN ĐIỀU LỆ & VỐN CHỦ SỞ HỮU TOÀN NGÀNH (2020–2024)',
          fontsize=13, fontweight='bold', pad=18, color=TEXT_DARK)

# Combined legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper left', frameon=True,
           facecolor='white', edgecolor='#e2e8f0', fontsize=9)

plt.tight_layout()
save1 = r'd:\uni\gcontest\slidev\slide_1_2_capital.png'
plt.savefig(save1, dpi=300, bbox_inches='tight')
plt.close()
print(f'Saved: {save1}')


# =====================================================================
# CHART 2 — Slide 1.3: Horizontal Bar — Equity Ratio per bank (2024)
# =====================================================================
bs_2024 = bs_5y[bs_5y['Năm'] == 2024].copy()
bs_2024['equity_ratio'] = bs_2024['A64'] / bs_2024['A1'] * 100
bs_2024 = bs_2024.sort_values('equity_ratio', ascending=True)

bank_labels = [f'NH {int(b)}' for b in bs_2024['Công ty']]
er_vals = bs_2024['equity_ratio'].values

fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

# Color each bar: red-ish if <6%, navy gradient otherwise
colors = []
for v in er_vals:
    if v < 6.0:
        colors.append('#CC3333')  # Warning red
    elif v < 8.0:
        colors.append(FRENCH_SKY)
    elif v < 10.0:
        colors.append(DODGER)
    elif v < 12.0:
        colors.append(NAVY_BRIGHT)
    else:
        colors.append(NAVY_DARK)

bars = ax.barh(bank_labels, er_vals, color=colors, height=0.65,
               edgecolor='white', linewidth=0.5, zorder=3)

# 6% threshold line
ax.axvline(x=6.0, color='#CC3333', linewidth=1.8, linestyle='--', zorder=4,
           label='Ngưỡng cảnh báo 6%')

# Industry mean line
mean_er = bs_2024['equity_ratio'].mean()
ax.axvline(x=mean_er, color=AZURE, linewidth=1.8, linestyle='-.', zorder=4,
           label=f'Trung bình ngành ({mean_er:.2f}%)')

# Value labels
for bar, val in zip(bars, er_vals):
    w = bar.get_width()
    txt_color = '#CC3333' if val < 6.0 else NAVY_DARK
    ax.text(w + 0.15, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}%', va='center', ha='left',
            fontsize=8, fontweight='bold', color=txt_color)

# Annotations for max, min
max_er = er_vals.max()
min_er = er_vals.min()
spread = max_er - min_er

# Add spread annotation
ax.annotate(f'Khoảng cách: {spread:.2f}pp',
            xy=(max_er - spread/2, len(er_vals) - 0.5),
            fontsize=10, fontweight='bold', color=NAVY_DARK,
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BABY_BLUE, alpha=0.3, edgecolor=NAVY_MID))

# Styling
ax.set_xlabel('Equity Ratio (%)', fontsize=11, fontweight='bold', labelpad=10, color=TEXT_MID)
ax.set_ylabel('')
ax.set_xlim(0, max_er + 2.5)
ax.grid(True, axis='x', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)
ax.tick_params(axis='y', labelsize=9)

plt.title('PHÂN HÓA TỶ LỆ AN TOÀN VỐN (EQUITY RATIO) NĂM 2024',
          fontsize=13, fontweight='bold', pad=18, color=TEXT_DARK)

ax.legend(loc='lower right', frameon=True, facecolor='white',
          edgecolor='#e2e8f0', fontsize=9)

plt.tight_layout()
save2 = r'd:\uni\gcontest\slidev\slide_1_3_equity_dispersion.png'
plt.savefig(save2, dpi=300, bbox_inches='tight')
plt.close()
print(f'Saved: {save2}')

print('\nDone! Both charts generated.')

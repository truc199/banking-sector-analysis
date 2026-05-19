"""
Generate unified premium charts for Chapter 1: Quy mô & Tăng trưởng
Standardized on the Navy Blue color scheme, featuring smooth dotted lines (PCHIP)
and highly professional layouts for a side-by-side dashboard grid.
Saves all charts inside the slidev/public/ directory so Slidev/Vite can serve them.
"""
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

# ─── Setup ───────────────────────────────────────────────────────────────
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

NAVY_DARK    = '#003366'  # Dark Midnight Blue
NAVY_MID_D   = '#004C99'  # US Air Force Academy Blue
NAVY_MID     = '#0066CC'  # Bright Navy Blue
AZURE        = '#007FFF'  # Azure
DODGER       = '#3399FF'  # Dodger blue
FRENCH_SKY   = '#66B2FF'  # French Sky Blue
BABY_BLUE    = '#99CCFF'  # Baby Blue Eyes

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

# Create the public directory for static assets if it doesn't exist
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

years = [2020, 2021, 2022, 2023, 2024]
year_labels = ['2020', '2021', '2022', '2023', '2024']

vdl_by_year  = bs_5y.groupby('Năm')['A66'].sum().reindex(years)
vcsh_by_year = bs_5y.groupby('Năm')['A64'].sum().reindex(years)
tts_by_year  = bs_5y.groupby('Năm')['A1'].sum().reindex(years)
equity_ratio = (vcsh_by_year / tts_by_year * 100).values

vdl_vals  = (vdl_by_year / 1000).values
vcsh_vals = (vcsh_by_year / 1000).values
tts_vals  = (tts_by_year / 1e6).values
gdp_growth = [2.91, 2.58, 8.02, 5.05, 7.09]

# =====================================================================
# GLOBAL UNIFORM FONT SIZE HIERARCHY (UPGRADED FOR VISUAL EXCELLENCE)
# =====================================================================
FS_TITLE = 13     # Bold chart title
FS_LABEL = 11.5   # Axis labels
FS_TICK = 10      # Axis ticks
FS_VAL = 10       # Bar/line annotations
FS_LEG = 10       # Legend font size

# =====================================================================
# CHART 1: TỔNG TÀI SẢN VS GDP (Wider side-by-side format)
# =====================================================================
fig, ax1 = plt.subplots(figsize=(5.5, 3.8), dpi=350)
x = np.arange(len(years))

# Bar for Assets (Dark Navy)
bars = ax1.bar(x, tts_vals, color=NAVY_DARK, width=0.4, alpha=0.90,
               edgecolor=NAVY_DARK, linewidth=0.8, label='Tổng tài sản', zorder=3)
ax1.set_ylabel('Tổng tài sản (Triệu tỷ VND)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=FS_TICK)
ax1.set_ylim(0, max(tts_vals) * 1.30)
ax1.tick_params(axis='y', labelsize=FS_TICK)

# Dual axis for GDP (French Sky Blue)
ax2 = ax1.twinx()
x_smooth = np.linspace(0, len(years)-1, 300)
pchip = PchipInterpolator(x, gdp_growth)
y_smooth = pchip(x_smooth)

# GDP Line in Dodger Blue
ax2.plot(x_smooth, y_smooth, color=DODGER, linewidth=2.0, linestyle=':', label='Tăng trưởng GDP (%)', zorder=5)
ax2.plot(x, gdp_growth, color=DODGER, marker='o', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)

ax2.set_ylabel('Tăng trưởng GDP (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
ax2.set_ylim(0, 10)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax2.tick_params(axis='y', labelsize=FS_TICK)

# Value annotations for bars
for bar in bars:
    h = bar.get_height()
    ax1.annotate(f'{h:.2f}T', xy=(bar.get_x() + bar.get_width()/2, h),
                 xytext=(0, 2), textcoords='offset points',
                 ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

# Value annotations for GDP line
for i, val in enumerate(gdp_growth):
    ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 5),
                 textcoords='offset points', ha='center', va='bottom',
                 fontsize=FS_VAL, fontweight='bold', color=DODGER)

ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# Combined Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper left', frameon=False, fontsize=FS_LEG)

# Chart Title
ax1.set_title('Tài sản Ngành & Phục hồi GDP Vĩ mô (2020 – 2024)', fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.savefig(os.path.join(public_dir, 'total_assets_vs_gdp.png'), dpi=350, bbox_inches='tight', transparent=True)
plt.close()


# =====================================================================
# CHART 2: VỐN ĐIỀU LỆ & VỐN CHỦ SỞ HỮU VS EQUITY/TTS (Wider side-by-side format)
# =====================================================================
fig, ax1 = plt.subplots(figsize=(5.5, 3.8), dpi=350)
x = np.arange(len(years))
bar_w = 0.26

# Grouped Bars: Charter Capital (VĐL - Dark Navy) vs Equity (VCSH - Dodger Blue)
bars1 = ax1.bar(x - bar_w/2, vdl_vals, bar_w, color=NAVY_DARK, alpha=0.90,
                edgecolor=NAVY_DARK, linewidth=0.8, label='Vốn điều lệ', zorder=3)
bars2 = ax1.bar(x + bar_w/2, vcsh_vals, bar_w, color=DODGER, alpha=0.85,
                edgecolor=NAVY_MID_D, linewidth=0.8, label='Vốn chủ sở hữu', zorder=3)

ax1.set_ylabel('Giá trị vốn (Nghìn tỷ VND)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=FS_TICK)
ax1.set_ylim(0, max(vcsh_vals) * 1.30)
ax1.tick_params(axis='y', labelsize=FS_TICK)

# Dual Axis: Equity/TTS ratio (French Sky Blue - high contrast and allowed navy)
ax2 = ax1.twinx()
pchip = PchipInterpolator(x, equity_ratio)
y_smooth = pchip(x_smooth)

ax2.plot(x_smooth, y_smooth, color=FRENCH_SKY, linewidth=2.0, linestyle=':', label='Tỷ lệ Equity/TTS', zorder=5)
ax2.plot(x, equity_ratio, color=FRENCH_SKY, marker='o', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)

ax2.set_ylabel('Equity / TTS (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
ax2.set_ylim(5, 10)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))
ax2.tick_params(axis='y', labelsize=FS_TICK)

# Annotate VĐL Bars
for bar in bars1:
    h = bar.get_height()
    ax1.annotate(f'{h:,.0f}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2), textcoords='offset points', ha='center', va='bottom', fontsize=FS_VAL-0.5, fontweight='bold', color=NAVY_DARK)

# Annotate VCSH Bars
for bar in bars2:
    h = bar.get_height()
    ax1.annotate(f'{h:,.0f}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2), textcoords='offset points', ha='center', va='bottom', fontsize=FS_VAL-0.5, fontweight='bold', color=NAVY_MID_D)

# Annotate Equity/TTS Line
for i, val in enumerate(equity_ratio):
    ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color=FRENCH_SKY)

ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# Combined Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper left', frameon=False, fontsize=FS_LEG)

# Chart Title
ax1.set_title('Tăng trưởng Vốn & Tỷ lệ An toàn Hệ thống (2020 – 2024)', fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.savefig(os.path.join(public_dir, 'slide_1_2_capital.png'), dpi=350, bbox_inches='tight', transparent=True)
plt.close()


# =====================================================================
# CHART 3: EQUITY DISPERSION BY BANK (Upgraded aspect ratio for 100% height)
# Aspect ratio set to (5.0, 8.4) to force pure vertical alignment & full slide fill
# =====================================================================
bs_2024 = bs_5y[bs_5y['Năm'] == 2024].copy()
bs_2024['equity_ratio'] = bs_2024['A64'] / bs_2024['A1'] * 100
bs_2024 = bs_2024.sort_values('equity_ratio', ascending=True)
bank_labels = [f'NH {int(b)}' for b in bs_2024['Công ty']]
er_vals = bs_2024['equity_ratio'].values

FS_TITLE_3 = 12.5
FS_LABEL_3 = 10.5
FS_TICK_3 = 9.5
FS_VAL_3 = 9.5
FS_LEG_3 = 9.5

# Taller figsize (5.0, 8.4) with high DPI to perfectly fill right column
fig, ax = plt.subplots(figsize=(5.0, 8.4), dpi=350)

# Strictly Navy Blue Gradient representation:
colors = [
    BABY_BLUE if v < 6.0 else 
    FRENCH_SKY if v < 8.0 else 
    DODGER if v < 10.0 else 
    NAVY_MID if v < 12.0 else 
    NAVY_DARK for v in er_vals
]

bars = ax.barh(bank_labels, er_vals, color=colors, height=0.62, edgecolor='white', linewidth=0.4, zorder=3)

# 6% Warning Line in NAVY_DARK (with dotted style)
ax.axvline(x=6.0, color=NAVY_DARK, linewidth=1.2, linestyle=':', zorder=4, label='Cảnh báo 6%')

# Average Line in AZURE
mean_er = bs_2024['equity_ratio'].mean()
ax.axvline(x=mean_er, color=AZURE, linewidth=1.2, linestyle='-.', zorder=4, label=f'Trung bình ({mean_er:.2f}%)')

# Annotate Bar values with correct gradient colors
for bar, val in zip(bars, er_vals):
    w = bar.get_width()
    txt_color = NAVY_DARK if val < 6.0 else NAVY_MID_D
    ax.text(w + 0.15, bar.get_y() + bar.get_height()/2, f'{val:.2f}%', va='center', ha='left', fontsize=FS_VAL_3, fontweight='bold', color=txt_color)

max_er = er_vals.max()
min_er = er_vals.min()
spread = max_er - min_er

# Custom Annotation Card for Spread
ax.annotate(f'Chênh lệch: {spread:.2f}pp', xy=(max_er - spread/2, len(er_vals) - 0.5),
            fontsize=FS_LABEL_3, fontweight='bold', color=NAVY_DARK, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=BABY_BLUE, alpha=0.25, edgecolor=NAVY_MID))

ax.set_xlabel('Tỷ lệ an toàn vốn (Equity / TTS %)', fontsize=FS_LABEL_3, fontweight='bold', labelpad=4, color=TEXT_MID)
ax.set_xlim(0, max_er + 3.0)
ax.grid(True, axis='x', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)
ax.tick_params(axis='y', labelsize=FS_TICK_3)
ax.tick_params(axis='x', labelsize=FS_TICK_3)

ax.legend(loc='lower right', frameon=False, fontsize=FS_LEG_3)

# Chart Title
ax.set_title('Phân hóa Đệm vốn toàn hệ thống (2024)', fontsize=FS_TITLE_3, fontweight='bold', pad=10, color=TEXT_DARK)

# Use tight layout and save with minimal pad to stretch chart to absolute margins
plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'slide_1_3_equity_dispersion.png'), dpi=350, bbox_inches='tight', pad_inches=0.01, transparent=True)
plt.close()

print("All premium conform side-by-side upgraded charts generated successfully in public/ folder!")

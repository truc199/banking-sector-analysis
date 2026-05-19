"""
Generate Chart for NEW Slide 1.1: Tổng tài sản toàn ngành & GDP Growth
Bar chart (Total Assets) + Dotted line (GDP Growth)
Saves to slidev/public/new_slide_1_1_assets_gdp.png
"""
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

# ─── Setup ───────────────────────────────────────────────────────────────
import matplotlib.font_manager as fm
for font_file in glob.glob(r'd:\uni\gcontest\slidev\fonts\*.ttf'):
    try:
        fm.fontManager.addfont(font_file)
    except Exception:
        pass

plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['font.sans-serif'] = ['Roboto', 'Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# ─── Color Palette ───────────────────────────────────────────────────────
NAVY_DARK    = '#003366'
NAVY_MID_D   = '#004C99'
NAVY_MID     = '#0066CC'
AZURE        = '#007FFF'
DODGER       = '#3399FF'
FRENCH_SKY   = '#66B2FF'
BABY_BLUE    = '#99CCFF'
SECONDARY_ORANGE = '#E67300'

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

# ─── Font Size Hierarchy (matching slide text) ───────────────────────────
FS_TITLE = 13
FS_LABEL = 11.5
FS_TICK  = 10.5
FS_VAL   = 10
FS_LEG   = 10

# ─── Output ──────────────────────────────────────────────────────────────
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_5y = bs[bs['Năm'].isin([2020, 2021, 2022, 2023, 2024])].copy()

years = [2020, 2021, 2022, 2023, 2024]
year_labels = ['2020', '2021', '2022', '2023', '2024']

tts_by_year = bs_5y.groupby('Năm')['A1'].sum().reindex(years)
tts_vals = (tts_by_year / 1e6).values  # Triệu tỷ VND

# YoY Growth of Total Assets
tts_growth = [None]  # no growth for first year
for i in range(1, len(tts_vals)):
    tts_growth.append((tts_vals[i] / tts_vals[i-1] - 1) * 100)

gdp_growth = [2.91, 2.58, 8.02, 5.05, 7.09]

# ─── Chart ───────────────────────────────────────────────────────────────
# Figsize optimized for col-span-6 in ImpressiveHeader (fills ~370px height)
fig, ax1 = plt.subplots(figsize=(6.0, 4.2), dpi=350)
x = np.arange(len(years))

# ── Bars: Total Assets (Navy Dark, solid, dominant) ──
bars = ax1.bar(x, tts_vals, color=NAVY_DARK, width=0.45, alpha=0.92,
               edgecolor=NAVY_DARK, linewidth=0.8, label='Tổng tài sản (Triệu tỷ VND)', zorder=3)

ax1.set_ylabel('Tổng tài sản (Triệu tỷ VND)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=TEXT_MID)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=FS_TICK, fontweight='bold')
ax1.set_ylim(0, max(tts_vals) * 1.28)
ax1.tick_params(axis='y', labelsize=FS_TICK)

# Annotate bar values on top
for bar in bars:
    h = bar.get_height()
    ax1.annotate(f'{h:.2f}', xy=(bar.get_x() + bar.get_width()/2, h),
                 xytext=(0, 3), textcoords='offset points',
                 ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

# ── Dual Axis: GDP Growth Line (Orange, dotted, PCHIP smoothed) ──
ax2 = ax1.twinx()
x_smooth = np.linspace(0, len(years)-1, 300)
pchip = PchipInterpolator(x, gdp_growth)
y_smooth = pchip(x_smooth)

ax2.plot(x_smooth, y_smooth, color=SECONDARY_ORANGE, linewidth=2.2, linestyle=':',
         label='Tăng trưởng GDP (%)', zorder=5)
ax2.plot(x, gdp_growth, color=SECONDARY_ORANGE, marker='o', markersize=6,
         markerfacecolor='white', markeredgewidth=2.0, linestyle='None', zorder=6)

ax2.set_ylabel('Tăng trưởng GDP (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=TEXT_MID)
ax2.set_ylim(0, 10.5)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax2.tick_params(axis='y', labelsize=FS_TICK)

# Annotate GDP values
for i, val in enumerate(gdp_growth):
    ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 6),
                 textcoords='offset points', ha='center', va='bottom',
                 fontsize=FS_VAL, fontweight='bold', color=SECONDARY_ORANGE)

# ── Grid & Spines ──
ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# ── Combined Legend at bottom ──
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, -0.12),
           ncol=2, frameon=False, fontsize=FS_LEG)

# ── Title ──
ax1.set_title('Tổng tài sản Ngành Ngân hàng & Tăng trưởng GDP (2020 – 2024)',
              fontsize=FS_TITLE, fontweight='bold', pad=12, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_1_1_assets_gdp.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

# ─── Print verification ─────────────────────────────────────────────────
print("=== VERIFICATION ===")
print(f"Total Assets (triệu tỷ VND): {dict(zip(years, [f'{v:.2f}' for v in tts_vals]))}")
print(f"GDP Growth (%): {dict(zip(years, gdp_growth))}")
cumulative = (tts_vals[-1] / tts_vals[0] - 1) * 100
print(f"Cumulative asset growth 2020->2024: +{cumulative:.1f}%")
print(f"Chart saved to: {os.path.join(public_dir, 'new_slide_1_1_assets_gdp.png')}")

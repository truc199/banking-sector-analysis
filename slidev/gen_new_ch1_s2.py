"""
Generate Chart for NEW Slide 1.2: Vốn điều lệ & Vốn CSH + Equity/TTS ratio
Grouped bar chart + Dotted line (Equity/TTS)
Saves to slidev/public/new_slide_1_2_capital.png
"""
import os, glob
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

# ─── Font Sizes ──────────────────────────────────────────────────────────
FS_TITLE = 13
FS_LABEL = 11.5
FS_TICK  = 10.5
FS_VAL   = 9.5
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

vdl_by_year  = bs_5y.groupby('Năm')['A66'].sum().reindex(years)
vcsh_by_year = bs_5y.groupby('Năm')['A64'].sum().reindex(years)
tts_by_year  = bs_5y.groupby('Năm')['A1'].sum().reindex(years)

vdl_vals  = (vdl_by_year / 1000).values   # nghìn tỷ VND
vcsh_vals = (vcsh_by_year / 1000).values   # nghìn tỷ VND

# Equity/TTS simple mean per bank
bs_5y['equity_ratio'] = bs_5y['A64'] / bs_5y['A1'] * 100
equity_ratio = bs_5y.groupby('Năm')['equity_ratio'].mean().reindex(years).values

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(6.0, 4.2), dpi=350)
x = np.arange(len(years))
bar_w = 0.28

# ── Grouped Bars: VĐL (Navy Dark) & VCSH (Dodger Blue) ──
bars1 = ax1.bar(x - bar_w/2, vdl_vals, bar_w, color=NAVY_DARK, alpha=0.92,
                edgecolor=NAVY_DARK, linewidth=0.8, label='Vốn điều lệ (VĐL)', zorder=3)
bars2 = ax1.bar(x + bar_w/2, vcsh_vals, bar_w, color=DODGER, alpha=0.88,
                edgecolor=NAVY_MID_D, linewidth=0.8, label='Vốn chủ sở hữu (VCSH)', zorder=3)

ax1.set_ylabel('Giá trị vốn (Nghìn tỷ VND)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=TEXT_MID)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=FS_TICK, fontweight='bold')
ax1.set_ylim(0, max(vcsh_vals) * 1.30)
ax1.tick_params(axis='y', labelsize=FS_TICK)

# Annotate bar values (removed per user request)
# for bar in bars1:
#     h = bar.get_height()
#     ax1.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
#                  xytext=(0, 3), textcoords='offset points',
#                  ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

# for bar in bars2:
#     h = bar.get_height()
#     ax1.annotate(f'{h:,.0f}', xy=(bar.get_x() + bar.get_width()/2, h),
#                  xytext=(0, 3), textcoords='offset points',
#                  ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color=NAVY_MID_D)

# ── Dual Axis: Equity/TTS Line (Orange, dotted, PCHIP) ──
ax2 = ax1.twinx()
x_smooth = np.linspace(0, len(years)-1, 300)
pchip = PchipInterpolator(x, equity_ratio)
y_smooth = pchip(x_smooth)

ax2.plot(x_smooth, y_smooth, color=SECONDARY_ORANGE, linewidth=2.2, linestyle=':',
         label='Equity/TTS (%)', zorder=5)
ax2.plot(x, equity_ratio, color=SECONDARY_ORANGE, marker='o', markersize=6,
         markerfacecolor='white', markeredgewidth=2.0, linestyle='None', zorder=6)

ax2.set_ylabel('Equity / TTS (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=TEXT_MID)
ax2.set_ylim(6.0, 10.5)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax2.tick_params(axis='y', labelsize=FS_TICK)

# Annotate Equity/TTS values
for i, val in enumerate(equity_ratio):
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
           ncol=3, frameon=False, fontsize=FS_LEG)

# ── Title ──
ax1.set_title('Tăng trưởng Vốn & Tỷ lệ An toàn Vốn Hệ thống (2020 – 2024)',
              fontsize=FS_TITLE, fontweight='bold', pad=12, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_1_2_capital.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE')

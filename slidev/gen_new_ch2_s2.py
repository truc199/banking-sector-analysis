"""
Generate Chart for NEW Slide 2.2: NIM toàn ngành (2020-2024)
Vertical bar chart + PCHIP trend line
Saves to slidev/public/new_slide_2_2_nim.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

# ─── Setup ───────────────────────────────────────────────────────────────
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
FS_LABEL = 11
FS_TICK  = 10.5
FS_VAL   = 9.5
FS_LEG   = 10

# ─── Output ──────────────────────────────────────────────────────────────
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
is_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)

years = [2020, 2021, 2022, 2023, 2024]

merged = pd.merge(
    bs[['Công ty', 'Năm', 'A1']],
    inc[['Công ty', 'Năm', 'B3']],
    on=['Công ty', 'Năm']
)
merged = merged[merged['Năm'].isin(years)].copy()
merged['NIM'] = merged['B3'] / merged['A1'] * 100

nim_avg = merged.groupby('Năm')['NIM'].mean().reindex(years).values

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=350)
x = np.arange(len(years))
bar_w = 0.5

# Bar colors: highlight 2022 peak
bar_colors = [NAVY_MID_D, NAVY_MID, NAVY_DARK, DODGER, DODGER]

bars = ax.bar(x, nim_avg, bar_w, color=bar_colors, alpha=0.90,
              edgecolor='white', linewidth=0.8, zorder=3)

ax.set_ylabel('NIM trung bình (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=TEXT_MID)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=FS_TICK, fontweight='bold')
ax.set_ylim(0, max(nim_avg) * 1.35)
ax.tick_params(axis='y', labelsize=FS_TICK)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Grid & Spines
ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

# Legend at bottom
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=NAVY_DARK, edgecolor='white', label='NIM trung bình hệ thống (%)')
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.12),
          ncol=1, frameon=False, fontsize=FS_LEG)

# Title
ax.set_title('Biên lãi thuần (NIM) Trung bình Hệ thống (2020 – 2024)',
             fontsize=FS_TITLE, fontweight='bold', pad=12, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_2_2_nim.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE')

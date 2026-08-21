"""
Generate Chart for Slide 3.1: Income Composition (100% Stacked Area)
TOI breakdown: Interest vs Non-Interest components (2020-2024)
Saves to slidev/public/new_slide_3_1_income_mix.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# --- Đường dẫn tương đối theo vị trí file (không phụ thuộc máy) ---
import sys as _sys
_sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
PUBLIC = ROOT / "slidev" / "public"
FONTS = ROOT / "slidev" / "fonts"
# ------------------------------------------------------------------

# ─── Setup ───────────────────────────────────────────────────────────────
for font_file in glob.glob(str(FONTS / "*.ttf")):
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
NAVY_MID     = '#0066CC'
AZURE        = '#007FFF'
DODGER       = '#3399FF'
FRENCH_SKY   = '#66B2FF'
BABY_BLUE    = '#99CCFF'
TEAL         = '#00897B'
ORANGE       = '#E67300'

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

FS_TITLE = 12
FS_LABEL = 10.5
FS_TICK  = 10
FS_VAL   = 9
FS_LEG   = 9

# ─── Output ──────────────────────────────────────────────────────────────
public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
is_file = glob.glob(str(DATA / "*Income*"))[0]
inc = pd.read_csv(is_file)
years = [2020, 2021, 2022, 2023, 2024]
inc_y = inc[inc['Năm'].isin(years)]

# System-level aggregation (weighted by size)
agg = inc_y.groupby('Năm').agg({
    'B3': 'sum',   # Net Interest Income
    'B6': 'sum',   # Net Fee Income
    'B7': 'sum',   # FX & Gold
    'B8': 'sum',   # Securities Trading
    'B9': 'sum',   # Securities Investment
    'B12': 'sum',  # Other
    'B13': 'sum',  # Equity Investment
    'B14': 'sum',  # TOI
}).reindex(years)

# As % of TOI
components = {
    'Thu nh\u1eadp l\u00e3i thu\u1ea7n': agg['B3'] / agg['B14'] * 100,
    'D\u1ecbch v\u1ee5 (thu\u1ea7n)': agg['B6'] / agg['B14'] * 100,
    'Ngo\u1ea1i h\u1ed1i & V\u00e0ng': agg['B7'] / agg['B14'] * 100,
    'CK Kinh doanh': agg['B8'] / agg['B14'] * 100,
    'CK \u0110\u1ea7u t\u01b0': agg['B9'] / agg['B14'] * 100,
    'Ho\u1ea1t \u0111\u1ed9ng kh\u00e1c': (agg['B12'] + agg['B13']) / agg['B14'] * 100,
}

# ─── Chart: 100% Stacked Area ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=350)

x = np.arange(len(years))
colors = [NAVY_DARK, TEAL, ORANGE, DODGER, FRENCH_SKY, BABY_BLUE]
labels = list(components.keys())
data = np.array([components[k].values for k in labels])

ax.stackplot(x, data, labels=labels, colors=colors, alpha=0.88, edgecolor='white', linewidth=0.5)

ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=FS_TICK, fontweight='bold')
ax.set_ylabel('T\u1ef7 tr\u1ecdng (% TOI)', fontsize=FS_LABEL, fontweight='bold', labelpad=6)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.tick_params(axis='y', labelsize=FS_TICK)

ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

# Legend at bottom
handles, lbls = ax.get_legend_handles_labels()
ax.legend(handles[::-1], lbls[::-1], loc='upper center', bbox_to_anchor=(0.5, -0.10),
          ncol=3, frameon=False, fontsize=FS_LEG)

ax.set_title('C\u01a1 c\u1ea5u Thu nh\u1eadp Ho\u1ea1t \u0111\u1ed9ng (TOI) to\u00e0n H\u1ec7 th\u1ed1ng',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_3_1_income_mix.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE chart 1')

# Print key stats for text
non_int_ratio_2020 = (1 - agg.loc[2020, 'B3'] / agg.loc[2020, 'B14']) * 100
non_int_ratio_2024 = (1 - agg.loc[2024, 'B3'] / agg.loc[2024, 'B14']) * 100
fee_ratio_2020 = agg.loc[2020, 'B6'] / agg.loc[2020, 'B14'] * 100
fee_ratio_2024 = agg.loc[2024, 'B6'] / agg.loc[2024, 'B14'] * 100
int_ratio_2020 = agg.loc[2020, 'B3'] / agg.loc[2020, 'B14'] * 100
int_ratio_2024 = agg.loc[2024, 'B3'] / agg.loc[2024, 'B14'] * 100
print(f'Interest Ratio: {int_ratio_2020:.2f}% -> {int_ratio_2024:.2f}%')
print(f'Non-Interest Ratio: {non_int_ratio_2020:.2f}% -> {non_int_ratio_2024:.2f}%')
print(f'Fee Ratio: {fee_ratio_2020:.2f}% -> {fee_ratio_2024:.2f}%')

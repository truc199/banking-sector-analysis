"""
Generate Chart for Slide 3.2: CIR Dispersion (2024)
Horizontal bar chart — CIR per bank (excluding NH22 outlier)
Saves to slidev/public/new_slide_3_2_cir_dispersion.png
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
RED_BRICK    = '#CC3333'
TEAL         = '#00897B'

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

FS_TITLE = 11.5
FS_LABEL = 10
FS_TICK  = 8.5
FS_VAL   = 8.0
FS_LEG   = 9

# ─── Output ──────────────────────────────────────────────────────────────
public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
is_file = glob.glob(str(DATA / "*Income*"))[0]
inc = pd.read_csv(is_file)

# CIR = |OPEX (B15)| / TOI (B14) * 100
inc_2024 = inc[inc['Năm'] == 2024].copy()
inc_2024['CIR'] = abs(inc_2024['B15']) / inc_2024['B14'] * 100

# Exclude NH22 (negative TOI => CIR meaningless)
inc_2024 = inc_2024[inc_2024['Công ty'] != 22].copy()

inc_2024 = inc_2024.sort_values('CIR', ascending=True)
bank_labels = [f'NH {int(b)}' for b in inc_2024['Công ty']]
cir_vals = inc_2024['CIR'].values

# System mean (excl NH22)
mean_cir = cir_vals.mean()

# Color gradient: lower CIR = better (teal/navy), higher CIR = worse (red-ish)
colors = []
for v in cir_vals:
    if v < 35:
        colors.append(TEAL)
    elif v < 45:
        colors.append(DODGER)
    elif v < 55:
        colors.append(FRENCH_SKY)
    elif v < 65:
        colors.append(BABY_BLUE)
    else:
        colors.append(RED_BRICK)

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=350)

bars = ax.barh(bank_labels, cir_vals, color=colors, height=0.60,
               edgecolor='white', linewidth=0.4, zorder=3)

# Mean reference line
ax.axvline(x=mean_cir, color=AZURE, linewidth=1.0, linestyle='-.',
           alpha=0.45, zorder=2, label=f'Trung b\u00ecnh ({mean_cir:.1f}%)')

# Value labels
for bar, val in zip(bars, cir_vals):
    w = bar.get_width()
    txt_color = RED_BRICK if val > 60 else TEXT_MID
    ax.text(w + 0.5, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', ha='left',
            fontsize=FS_VAL, fontweight='bold', color=txt_color)

ax.set_xlabel('CIR (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
ax.set_xlim(0, max(cir_vals) + 8)
ax.grid(True, axis='x', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)
ax.tick_params(axis='y', labelsize=FS_TICK)
ax.tick_params(axis='x', labelsize=FS_TICK)

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07),
          ncol=1, frameon=False, fontsize=FS_LEG)

ax.set_title('Ph\u00e2n h\u00f3a Chi ph\u00ed Ho\u1ea1t \u0111\u1ed9ng (CIR) n\u0103m 2024',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_3_2_cir_dispersion.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

gap = cir_vals.max() - cir_vals.min()
print(f'CIR Gap (excl NH22): {gap:.2f}pp (Min={cir_vals.min():.2f}%, Max={cir_vals.max():.2f}%)')
print(f'CIR Mean (excl NH22): {mean_cir:.2f}%')
print('DONE chart 2')

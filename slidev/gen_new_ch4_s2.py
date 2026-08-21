"""
Generate Chart for Slide 4.2: LDR Trend (2020-2024)
Line chart with threshold marker
Saves to slidev/public/new_slide_4_2_ldr.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

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
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

NAVY_DARK    = '#003366'
RED_BRICK    = '#CC3333'
GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'

FS_TITLE = 11.5
FS_LABEL = 10
FS_TICK  = 8.5
FS_VAL   = 9

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(str(DATA / "*Balance*"))[0]
bs = pd.read_csv(bs_file)

years = [2020, 2021, 2022, 2023, 2024]
bs_y = bs[bs['Năm'].isin(years)].copy()

bs_y['LDR'] = bs_y['A12'] / bs_y['A55'] * 100
ldr_avg = bs_y.groupby('Năm')['LDR'].mean().reindex(years).values

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=350)
x = np.arange(len(years))

# PCHIP Line
x_smooth = np.linspace(0, len(years)-1, 300)
pchip = PchipInterpolator(x, ldr_avg)

ax.plot(x_smooth, pchip(x_smooth), color=NAVY_DARK, linewidth=2.5, zorder=3)
ax.plot(x, ldr_avg, color=NAVY_DARK, marker='o', markersize=7,
        markerfacecolor='white', markeredgewidth=2.2, linestyle='None', zorder=4)

# 100% threshold
ax.axhline(y=100, color=RED_BRICK, linewidth=1.5, linestyle='--', zorder=2, label='Ng\u01b0\u1ee1ng 100%')

for i, val in enumerate(ldr_avg):
    y_offset = -1.5 if val < 100 else 1.2
    va = 'top' if val < 100 else 'bottom'
    color = NAVY_DARK if val < 100 else RED_BRICK
    ax.text(x[i], val + y_offset, f'{val:.1f}%', ha='center', va=va,
            fontsize=FS_VAL, fontweight='bold', color=color)

ax.set_ylabel('LDR trung b\u00ecnh (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=FS_TICK, fontweight='bold')
ax.set_ylim(85, 110)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.tick_params(axis='y', labelsize=FS_TICK)

ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

ax.legend(loc='upper left', frameon=False, fontsize=FS_VAL)

ax.set_title('T\u1ef7 l\u1ec7 D\u01b0 n\u1ee3 / Huy \u0111\u1ed9ng (LDR) Trung b\u00ecnh H\u1ec7 th\u1ed1ng',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_4_2_ldr.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

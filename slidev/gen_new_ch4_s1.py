"""
Generate Chart for Slide 4.1: CASA Ratio Trend (2020-2024)
Line chart with PCHIP interpolation
Saves to slidev/public/new_slide_4_1_casa.png
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
ORANGE       = '#E67300'
TEAL         = '#00897B'
GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'

FS_TITLE = 11.5
FS_LABEL = 10
FS_TICK  = 8.5
FS_VAL   = 9
FS_LEG   = 9

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(str(DATA / "*Balance*"))[0]
n_file = glob.glob(str(DATA / "*Note*"))[0]
bs = pd.read_csv(bs_file)
note = pd.read_csv(n_file)

years = [2020, 2021, 2022, 2023, 2024]
bs_y = bs[bs['Năm'].isin(years)]
note_y = note[note['Năm'].isin(years)]

df = pd.merge(bs_y[['Công ty', 'Năm', 'A55']], note_y[['Công ty', 'Năm', 'C68']], on=['Công ty', 'Năm'])
df['CASA'] = df['C68'] / df['A55'] * 100

casa_avg = df.groupby('Năm')['CASA'].mean().reindex(years).values

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=350)
x = np.arange(len(years))

x_smooth = np.linspace(0, len(years)-1, 300)
pchip = PchipInterpolator(x, casa_avg)

ax.plot(x_smooth, pchip(x_smooth), color=NAVY_DARK, linewidth=2.5, zorder=3)
ax.plot(x, casa_avg, color=NAVY_DARK, marker='o', markersize=7,
        markerfacecolor='white', markeredgewidth=2.2, linestyle='None', zorder=4)

for i, val in enumerate(casa_avg):
    y_offset = 0.5 if i != 2 else -0.8
    va = 'bottom' if i != 2 else 'top'
    ax.text(x[i], val + y_offset, f'{val:.2f}%', ha='center', va=va,
            fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

ax.set_ylabel('CASA Ratio (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=FS_TICK, fontweight='bold')
ax.set_ylim(min(casa_avg) - 2, max(casa_avg) + 2)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.tick_params(axis='y', labelsize=FS_TICK)

ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

ax.set_title('T\u1ef7 l\u1ec7 Ti\u1ec1n g\u1eedi kh\u00f4ng k\u1ef3 h\u1ea1n (CASA) Trung b\u00ecnh H\u1ec7 th\u1ed1ng',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_4_1_casa.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

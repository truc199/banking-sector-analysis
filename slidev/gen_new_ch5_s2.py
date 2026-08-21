"""
Generate Chart for Slide 5.2: NPL Coverage Ratio (LLR) 2024
Scatter plot with log scale and adjustText
Saves to slidev/public/new_slide_5_2_llr.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from adjustText import adjust_text

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
TEAL         = '#00897B'
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
n_file = glob.glob(str(DATA / "*Note*"))[0]

bs = pd.read_csv(bs_file)
note = pd.read_csv(n_file)

df = pd.merge(bs[['Công ty', 'Năm', 'A14']], note[['Công ty', 'Năm', 'C32', 'C35', 'C36', 'C37']], on=['Công ty', 'Năm'])
df_2024 = df[df['Năm'] == 2024].copy()

df_2024['NPL_Amount'] = df_2024['C35'] + df_2024['C36'] + df_2024['C37']
df_2024['NPL_Ratio'] = df_2024['NPL_Amount'] / df_2024['C32'] * 100
df_2024['LLR'] = abs(df_2024['A14']) / df_2024['NPL_Amount'] * 100

df_2024 = df_2024.dropna(subset=['LLR', 'NPL_Ratio'])

# ─── Chart: Scatter Plot ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=350)

# Set scales before plotting thresholds
ax.set_yscale('log')
ax.set_xscale('log')

for i, row in df_2024.iterrows():
    llr = row['LLR']
    npl = row['NPL_Ratio']
    
    if llr < 100:
        c = RED_BRICK
    elif llr > 150:
        c = TEAL
    else:
        c = NAVY_DARK
        
    ax.scatter(npl, llr, color=c, s=100, alpha=0.8, edgecolor='white', linewidth=0.5, zorder=4)

# Thresholds
ax.axhline(y=100, color=RED_BRICK, linewidth=1.5, linestyle='--', zorder=2, label='Ng\u01b0\u1ee1ng b\u00e1o \u0111\u1ed9ng (<100%)')
ax.axhline(y=150, color=TEAL, linewidth=1.5, linestyle=':', zorder=2, label='Ng\u01b0\u1ee1ng an to\u00e0n (>150%)')
ax.axvline(x=3.0, color='gray', linewidth=1.0, linestyle='-.', zorder=2, alpha=0.5)

ax.set_xlabel('T\u1ef7 l\u1ec7 N\u1ee3 x\u1ea5u (NPL, %) - Log Scale', fontsize=FS_LABEL, fontweight='bold', labelpad=6)
ax.set_ylabel('T\u1ef7 l\u1ec7 Bao ph\u1ee7 n\u1ee3 x\u1ea5u (LLR, %) - Log Scale', fontsize=FS_LABEL, fontweight='bold', labelpad=6)

# Formatters for log scale
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: '{:g}%'.format(y)))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: '{:g}%'.format(y)))
ax.tick_params(axis='both', labelsize=FS_TICK)

# No text adjustment needed

ax.grid(True, which='both', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

# Legend placement
ax.legend(loc='upper right', frameon=True, fontsize=FS_TICK, framealpha=0.9, edgecolor=SPINE_COLOR)

ax.set_title('Ph\u00e2n h\u00f3a R\u1ee7i ro T\u00e0i s\u1ea3n: NPL vs LLR (N\u0103m 2024)',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_5_2_llr.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

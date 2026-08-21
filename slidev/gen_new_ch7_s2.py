"""
Generate Scatter Quadrant Plot for Slide 7.2:
X-axis: LDR Ratio (%), from 60% to 150%
Y-axis: GTCG/Deposit Ratio (%), from 0% to 35%
Averaged over Phase 2 (2022-2023)
Saves to d:\\uni\\gcontest\\slidev\\public\\new_slide_7_2_liquidity_quadrant.png
"""
import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches

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

# Setup fonts
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
RED          = '#C0392B'
ORANGE       = '#E67E22'
TEAL         = '#0D9488'
GRID_COLOR   = '#f1f5f9'
TEXT_DARK    = '#0f172a'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# Load data
bs = pd.read_csv(DATA / "[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
note = pd.read_csv(DATA / "[G'Contest 2026] Đề Vòng 2_3. Note.csv")
df = bs.merge(note, on=['Công ty', 'Năm'], how='inner')

# Calculate metrics for each row
df['LDR'] = (df['A13'] / df['A55']) * 100
df['GTCG_DEP'] = (df['A58'] / df['A55']) * 100

# Filter for phase 2 (2022-2023)
gd2 = df[df['Năm'].isin([2022, 2023])].copy()

# Average over phase 2 for each bank
grouped = gd2.groupby('Công ty')[['LDR', 'GTCG_DEP']].mean().reset_index()

# Plot
fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=350)

# Colors mapping based on quadrants
colors = []
for idx, r in grouped.iterrows():
    if r['LDR'] > 100 and r['GTCG_DEP'] > 5:
        colors.append(RED)
    elif r['LDR'] > 100:
        colors.append(ORANGE)
    elif r['GTCG_DEP'] > 5:
        colors.append('#E67E22') # Amber
    else:
        colors.append(TEAL)

# Plot scatter points
ax.scatter(grouped['LDR'], grouped['GTCG_DEP'], color=colors, s=55, edgecolor='black', linewidth=0.5, zorder=5)

# Removed bank labels from points to simplify visualization


# Draw limits
ax.axvline(100, color=RED, lw=1.2, ls='--', zorder=3, alpha=0.8)
ax.axhline(5, color=ORANGE, lw=1.2, ls='--', zorder=3, alpha=0.8)

# Highlight zones with shading
ax.fill_between([100, 150], 5, 35, color=RED, alpha=0.06)
ax.fill_between([100, 150], 0, 5, color=ORANGE, alpha=0.06)
ax.fill_between([60, 100], 5, 35, color='#E67E22', alpha=0.04)
ax.fill_between([60, 100], 0, 5, color=TEAL, alpha=0.06)

# Add zone labels (watermark-like)
ax.text(125, 20, "C\u1ef0C K\u1ef2 R\u1ee6I RO\n(LDR > 100% & GTCG > 5%)\n14 Ng\u00e2n h\u00e0ng", 
        color=RED, fontsize=8, fontweight='bold', ha='center', va='center', alpha=0.3, zorder=1)
ax.text(80, 2, "V\u00d9NG AN TO\u00c0N\n(LDR \u2264 100% & GTCG \u2264 5%)", 
        color=TEAL, fontsize=8, fontweight='bold', ha='center', va='center', alpha=0.3, zorder=1)
ax.text(80, 20, "CHI PH\u00cd V\u1ed0N CAO\n(GTCG > 5%)", 
        color='#E67E22', fontsize=8, fontweight='bold', ha='center', va='center', alpha=0.3, zorder=1)

ax.set_xlabel("T\u1ef7 l\u1ec7 LDR trung b\u00ecnh (%)", fontsize=9.5, fontweight='bold', color='#1E293B', labelpad=6)
ax.set_ylabel("T\u1ef7 l\u1ec7 GTCG / Ti\u1ec1n g\u1eedi (%)", fontsize=9.5, fontweight='bold', color='#1E293B', labelpad=6)
ax.set_title("B\u1ea3n \u0111\u1ed3 LDR vs T\u1ef7 l\u1ec7 GTCG / Ti\u1ec1n g\u1eedi G\u01102 (2022-2023)\n(Ph\u00e2n v\u00f9ng c\u1ea3nh b\u00e1o R\u1ee7i ro Thanh kho\u1ea3n & K\u1ef3 h\u1ea1n)", 
             fontsize=11.5, fontweight='bold', pad=15, color=TEXT_DARK)

ax.set_xlim(60, 150)
ax.set_ylim(0, 35)

ax.grid(True, ls='--', color=GRID_COLOR, alpha=0.8, zorder=0)

# Legend
patches = [
    mpatches.Patch(color=RED, alpha=0.15, label='C\u1ef1c k\u1ef3 r\u1ee7i ro (LDR > 100% & GTCG > 5%): 14 NH'),
    mpatches.Patch(color='#E67E22', alpha=0.1, label='Chi ph\u00ed v\u1ed1n cao (GTCG > 5%): 6 NH'),
    mpatches.Patch(color=TEAL, alpha=0.15, label='V\u00f9ng an to\u00e0n (LDR \u2264 100% & GTCG \u2264 5%): 7 NH'),
]
ax.legend(handles=patches, loc='upper left', fontsize=8.5, framealpha=0.9)

plt.tight_layout()
path = os.path.join(public_dir, 'new_slide_7_2_liquidity_quadrant.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 7.2 chart successfully!")

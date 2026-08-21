"""
Generate Chart for Slide 6.1: Macro Context 2020-2021
Combo Line & Shaded Area Chart
Saves to slidev/public/new_slide_6_1_macro.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np

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
AZURE        = '#007FFF'
ORANGE       = '#E67300'
RED_BRICK    = '#CC3333'
GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'

FS_TITLE = 11.5
FS_LABEL = 9.5
FS_TICK  = 8
FS_VAL   = 8

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
months = ['T1/20', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12',
          'T1/21', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
x = np.arange(len(months))

# PMI Data (Right Axis)
pmi = [50.6, 49.0, 41.9, 32.7, 42.7, 51.1, 47.6, 45.3, 52.2, 51.8, 49.9, 51.7,
       51.3, 51.6, 53.6, 54.7, 53.1, 44.1, 40.0, 40.2, 40.2, 52.1, 52.2, 52.5]

# Retail Sales YoY (Left Axis)
retail = [5.4, 4.8, -0.8, -26.0, -4.8, 5.3, 4.3, 1.9, 4.9, 6.1, 8.5, 9.4,
          6.4, 8.2, 9.2, 30.0, -1.0, -6.6, -19.8, -33.7, -28.4, -19.5, -12.2, -1.1]

# GDP YoY (Left Axis, Quarterly mapped to months 2, 5, 8, 11 for plotting in middle of Q)
gdp_q_idx = [1, 4, 7, 10, 13, 16, 19, 22] # Feb, May, Aug, Nov
gdp_val = [3.68, 0.39, 2.69, 4.48, 4.72, 6.61, -6.02, 5.22]

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(7.5, 4.2), dpi=350)
ax2 = ax1.twinx()

# Shaded areas for Lockdown
# Q2/2020: Apr-Jun (idx 3 to 5)
ax1.axvspan(3, 5, color='gray', alpha=0.15, zorder=0, label='Gi\u00e3n c\u00e1ch to\u00e0n qu\u1ed1c (Q2/20)')
# Q3/2021: Jul-Sep (idx 18 to 20)
ax1.axvspan(18, 20, color='gray', alpha=0.15, zorder=0, label='Gi\u00e3n c\u00e1ch Q3/21')

# GDP Bars
bars = ax1.bar(gdp_q_idx, gdp_val, width=2.6, color=AZURE, alpha=0.4, label='GDP t\u0103ng tr\u01b0\u1edfng (YoY %)', zorder=2)
for i, v in zip(gdp_q_idx, gdp_val):
    y_off = 1 if v > 0 else -3
    ax1.text(i, v + y_off, f'{v:.1f}%', ha='center', va='center', color=AZURE, fontweight='bold', fontsize=7)

# Retail Line
ax1.plot(x, retail, color=ORANGE, linewidth=2, marker='o', markersize=4, label='T\u1ed5ng m\u1ee9c b\u00e1n l\u1ebb (YoY %)', zorder=4)

# PMI Line
ax2.plot(x, pmi, color=RED_BRICK, linewidth=2.5, linestyle='-.', label='Ch\u1ec9 s\u1ed1 PMI s\u1ea3n xu\u1ea5t (\u0111i\u1ec3m)', zorder=5)
ax2.axhline(50, color=RED_BRICK, linestyle=':', alpha=0.6, zorder=1) # 50 threshold

# Annotations
# PMI drop Apr 2020
ax2.annotate('PMI t\u1ee5t \u0111\u00e1y: 32.7', xy=(3, 32.7), xytext=(4, 25),
             arrowprops=dict(facecolor=RED_BRICK, arrowstyle='->'),
             fontsize=8, fontweight='bold', color=RED_BRICK)
ax2.annotate('PMI suy y\u1ebfu', xy=(19, 40.2), xytext=(15, 30),
             arrowprops=dict(facecolor=RED_BRICK, arrowstyle='->'),
             fontsize=8, fontweight='bold', color=RED_BRICK)

# Circulars
ax1.annotate('Th\u00f4ng t\u01b0 01\n(C\u01a1 c\u1ea5u n\u1ee3)', xy=(2, 20), xytext=(2, 35),
             arrowprops=dict(facecolor=NAVY_DARK, width=1.5, headwidth=6),
             ha='center', fontsize=8, fontweight='bold', color=NAVY_DARK,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=NAVY_DARK, alpha=0.8))

ax1.annotate('Th\u00f4ng t\u01b0 03\n(S\u1eeda \u0111\u1ed5i TT01)', xy=(15, 20), xytext=(15, 35),
             arrowprops=dict(facecolor=NAVY_DARK, width=1.5, headwidth=6),
             ha='center', fontsize=8, fontweight='bold', color=NAVY_DARK,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=NAVY_DARK, alpha=0.8))

# Formatting
ax1.set_xticks(x)
ax1.set_xticklabels(months, rotation=45, ha='right', fontsize=7)
ax1.set_ylabel('T\u0103ng tr\u01b0\u1edfng (YoY %)', fontsize=FS_LABEL, fontweight='bold', color=NAVY_DARK, labelpad=6)
ax2.set_ylabel('Ch\u1ec9 s\u1ed1 PMI (\u0110i\u1ec3m)', fontsize=FS_LABEL, fontweight='bold', color=RED_BRICK, labelpad=6)

ax1.set_ylim(-40, 45)
ax2.set_ylim(20, 65)

ax1.tick_params(axis='y', colors=NAVY_DARK, labelsize=FS_TICK)
ax2.tick_params(axis='y', colors=RED_BRICK, labelsize=FS_TICK)

ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center', bbox_to_anchor=(0.5, -0.15),
           ncol=4, frameon=False, fontsize=7)

ax1.set_title('T\u00e1c \u0111\u1ed9ng k\u00e9p c\u1ee7a COVID-19: C\u00fa s\u1ed1c t\u0103ng tr\u01b0\u1edfng & Ph\u1ea3n \u1ee9ng ch\u00ednh s\u00e1ch',
              fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_6_1_macro.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

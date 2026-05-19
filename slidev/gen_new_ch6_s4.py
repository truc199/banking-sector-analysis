"""
Generate Chart for Slide 6.4: Nợ ẩn & Trái phiếu VAMC
Dual-Axis Combo Chart (Stacked Bar + Line)
Saves to slidev/public/new_slide_6_4_no_an_vamc.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ─── Setup ───────────────────────────────────────────────────────────────
for font_file in glob.glob(r'd:\uni\gcontest\slidev\fonts\*.ttf'):
    try:
        fm.fontManager.addfont(font_file)
    except Exception:
        pass

plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ─── Colors ──────────────────────────────────────────────────────────────
# 10 colors for 10 banks (VAMC stacked segments)
vamc_colors = [
    '#002244', '#003366', '#004C99', '#0066CC', 
    '#007FFF', '#3399FF', '#66B2FF', '#99CCFF', 
    '#0D9488', '#E67300'
]
GRAY_NPL   = '#78909C'
RED_N2     = '#CC3333'
GRID_COLOR = '#f1f5f9'
SPINE_COLOR = '#cbd5e1'
TEXT_DARK  = '#0f172a'

# ─── Data ────────────────────────────────────────────────────────────────
# 10 banks: NH 3, NH 9, NH 10, NH 12, NH 14, NH 19, NH 22, NH 25, NH 26, NH 27
banks = ['NH 3', 'NH 9', 'NH 10', 'NH 12', 'NH 14', 'NH 19', 'NH 22', 'NH 25', 'NH 26', 'NH 27']

# VAMC values in billion VND
vamc_data = {
    'NH 3':  [0.0, 169.684],
    'NH 9':  [4246.91, 0.0],
    'NH 10': [27322.052, 23727.969],
    'NH 12': [2032.481, 0.0],
    'NH 14': [42.38, 42.0],
    'NH 19': [1512.094, 823.812],
    'NH 22': [5866.923, 5699.462],
    'NH 25': [752.229, 657.446],
    'NH 26': [574.511529, 707.649],
    'NH 27': [1950.033, 1377.193]
}

years = ['2020', '2021']
x = np.arange(len(years))

npl = [1.74, 1.78]
n2 = [1.25, 1.67]

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(6.5, 4.5), dpi=350)

# 1. Stacked Bars on Y2 (Right Axis)
ax2 = ax1.twinx()

bottoms = np.zeros(2)
for i, bank in enumerate(banks):
    vals = np.array(vamc_data[bank])
    ax2.bar(x, vals, bottom=bottoms, width=0.35, label=bank, color=vamc_colors[i], edgecolor='white', linewidth=0.5, zorder=2)
    bottoms += vals

# Write total values on top of bars
for idx, tot in enumerate(bottoms):
    ax2.annotate(f'{tot/1000:.1f}k t\u1ef7',
                xy=(idx, tot),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', fontsize=8.5, color=TEXT_DARK)

# 2. Lines on Y1 (Left Axis)
line1, = ax1.plot(x, npl, color=GRAY_NPL, linewidth=2.5, marker='o', label='T\u1ef7 l\u1ec7 N\u1ee3 x\u1ea5u (NPL) b\u00e1o c\u00e1o', zorder=5)
line2, = ax1.plot(x, n2, color=RED_N2, linewidth=2.5, marker='s', label='T\u1ef7 l\u1ec7 N\u1ee3 Nh\u00f3m 2 (Watch-list)', zorder=5)

# Value annotations for lines
for idx, val in enumerate(npl):
    ax1.annotate(f'{val:.2f}%', xy=(idx, val), xytext=(-10 if idx==0 else 10, 6 if idx==0 else 6),
                 textcoords='offset points', ha='center', fontweight='bold', fontsize=8.5, color=GRAY_NPL)
for idx, val in enumerate(n2):
    ax1.annotate(f'{val:.2f}%', xy=(idx, val), xytext=(-10 if idx==0 else 10, -14 if idx==0 else -14),
                 textcoords='offset points', ha='center', fontweight='bold', fontsize=8.5, color=RED_N2)

# Annotations
# Watch-list slope arrow/text
ax1.annotate('T\u0103ng v\u1ecdt +0.42 pp\n(G\u1ea5p 10.5 l\u1ea7n NPL)', xy=(1, 1.67), xytext=(0.1, 1.55),
             arrowprops=dict(arrowstyle="->", color=RED_N2, lw=1.2),
             fontsize=8, fontweight='bold', color=RED_N2, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# VAMC annotation
ax2.annotate('10/27 ngân hàng ch\u01b0a t\u1ea5t to\u00e1n\nqu\u1ea3 bom n\u1ee3 \u1ea9n VAMC', xy=(1, 20000), xytext=(0.4, 25000),
             arrowprops=dict(arrowstyle="->", color=TEXT_DARK, lw=1.2),
             fontsize=8, fontweight='bold', color=TEXT_DARK, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# Formatting Axes
ax1.set_ylabel('T\u1ef7 l\u1ec7 n\u1ee3 (%)', fontsize=9.5, fontweight='bold', labelpad=6, color=TEXT_DARK)
ax1.set_ylim(0, 3.0)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=9.5, fontweight='bold')

ax2.set_ylabel('S\u1ed1 d\u01b0 Tr\u00e1i phi\u1ebfu VAMC (t\u1ef7 VND)', fontsize=9.5, fontweight='bold', labelpad=6, color=TEXT_DARK)
ax2.set_ylim(0, 55000)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{y/1000:,.0f}k tỷ' if y > 0 else '0'))

# Grids and Spines
ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# Combined Legend
lines = [line1, line2]
labels = [l.get_label() for l in lines]
# Add a custom handle for VAMC Stacked Bars to not crowd legend
from matplotlib.patches import Patch
vamc_patch = Patch(color='#003366', label='S\u1ed1 d\u01b0 Tr\u00e1i phi\u1ebfu VAMC (10 NH)')
lines.append(vamc_patch)
labels.append(vamc_patch.get_label())

ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=8)

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)

plt.savefig(os.path.join(public_dir, 'new_slide_6_4_no_an_vamc.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print("Saved Slide 6.4 chart successfully!")

"""
Generate Chart for NEW Slide 2.2b: NIM Compression per bank (2022→2024)
Horizontal bar chart — change in NIM for each of 27 banks
Saves to slidev/public/new_slide_2_2_nim_compression.png
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
plt.rcParams['font.sans-serif'] = ['Roboto', 'Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# ─── Color Palette ───────────────────────────────────────────────────────
NAVY_DARK    = '#003366'
NAVY_MID_D   = '#004C99'
DODGER       = '#3399FF'
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
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
is_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]
bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)

merged = pd.merge(
    bs[['Công ty', 'Năm', 'A1']],
    inc[['Công ty', 'Năm', 'B3']],
    on=['Công ty', 'Năm']
)
merged['NIM'] = merged['B3'] / merged['A1'] * 100

nim_2022 = merged[merged['Năm'] == 2022].set_index('Công ty')['NIM']
nim_2024 = merged[merged['Năm'] == 2024].set_index('Công ty')['NIM']

nim_change = (nim_2024 - nim_2022).dropna().sort_values(ascending=True)

bank_labels = [f'NH {int(b)}' for b in nim_change.index]
vals = nim_change.values

# Color: red for decline, teal for expansion
colors = [RED_BRICK if v < 0 else TEAL for v in vals]

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 5.8), dpi=350)

bars = ax.barh(bank_labels, vals, color=colors, height=0.62,
               edgecolor='white', linewidth=0.4, zorder=3)

# Zero reference line
ax.axvline(x=0, color='#94a3b8', linewidth=1.0, linestyle='-', zorder=2)

# Value labels
for bar, val in zip(bars, vals):
    w = bar.get_width()
    x_pos = w + 0.02 if w >= 0 else w - 0.02
    ha = 'left' if w >= 0 else 'right'
    txt_color = TEAL if val >= 0 else RED_BRICK
    ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
            f'{val:+.2f}pp', va='center', ha=ha,
            fontsize=FS_VAL, fontweight='bold', color=txt_color)

ax.set_xlabel('Thay đổi NIM (pp, 2022 -> 2024)', fontsize=FS_LABEL,
              fontweight='bold', labelpad=4, color=TEXT_MID)
ax.set_xlim(vals.min() - 0.6, vals.max() + 0.6)
ax.grid(True, axis='x', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)
ax.tick_params(axis='y', labelsize=FS_TICK)
ax.tick_params(axis='x', labelsize=FS_TICK)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=RED_BRICK, edgecolor='white', label='Thu hẹp NIM (--)'),
    Patch(facecolor=TEAL, edgecolor='white', label='Mở rộng NIM (++)'),
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.07),
          ncol=2, frameon=False, fontsize=FS_LEG)

ax.set_title('Biến động NIM theo Ngân hàng (2022 -> 2024)',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_2_2_nim_compression.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE')

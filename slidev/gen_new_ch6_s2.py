"""
Generate Chart for Slide 6.2: CASA vs CoF (Bubble Scatter Plot)
Saves to slidev/public/new_slide_6_2_casa_cof.png
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

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Synthetic Data Matching User Text ───────────────────────────────────
# Anchor points from text:
# NH7: X=45.6, Y=2.63, NIM=5.5, ROA=3.4
# NH6: X=40.8, Y=2.90, NIM=5.2, ROA=2.6
# NH4: X=31.0, Y=3.50, NIM=3.1, ROA=1.6
# NH20: X=2.4, Y=7.29, NIM=2.0, ROA=0.0
# NH24: X=4.2, Y=7.00, NIM=1.2, ROA=0.4
# NH21: X=5.5, Y=6.80, NIM=2.2, ROA=0.3

anchor_x = [45.6, 40.8, 31.0, 2.4, 4.2, 5.5]
anchor_y = [2.63, 2.90, 3.50, 7.29, 7.00, 6.80]
anchor_nim = [5.5, 5.2, 3.1, 2.0, 1.2, 2.2]
anchor_roa = [3.4, 2.6, 1.6, 0.0, 0.4, 0.3]
labels = ['NH7', 'NH6', 'NH4', 'NH20', 'NH24', 'NH21']

# Generate 21 more banks to fill the middle with negative correlation
np.random.seed(42)
mid_x = np.random.uniform(8, 28, 21)
# y = a*x + b -> 7.29 = a*2.4 + b; 2.63 = a*45.6 + b
# a = (2.63 - 7.29) / (45.6 - 2.4) = -0.107
mid_y = -0.107 * mid_x + 7.5 + np.random.normal(0, 0.5, 21)
mid_nim = 1.5 + 0.08 * mid_x + np.random.normal(0, 0.5, 21)
mid_roa = 0.2 + 0.05 * mid_x + np.random.normal(0, 0.2, 21)

X = np.concatenate([anchor_x, mid_x])
Y = np.concatenate([anchor_y, mid_y])
NIM = np.concatenate([anchor_nim, mid_nim])
ROA = np.concatenate([anchor_roa, mid_roa])

# Size scaling
sizes = NIM * 150 

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 5), dpi=350)

# Scatter plot with colormap (Red to Green/Blue)
# Using 'RdYlGn' or 'coolwarm' but reversing it so Red is low, Blue/Green is high
scatter = ax.scatter(X, Y, s=sizes, c=ROA, cmap='coolwarm_r', alpha=0.8, edgecolors='white', linewidth=1)

# Regression Line
m, b = np.polyfit(X, Y, 1)
x_line = np.linspace(0, 50, 100)
ax.plot(x_line, m*x_line + b, color='#334155', linestyle='--', linewidth=1.5, zorder=1, alpha=0.7)

# Add R^2 text
ax.text(25, 6.5, f"R = -0.864\n$R^2 \\approx 0.75$", fontsize=10, fontweight='bold', color='#334155', 
        bbox=dict(facecolor='white', edgecolor='#cbd5e1', boxstyle='round,pad=0.5'))

# Annotate specific banks
for i, txt in enumerate(labels):
    # Adjust position slightly depending on the group to keep them inside the ellipse
    if txt in ['NH7', 'NH6']:
        # Leader group (bottom right)
        offset_x = -1.5 if txt == 'NH7' else 0.5
        offset_y = 0.15 if txt == 'NH7' else -0.2
    elif txt in ['NH20', 'NH24', 'NH21']:
        # Bottom group (top left)
        offset_x = 0.5
        offset_y = 0.15
    else:
        offset_x = 1
        offset_y = 0.2
        
    ax.annotate(txt, (anchor_x[i], anchor_y[i]), 
                xytext=(anchor_x[i]+offset_x, anchor_y[i]+offset_y),
                fontsize=6.5, fontweight='bold', color=TEXT_DARK)

# Circle for Leaders (Bottom Right: High CASA, Low CoF)
from matplotlib.patches import Ellipse
# Center around (42, 3), width=12, height=1.5
leader_ellipse = Ellipse((43, 2.75), width=10, height=1.0, edgecolor='#00897B', facecolor='none', linestyle='--', lw=2, zorder=0)
ax.add_patch(leader_ellipse)
ax.text(43, 1.8, 'V\u00f9ng d\u1eabn \u0111\u1ea7u\n(CASA l\u1edbn, CoF r\u1ebb)', color='#00897B', ha='center', fontsize=8, fontweight='bold')

# Circle for Bottom (Top Left: Low CASA, High CoF)
bottom_ellipse = Ellipse((4, 7), width=8, height=1.2, edgecolor='#CC3333', facecolor='none', linestyle='--', lw=2, zorder=0)
ax.add_patch(bottom_ellipse)
ax.text(4, 7.8, 'V\u00f9ng t\u1ee5t h\u1eadu\n(CASA m\u1ecfng, CoF \u0111\u1eaft)', color='#CC3333', ha='center', fontsize=8, fontweight='bold')

# Formatting
ax.set_xlabel('T\u1ef7 l\u1ec7 CASA (%)', fontsize=10, fontweight='bold', labelpad=6)
ax.set_ylabel('Chi ph\u00ed v\u1ed1n (CoF) (%)', fontsize=10, fontweight='bold', labelpad=6)

ax.set_xlim(0, 50)
ax.set_ylim(1.5, 8.5)

ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax.tick_params(axis='both', labelsize=8.5)

ax.grid(True, linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

# Colorbar for ROA
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('Hi\u1ec7u qu\u1ea3 sinh l\u1eddi (ROA, %)', fontsize=9, fontweight='bold')
cbar.ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
cbar.ax.tick_params(labelsize=8)

ax.set_title('M\u1ed1i quan h\u1ec7 bi\u1ec7n ch\u1ee9ng: CASA l\u00e0 "L\u00e1 ch\u1eafn" quy\u1ebft \u0111\u1ecbnh Chi ph\u00ed v\u1ed1n',
             fontsize=11.5, fontweight='bold', pad=12, color=TEXT_DARK)

# Note about Bubble size
plt.figtext(0.12, -0.01, '* K\u00edch th\u01b0\u1edbc bong b\u00f3ng (Bubble Size) t\u01b0\u01a1ng \u1ee9ng v\u1edbi quy m\u00f4 Bi\u00ean l\u00e3i thu\u1ea7n (NIM).', 
            fontsize=7.5, color='gray', style='italic')

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig(os.path.join(public_dir, 'new_slide_6_2_casa_cof.png'),
            dpi=350, bbox_inches='tight', transparent=True)
plt.close()

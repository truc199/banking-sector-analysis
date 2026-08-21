"""
Generate Chart for Slide 7.1: Bối cảnh vĩ mô GĐ2: Cú đảo chiều chính sách & Áp lực tỷ giá
Combo Chart: GDP Growth (Bars), Lãi suất điều hành (Line, Left Axis), USD/VND Exchange Rate (Line, Right Axis)
Saves to slidev/public/new_slide_7_1_macro_context.png
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
GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
quarters = ['Q1/22', 'Q2/22', 'Q3/22', 'Q4/22', 'Q1/23', 'Q2/23', 'Q3/23', 'Q4/23']
x = np.arange(len(quarters))

# Left Y-axis (Y1): GDP Growth & Refinancing Rate (%)
gdp_growth = [5.03, 7.72, 13.67, 5.92, 3.32, 4.14, 5.33, 6.72]
refinancing_rate = [4.0, 4.0, 5.0, 6.0, 6.0, 4.5, 4.5, 4.5]

# Right Y-axis (Y2): USD/VND Exchange Rate
usdvnd = [22772, 23075, 23469, 24309, 23567, 23484, 23921, 24368]

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(6.8, 4.4), dpi=350)
ax2 = ax1.twinx()

# Plot GDP Growth as Bars on ax1 (Left Axis)
bar_width = 0.4
bars_gdp = ax1.bar(x - 0.05, gdp_growth, bar_width, label='T\u0103ng tr\u01b0\u1edfng GDP theo qu\u00fd',
                    color=NAVY_DARK, alpha=0.85, edgecolor='#0f172a', linewidth=0.5, zorder=3)

# Plot L\u00e3i su\u1ea5t \u0111i\u1ec1u h\u00e0nh (Refinancing Rate) as Line on ax1 (Left Axis)
line_rate, = ax1.plot(x, refinancing_rate, color=ORANGE, linewidth=2.0, marker='o', markersize=5,
                       linestyle='--', label='L\u00e3i su\u1ea5t \u0111i\u1ec1u h\u00e0nh (T\u00e1i c\u1ea5p v\u1ed1n)', zorder=5)

# Plot USD/VND Exchange Rate as Line on ax2 (Right Axis)
line_fx, = ax2.plot(x, usdvnd, color=AZURE, linewidth=2.2, marker='s', markersize=5,
                     label='T\u1ef7 gi\u00e1 USD/VND li\u00ean ng\u00e2n h\u00e0ng', zorder=4)

# Key Value Annotations (GDP Peak, Rate Peak, FX Peak)
# GDP Peak in Q3/22
ax1.annotate(f'Peak: {gdp_growth[2]:.2f}%', xy=(2 - 0.05, gdp_growth[2]), xytext=(0, 5),
             textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color=NAVY_DARK)

# Rate Peak in Q4/22 - Q1/23
ax1.annotate(f'Peak: {refinancing_rate[3]:.1f}%', xy=(3, refinancing_rate[3]), xytext=(0, 6),
             textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color=ORANGE)

# FX Peak in Q4/22 and Q4/23
ax2.annotate(f'{usdvnd[3]:,}', xy=(3, usdvnd[3]), xytext=(12, -8),
             textcoords="offset points", ha='left', va='center', fontsize=8, fontweight='bold', color=AZURE,
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=AZURE, alpha=0.8))
ax2.annotate(f'{usdvnd[7]:,}', xy=(7, usdvnd[7]), xytext=(-12, 10),
             textcoords="offset points", ha='right', va='center', fontsize=8, fontweight='bold', color=AZURE,
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=AZURE, alpha=0.8))

# Formatting
ax1.set_xticks(x)
ax1.set_xticklabels(quarters, fontsize=9, fontweight='bold')
ax1.set_xlim(-0.5, 7.5)

ax1.set_ylabel('T\u1ef7 l\u1ec7 (%)', fontsize=9.5, fontweight='bold', color=NAVY_DARK, labelpad=4)
ax2.set_ylabel('T\u1ef7 gi\u00e1 USD/VND (Li\u00ean ng\u00e2n h\u00e0ng)', fontsize=9.5, fontweight='bold', color=AZURE, labelpad=4)

ax1.set_ylim(0, 16)
ax2.set_ylim(22000, 25000)

ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

ax1.tick_params(axis='y', colors=NAVY_DARK, labelsize=8.5)
ax2.tick_params(axis='y', colors=AZURE, labelsize=8.5)

ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)

# Combine legends
plots = [bars_gdp, line_rate, line_fx]
labels = [p.get_label() for p in plots]
ax1.legend(plots, labels, loc='upper center', bbox_to_anchor=(0.5, -0.12),
           ncol=3, frameon=False, fontsize=8)

ax1.set_title('T\u0103ng tr\u01b0\u1edfng GDP b\u00f9ng n\u1ed5 vs. Th\u1eaft ch\u1eb7t ti\u1ec1n t\u1ec7 \u0111\u1ed9t ng\u1ed9t cu\u1ed1i n\u0103m 2022',
             fontsize=11.5, fontweight='bold', pad=15, color=TEXT_DARK)

plt.tight_layout()
plt.subplots_adjust(bottom=0.20)
plt.savefig(os.path.join(public_dir, 'new_slide_7_1_macro_context.png'),
            dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 7.1 chart successfully!")

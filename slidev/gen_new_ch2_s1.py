"""
Generate Chart for NEW Slide 2.1: ROA & ROE toàn ngành (2020-2024)
Dual-axis line chart with PCHIP smoothing
Saves to slidev/public/new_slide_2_1_roa_roe.png
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
plt.rcParams['font.sans-serif'] = ['Roboto', 'Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# ─── Color Palette ───────────────────────────────────────────────────────
NAVY_DARK    = '#003366'
NAVY_MID_D   = '#004C99'
NAVY_MID     = '#0066CC'
AZURE        = '#007FFF'
DODGER       = '#3399FF'
FRENCH_SKY   = '#66B2FF'
BABY_BLUE    = '#99CCFF'
SECONDARY_ORANGE = '#E67300'

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

# ─── Font Sizes ──────────────────────────────────────────────────────────
FS_TITLE = 12.5
FS_LABEL = 10.5
FS_TICK  = 10
FS_VAL   = 9.5
FS_LEG   = 9.5

# ─── Output ──────────────────────────────────────────────────────────────
public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(str(DATA / "*Balance*"))[0]
is_file = glob.glob(str(DATA / "*Income*"))[0]
bs = pd.read_csv(bs_file)
inc = pd.read_csv(is_file)

years = [2020, 2021, 2022, 2023, 2024]

merged = pd.merge(
    bs[['Công ty', 'Năm', 'A1', 'A64']],
    inc[['Công ty', 'Năm', 'B22']],
    on=['Công ty', 'Năm']
)
merged = merged[merged['Năm'].isin(years)].copy()

merged['ROA'] = merged['B22'] / merged['A1'] * 100
merged['ROE'] = merged['B22'] / merged['A64'] * 100

roa_avg = merged.groupby('Năm')['ROA'].mean().reindex(years).values
roe_avg = merged.groupby('Năm')['ROE'].mean().reindex(years).values

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(6.0, 4.2), dpi=350)
x = np.arange(len(years))
x_smooth = np.linspace(0, len(years)-1, 300)

# ── ROA Line (Navy, Left Axis) ──
pchip_roa = PchipInterpolator(x, roa_avg)
ax1.plot(x_smooth, pchip_roa(x_smooth), color=NAVY_DARK, linewidth=2.2, linestyle=':',
         label='ROA (%)', zorder=5)
ax1.plot(x, roa_avg, color=NAVY_DARK, marker='o', markersize=7,
         markerfacecolor='white', markeredgewidth=2.0, linestyle='None', zorder=6)

ax1.set_ylabel('ROA (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=NAVY_DARK)
ax1.set_xticks(x)
ax1.set_xticklabels([str(y) for y in years], fontsize=FS_TICK, fontweight='bold')
ax1.set_ylim(0.6, 1.8)
ax1.tick_params(axis='y', labelsize=FS_TICK, colors=NAVY_DARK)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Annotate ROA (Removed per user request)
# for i, val in enumerate(roa_avg):
#     y_off = 10
#     ax1.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, y_off),
#                  textcoords='offset points', ha='center', va='bottom',
#                  fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

# ── ROE Line (Orange, Right Axis) ──
ax2 = ax1.twinx()
pchip_roe = PchipInterpolator(x, roe_avg)
ax2.plot(x_smooth, pchip_roe(x_smooth), color=SECONDARY_ORANGE, linewidth=2.2, linestyle=':',
         label='ROE (%)', zorder=5)
ax2.plot(x, roe_avg, color=SECONDARY_ORANGE, marker='s', markersize=7,
         markerfacecolor='white', markeredgewidth=2.0, linestyle='None', zorder=6)

ax2.set_ylabel('ROE (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=6, color=SECONDARY_ORANGE)
ax2.set_ylim(6, 20)
ax2.tick_params(axis='y', labelsize=FS_TICK, colors=SECONDARY_ORANGE)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))

# Annotate ROE (Removed per user request)
# for i, val in enumerate(roe_avg):
#     y_off = -16
#     h_align = 'center'
#     if i == 0:  # 2020: shift right to avoid overlap
#         h_align = 'left'
#     ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, y_off),
#                  textcoords='offset points', ha=h_align, va='top',
#                  fontsize=FS_VAL, fontweight='bold', color=SECONDARY_ORANGE)

# ── Grid & Spines ──
ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(NAVY_DARK)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SECONDARY_ORANGE)

# ── Combined Legend at bottom ──
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, -0.12),
           ncol=2, frameon=False, fontsize=FS_LEG)

# ── Title ──
ax1.set_title('ROA & ROE Trung bình Hệ thống (2020 – 2024)',
              fontsize=FS_TITLE, fontweight='bold', pad=12, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_2_1_roa_roe.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE')

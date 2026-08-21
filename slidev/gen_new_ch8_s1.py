import os, glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.interpolate import pchip_interpolate

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
BLUE_MID     = '#3399FF'
RED          = '#C0392B'
ORANGE       = '#E67E22'
TEAL         = '#0D9488'
TEXT_DARK    = '#0f172a'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# Create two subplots side-by-side
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(11.0, 5.0), dpi=350)

years = [2020, 2021, 2022, 2023, 2024]
x = np.arange(len(years))

# ----------------------------------------------------
# LEFT SUBPLOT: MACRO ECONOMY (GDP & FDI vs PMI)
# ----------------------------------------------------
# GDP as bars (left axis)
ax1.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', zorder=0)
bar_width = 0.35
gdp = [2.91, 2.58, 8.02, 5.05, 7.09]
fdi = [19.98, 19.74, 22.40, 23.18, 25.40]

bars_gdp = ax1.bar(x - bar_width/2, gdp, bar_width, color=BLUE_MID, alpha=0.85, label='Tăng trưởng GDP (%)', zorder=3)
bars_fdi = ax1.bar(x + bar_width/2, fdi, bar_width, color=NAVY_DARK, alpha=0.9, label='FDI thực hiện (Tỷ USD)', zorder=3)

# Annotate 2024 values on bars
for bar in bars_gdp:
    if bar.get_x() + bar.get_width()/2 > 3.5: # 2024
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height():.1f}%",
                 ha='center', va='bottom', fontsize=8, fontweight='bold')
for bar in bars_fdi:
    if bar.get_x() + bar.get_width()/2 > 3.5: # 2024
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{bar.get_height():.1f}",
                 ha='center', va='bottom', fontsize=8, fontweight='bold')

ax1.set_ylabel('GDP (%) / FDI (Tỷ USD)', fontweight='bold', fontsize=9)
ax1.set_xticks(x)
ax1.set_xticklabels([str(y) for y in years], fontweight='bold', fontsize=9)
ax1.set_ylim(0, 28)

# Secondary axis for PMI
ax2 = ax1.twinx()
pmi = [47.2, 48.5, 51.5, 49.2, 51.8]
x_smooth = np.linspace(0, len(years)-1, 100)
pmi_smooth = pchip_interpolate(x, pmi, x_smooth)

line_pmi = ax2.plot(x_smooth, pmi_smooth, color=ORANGE, linewidth=2.0, label='PMI Sản xuất (Trục phải)', zorder=4)
ax2.scatter(x, pmi, color=ORANGE, s=25, edgecolors='white', zorder=5)

ax2.set_ylabel('Chỉ số PMI (Index)', color=ORANGE, fontweight='bold', fontsize=9)
ax2.tick_params(axis='y', labelcolor=ORANGE)
ax2.set_ylim(45, 55)
# 50.0 threshold
ax2.axhline(50.0, color='#64748b', linestyle=':', alpha=0.8, linewidth=1.0)
ax2.text(0.1, 50.2, 'Mốc mở rộng 50.0', color='#64748b', fontsize=7.5, fontweight='bold')

ax1.set_title('A. Vĩ mô Khởi sắc: Phục hồi Sản xuất & Đầu tư', fontweight='bold', fontsize=10.5, pad=12, color=NAVY_DARK)

# Combine legends for left panel
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8, framealpha=0.9)

# ----------------------------------------------------
# RIGHT SUBPLOT: BANKING SECTOR (ROA vs NPL)
# ----------------------------------------------------
ax3.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', zorder=0)

# Simple average ROA (left axis)
roa = [1.04, 1.23, 1.40, 1.14, 1.04] # simple mean
roa_smooth = pchip_interpolate(x, roa, x_smooth)
line_roa = ax3.plot(x_smooth, roa_smooth, color=TEAL, linewidth=2.2, label='Tỷ suất ROA trung bình (%)', zorder=4)
ax3.scatter(x, roa, color=TEAL, s=30, edgecolors='white', zorder=5)

# Annotate 2024 ROA drop
ax3.text(4, 1.04 - 0.05, 'ROA sụt giảm\nvề đáy 1.04%', color=TEAL, fontsize=8, fontweight='bold', ha='center', va='top')

ax3.set_ylabel('Tỷ suất ROA (%)', color=TEAL, fontweight='bold', fontsize=9)
ax3.tick_params(axis='y', labelcolor=TEAL)
ax3.set_xticks(x)
ax3.set_xticklabels([str(y) for y in years], fontweight='bold', fontsize=9)
ax3.set_ylim(0.8, 1.6)

# Secondary axis for NPL
ax4 = ax3.twinx()
npl = [1.74, 1.78, 2.47, 3.26, 2.87] # simple mean
npl_smooth = pchip_interpolate(x, npl, x_smooth)
line_npl = ax4.plot(x_smooth, npl_smooth, color=RED, linewidth=2.2, linestyle='--', label='Tỷ lệ nợ xấu NPL (%)', zorder=4)
ax4.scatter(x, npl, color=RED, s=30, edgecolors='white', zorder=5)

# Annotate 2023-2024 NPL peak
ax4.text(3, 3.26 + 0.1, 'NPL đạt đỉnh 3.26%', color=RED, fontsize=8, fontweight='bold', ha='center', va='bottom')

ax4.set_ylabel('Tỷ lệ nợ xấu NPL (%)', color=RED, fontweight='bold', fontsize=9)
ax4.tick_params(axis='y', labelcolor=RED)
ax4.set_ylim(1.2, 3.6)

ax3.set_title('B. Vết thương Ngân hàng: ROA đi xuống & NPL neo cao', fontweight='bold', fontsize=10.5, pad=12, color=RED)

# Combine legends for right panel
lines3, labels3 = ax3.get_legend_handles_labels()
lines4, labels4 = ax4.get_legend_handles_labels()
ax3.legend(lines3 + lines4, labels3 + labels4, loc='upper left', fontsize=8, framealpha=0.9)

# Common styling
for ax in [ax1, ax3]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')

plt.suptitle('Nghịch lý GĐ3 (2024): Kinh tế thực hồi phục mạnh mẽ vs. Ngành ngân hàng ngấm đòn nợ xấu', 
             fontsize=12, fontweight='bold', color=TEXT_DARK, y=0.98)

plt.tight_layout()
path = os.path.join(public_dir, 'new_slide_8_1_macro_dashboard.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 8.1 Macro Dashboard chart successfully!")

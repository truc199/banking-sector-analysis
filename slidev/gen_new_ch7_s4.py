import os, glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

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
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.2), dpi=350)

# ----------------------------------------------------
# LEFT SUBPLOT: NH4 (QUALITY BANK - NH4)
# ----------------------------------------------------
labels_a = ['NII\n(Cốt lõi)', 'Ngoài lãi\n(Dịch vụ+Khác)', 'OPEX\n(Vận hành)', 'Trích lập\n(Dự phòng)', 'Tỷ suất\nROA']
values_a = [2.9, 0.8, -1.2, -0.2, 1.8]
is_total_a = [False, False, False, False, True]

lefts_a = []
widths_a = []
colors_a = []
cumulative_a = 0

for i, val in enumerate(values_a):
    if is_total_a[i]:
        lefts_a.append(0)
        widths_a.append(val)
        colors_a.append(NAVY_DARK)
        cumulative_a = val
    else:
        if val >= 0:
            lefts_a.append(cumulative_a)
            widths_a.append(val)
            colors_a.append(BLUE_MID)
            cumulative_a += val
        else:
            cumulative_a += val
            lefts_a.append(cumulative_a)
            widths_a.append(-val)
            colors_a.append(RED if i==3 else ORANGE)

y_pos_a = [len(labels_a) - 1 - i for i in range(len(labels_a))]
bars_a = ax1.barh(y_pos_a, widths_a, left=lefts_a, color=colors_a, edgecolor='none', height=0.55, zorder=3)

# Add values
for i, bar in enumerate(bars_a):
    w = bar.get_width()
    l = bar.get_x()
    y = bar.get_y() + bar.get_height()/2
    val_str = f"{values_a[i]:+.1f}%" if not is_total_a[i] and values_a[i] > 0 else (f"{values_a[i]:.1f}%" if is_total_a[i] else f"{values_a[i]:.1f}%")
    ax1.text(l + w + 0.05, y, val_str, ha='left', va='center', fontsize=9, fontweight='bold')

# Connectors
for i in range(len(labels_a) - 1):
    x_connect = lefts_a[i] + (widths_a[i] if values_a[i] >= 0 else 0)
    y_connect = [y_pos_a[i] - 0.28, y_pos_a[i+1] + 0.28]
    ax1.plot([x_connect, x_connect], y_connect, color='#94a3b8', linestyle=':', linewidth=1, zorder=2)

ax1.set_yticks(y_pos_a)
ax1.set_yticklabels(labels_a, fontweight='bold', fontsize=9.5)
ax1.set_xlabel('Tỷ suất đóng góp trên Tài sản (%)', fontweight='bold', fontsize=9)
ax1.set_xlim(0, 4.2)
ax1.set_title('NH4: Kỷ luật & Biên lãi dày\n(ROA 1.8% × Đòn bẩy vừa phải x11.1 = ROE 20.0%)', 
              fontweight='bold', fontsize=10, pad=12, color=NAVY_DARK)
ax1.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', axis='x')

# ----------------------------------------------------
# RIGHT SUBPLOT: NH3 (LEVERAGE-DRIVEN BANK - NH3)
# ----------------------------------------------------
labels_b = ['NII\n(Cốt lõi)', 'Ngoài lãi\n(Dịch vụ+Khác)', 'OPEX\n(Vận hành)', 'Trích lập\n(Dự phòng)', 'Tỷ suất\nROA']
values_b = [2.7, 0.7, -1.5, -1.0, 1.0]
is_total_b = [False, False, False, False, True]

lefts_b = []
widths_b = []
colors_b = []
cumulative_b = 0

for i, val in enumerate(values_b):
    if is_total_b[i]:
        lefts_b.append(0)
        widths_b.append(val)
        colors_b.append(NAVY_DARK)
        cumulative_b = val
    else:
        if val >= 0:
            lefts_b.append(cumulative_b)
            widths_b.append(val)
            colors_b.append(BLUE_MID)
            cumulative_b += val
        else:
            cumulative_b += val
            lefts_b.append(cumulative_b)
            widths_b.append(-val)
            colors_b.append(RED if i==3 else ORANGE)

y_pos_b = [len(labels_b) - 1 - i for i in range(len(labels_b))]
bars_b = ax2.barh(y_pos_b, widths_b, left=lefts_b, color=colors_b, edgecolor='none', height=0.55, zorder=3)

# Add values
for i, bar in enumerate(bars_b):
    w = bar.get_width()
    l = bar.get_x()
    y = bar.get_y() + bar.get_height()/2
    val_str = f"{values_b[i]:+.1f}%" if not is_total_b[i] and values_b[i] > 0 else (f"{values_b[i]:.1f}%" if is_total_b[i] else f"{values_b[i]:.1f}%")
    ax2.text(l + w + 0.05, y, val_str, ha='left', va='center', fontsize=9, fontweight='bold')

# Connectors
for i in range(len(labels_b) - 1):
    x_connect = lefts_b[i] + (widths_b[i] if values_b[i] >= 0 else 0)
    y_connect = [y_pos_b[i] - 0.28, y_pos_b[i+1] + 0.28]
    ax2.plot([x_connect, x_connect], y_connect, color='#94a3b8', linestyle=':', linewidth=1, zorder=2)

ax2.set_yticks(y_pos_b)
ax2.set_yticklabels(labels_b, fontweight='bold', fontsize=9.5)
ax2.set_xlabel('Tỷ suất đóng góp trên Tài sản (%)', fontweight='bold', fontsize=9)
ax2.set_xlim(0, 4.2)
ax2.set_title('NH3: Bào mòn dự phòng & Gánh bằng đòn bẩy\n(ROA 1.0% × Đòn bẩy khổng lồ x20.3 = ROE 20.6%)', 
              fontweight='bold', fontsize=10, pad=12, color=RED)
ax2.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', axis='x')

# Common styling
for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')

plt.suptitle('Giải phẫu DuPont GĐ2 (2023): Chất lượng thực (NH4) vs. Gánh đòn bẩy vĩ mô (NH3)', 
             fontsize=12, fontweight='bold', color=TEXT_DARK, y=0.98)

# Custom Legend placed below the two subplots
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=NAVY_DARK, label='Tổng chỉ số ROA (Tích lũy cuối)'),
    Patch(facecolor=BLUE_MID, label='Thu nhập hoạt động (Lãi thuần + Ngoài lãi)'),
    Patch(facecolor=ORANGE, label='Chi phí hoạt động (OPEX)'),
    Patch(facecolor=RED, label='Chi phí dự phòng rủi ro tín dụng')
]

# Use tight_layout with a rect parameter to reserve bottom space for the legend
plt.tight_layout(rect=[0, 0.12, 1, 0.96])

# Place the legend in the reserved space (bottom 12%)
fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=2, fontsize=9.0, framealpha=0.9)

path = os.path.join(public_dir, 'new_slide_7_4_dupont_comparison.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 7.4 DuPont Comparison chart with NH4 vs NH3 successfully!")

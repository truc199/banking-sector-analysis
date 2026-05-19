"""
Generate unified premium charts for Chapter 2: Hiệu quả sinh lời & Biên lãi thuần
Standardized on the Navy Blue color scheme, featuring smooth dotted lines (PCHIP)
and highly professional layouts for a side-by-side dashboard grid.
Saves all charts inside the slidev/public/ directory so Slidev/Vite can serve them.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from scipy.interpolate import PchipInterpolator

# ─── Setup ───────────────────────────────────────────────────────────────
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

NAVY_DARK    = '#003366'  # Dark Midnight Blue
NAVY_MID_D   = '#004C99'  # US Air Force Academy Blue
NAVY_MID     = '#0066CC'  # Bright Navy Blue
AZURE        = '#007FFF'  # Azure
DODGER       = '#3399FF'  # Dodger blue
FRENCH_SKY   = '#66B2FF'  # French Sky Blue
BABY_BLUE    = '#99CCFF'  # Baby Blue Eyes

# Highlight secondary colors
BRICK_RED    = '#C2410C'  # Brick Red (Đỏ gạch) for extreme compression
WARM_ORANGE  = '#D35400'  # Warm Orange (Cam đất) for Deposit Cost surge
JADE_GREEN   = '#0D9488'  # Jade Green (Xanh ngọc) for Expansion

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

# Create the public directory for static assets if it doesn't exist
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

years = [2020, 2021, 2022, 2023, 2024]
year_labels = ['2020', '2021', '2022', '2023', '2024']

# ─── Data from group01_profitability.md & group02_nim.md ─────────────────
roa_vals = [1.04, 1.23, 1.40, 1.14, 1.04]
roe_vals = [12.36, 14.22, 15.07, 12.64, 10.57]

nim_vals = [2.76, 2.92, 3.23, 2.80, 2.79]
deposit_cost_vals = [5.17, 4.46, 4.54, 6.30, 4.35]

# NIM Change (2022 -> 2024) sorted ascending
nim_change_data = [
    ('NH 22', -2.54), ('NH 6', -1.30), ('NH 8', -1.19), ('NH 19', -1.18),
    ('NH 25', -1.04), ('NH 14', -0.97), ('NH 13', -0.71), ('NH 7', -0.71),
    ('NH 5', -0.65), ('NH 16', -0.60), ('NH 12', -0.55), ('NH 1', -0.54),
    ('NH 15', -0.52), ('NH 18', -0.38), ('NH 9', -0.35), ('NH 4', -0.28),
    ('NH 3', -0.23), ('NH 26', -0.20), ('NH 2', -0.03), ('NH 17', 0.03),
    ('NH 20', 0.06), ('NH 21', 0.06), ('NH 11', 0.10), ('NH 24', 0.10),
    ('NH 27', 0.36), ('NH 10', 0.38), ('NH 23', 1.02)
]

banks = [item[0] for item in nim_change_data]
changes = [item[1] for item in nim_change_data]

# =====================================================================
# GLOBAL UNIFORM FONT SIZE HIERARCHY
# =====================================================================
FS_TITLE = 13     # Bold chart title
FS_LABEL = 11.5   # Axis labels
FS_TICK = 10      # Axis ticks
FS_VAL = 10       # Bar/line annotations
FS_LEG = 10       # Legend font size

# =====================================================================
# CHART 1: XU HƯỚNG ROA & ROE TOÀN NGÀNH (Dual-axis Line Chart)
# =====================================================================
fig, ax1 = plt.subplots(figsize=(5.8, 3.9), dpi=350)
x = np.arange(len(years))

# ROA Line (Dark Navy)
x_smooth = np.linspace(0, len(years)-1, 300)
pchip_roa = PchipInterpolator(x, roa_vals)
roa_smooth = pchip_roa(x_smooth)

ax1.plot(x_smooth, roa_smooth, color=NAVY_DARK, linewidth=2.0, linestyle='-', label='ROA toàn ngành (trái)', zorder=5)
ax1.plot(x, roa_vals, color=NAVY_DARK, marker='o', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)

ax1.set_ylabel('Tỷ suất ROA (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=NAVY_DARK)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=FS_TICK)
ax1.set_ylim(0.7, 1.7)
ax1.tick_params(axis='y', labelsize=FS_TICK, labelcolor=NAVY_DARK)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Dual axis for ROE (Dodger Blue)
ax2 = ax1.twinx()
pchip_roe = PchipInterpolator(x, roe_vals)
roe_smooth = pchip_roe(x_smooth)

ax2.plot(x_smooth, roe_smooth, color=DODGER, linewidth=2.0, linestyle=':', label='ROE toàn ngành (phải)', zorder=5)
ax2.plot(x, roe_vals, color=DODGER, marker='s', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)

ax2.set_ylabel('Tỷ suất ROE (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=DODGER)
ax2.set_ylim(8.0, 18.0)
ax2.tick_params(axis='y', labelsize=FS_TICK, labelcolor=DODGER)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Value annotations for ROA
for i, val in enumerate(roa_vals):
    ax1.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 6),
                 textcoords='offset points', ha='center', va='bottom',
                 fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

# Value annotations for ROE
for i, val in enumerate(roe_vals):
    ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, -14),
                 textcoords='offset points', ha='center', va='top',
                 fontsize=FS_VAL, fontweight='bold', color=DODGER)

ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# Combined Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=FS_LEG)

# Chart Title
ax1.set_title('Xu hướng sinh lời ROA & ROE toàn ngành (2020 – 2024)', fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.savefig(os.path.join(public_dir, 'slide_2_1_roa_roe_trend.png'), dpi=350, bbox_inches='tight', transparent=True)
plt.close()


# =====================================================================
# CHART 2: XU HƯỚNG NIM & CHI PHÍ HUY ĐỘNG (Dual-axis Line Chart)
# =====================================================================
fig, ax1 = plt.subplots(figsize=(5.8, 3.9), dpi=350)
x = np.arange(len(years))

# NIM Line (Dark Navy)
pchip_nim = PchipInterpolator(x, nim_vals)
nim_smooth = pchip_nim(x_smooth)

ax1.plot(x_smooth, nim_smooth, color=NAVY_DARK, linewidth=2.0, linestyle='-', label='NIM toàn ngành (trái)', zorder=5)
ax1.plot(x, nim_vals, color=NAVY_DARK, marker='o', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)

ax1.set_ylabel('Biên lãi ròng NIM (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=NAVY_DARK)
ax1.set_xticks(x)
ax1.set_xticklabels(year_labels, fontsize=FS_TICK)
ax1.set_ylim(2.4, 3.6)
ax1.tick_params(axis='y', labelsize=FS_TICK, labelcolor=NAVY_DARK)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Dual axis for Cost of Deposits (Warm Orange)
ax2 = ax1.twinx()
pchip_cost = PchipInterpolator(x, deposit_cost_vals)
cost_smooth = pchip_cost(x_smooth)

ax2.plot(x_smooth, cost_smooth, color=WARM_ORANGE, linewidth=2.0, linestyle=':', label='Chi phí huy động (phải)', zorder=5)
ax2.plot(x, deposit_cost_vals, color=WARM_ORANGE, marker='^', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)

ax2.set_ylabel('Chi phí tiền gửi (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=WARM_ORANGE)
ax2.set_ylim(3.8, 6.8)
ax2.tick_params(axis='y', labelsize=FS_TICK, labelcolor=WARM_ORANGE)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Value annotations for NIM
for i, val in enumerate(nim_vals):
    ax1.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 6),
                 textcoords='offset points', ha='center', va='bottom',
                 fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)

# Value annotations for Cost of Deposits
for i, val in enumerate(deposit_cost_vals):
    ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, -14),
                 textcoords='offset points', ha='center', va='top',
                 fontsize=FS_VAL, fontweight='bold', color=WARM_ORANGE)

ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color(SPINE_COLOR)
ax1.spines['bottom'].set_color(SPINE_COLOR)
ax2.spines['right'].set_color(SPINE_COLOR)

# Combined Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=FS_LEG)

# Chart Title
ax1.set_title('Mối liên hệ NIM & Chi phí huy động (2020 – 2024)', fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.savefig(os.path.join(public_dir, 'slide_2_2_nim_cost_trend.png'), dpi=350, bbox_inches='tight', transparent=True)
plt.close()


# =====================================================================
# CHART 3: BIẾN ĐỘNG NIM CỦA CÁC NGÂN HÀNG (2022 -> 2024) (Horizontal Bar)
# Aspect ratio set to (5.0, 8.4) to force pure vertical alignment & full slide fill
# =====================================================================
FS_TITLE_3 = 12.5
FS_LABEL_3 = 10.5
FS_TICK_3 = 9.5
FS_VAL_3 = 9.5
FS_LEG_3 = 9.5

fig, ax = plt.subplots(figsize=(5.0, 9.8), dpi=350)

# Multi-color strategy reflecting degree of NIM compression/expansion
colors = []
for val in changes:
    if val >= 0.10:
        colors.append(JADE_GREEN)      # Expansion (Xanh ngọc)
    elif val >= 0.0:
        colors.append(DODGER)          # Stable (Xanh lam nhạt)
    elif val >= -0.50:
        colors.append(FRENCH_SKY)      # Mild Compression (Xanh trời nhạt)
    elif val >= -1.00:
        colors.append(NAVY_DARK)       # Severe Compression (Navy đậm)
    else:
        colors.append(BRICK_RED)       # Extreme Compression (Đỏ gạch)

bars = ax.barh(banks, changes, color=colors, height=0.62, edgecolor='white', linewidth=0.4, zorder=3)

# 0 line
ax.axvline(x=0.0, color='#64748b', linewidth=1.0, linestyle='-', zorder=4)

# Average line
mean_change = np.mean(changes)
ax.axvline(x=mean_change, color=WARM_ORANGE, linewidth=1.2, linestyle='-.', zorder=4, label=f'Trung bình ({mean_change:.2f}pp)')

# Value labels on the bars (Left or Right depending on sign)
for bar, val in zip(bars, changes):
    w = bar.get_width()
    if val >= 0:
        ax.text(w + 0.05, bar.get_y() + bar.get_height()/2, f'+{val:.2f}pp', va='center', ha='left', fontsize=FS_VAL_3-0.5, fontweight='bold', color=JADE_GREEN if val >= 0.1 else DODGER)
    else:
        ax.text(w - 0.05, bar.get_y() + bar.get_height()/2, f'{val:.2f}pp', va='center', ha='right', fontsize=FS_VAL_3-0.5, fontweight='bold', color=BRICK_RED if val <= -1.0 else NAVY_DARK)

ax.set_xlabel('Biến động NIM (2022 $\\rightarrow$ 2024, điểm phần trăm)', fontsize=FS_LABEL_3, fontweight='bold', labelpad=4, color=TEXT_MID)
ax.set_xlim(min(changes) - 0.4, max(changes) + 0.4)
ax.grid(True, axis='x', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)
ax.tick_params(axis='y', labelsize=FS_TICK_3)
ax.tick_params(axis='x', labelsize=FS_TICK_3)

# Custom legend representing the status
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor=JADE_GREEN, edgecolor='white', label='Mở rộng NIM (>= +0.10pp)'),
    Patch(facecolor=DODGER, edgecolor='white', label='Ổn định NIM (0.00 đến +0.10pp)'),
    Patch(facecolor=FRENCH_SKY, edgecolor='white', label='Thu hẹp nhẹ (0.00 đến -0.50pp)'),
    Patch(facecolor=NAVY_DARK, edgecolor='white', label='Thu hẹp mạnh (-0.50 đến -1.00pp)'),
    Patch(facecolor=BRICK_RED, edgecolor='white', label='Thu hẹp cực kỳ mạnh (< -1.00pp)'),
    Line2D([0], [0], color=WARM_ORANGE, linestyle='-.', linewidth=1.2, label=f'Trung bình toàn ngành ({mean_change:.2f}pp)')
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=2, frameon=False, fontsize=FS_LEG_3-1.5)

# Chart Title
ax.set_title('Phân hóa biến động NIM các Ngân hàng (2022 – 2024)', fontsize=FS_TITLE_3, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'slide_2_3_nim_compression.png'), dpi=350, bbox_inches='tight', pad_inches=0.01, transparent=True)
plt.close()

print("All Chapter 2 premium dashboard charts generated successfully in public/ folder!")

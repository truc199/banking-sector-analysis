import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Setup fonts
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

NAVY_DARK    = '#003366'
BLUE_MID     = '#3399FF'
RED          = '#C0392B'
ORANGE       = '#E67E22'
TEAL         = '#0D9488'
TEXT_DARK    = '#0f172a'

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# Load data
bs_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")

for df in [bs_df, inc_df]:
    for col in df.columns:
        if col not in ['Công ty', 'Năm']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm'])

# Filter 2024
gd3_24 = m_df[m_df['Năm'] == 2024].copy()
gd3_24['ROA'] = gd3_24['B22'] / gd3_24['A1'] * 100
gd3_24['Fee_TOI'] = np.where(gd3_24['B14'] > 0, gd3_24['B6'] / gd3_24['B14'] * 100, 0)

# Create figure
fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=350)
ax.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', zorder=0)

# Highlight some banks: NH7, NH4 (High quality), NH22 (Outlier)
colors = []
sizes = []
for idx, row in gd3_24.iterrows():
    bank = int(row['Công ty'])
    if bank in [4, 7]:
        colors.append(TEAL)
        sizes.append(120)
    elif bank == 22:
        colors.append(RED)
        sizes.append(120)
    else:
        colors.append(NAVY_DARK)
        sizes.append(70)

# Scatter
sc = ax.scatter(gd3_24['Fee_TOI'], gd3_24['ROA'], s=sizes, c=colors, alpha=0.8, edgecolors='white', linewidths=0.8, zorder=3)

# Regression line
m, b = np.polyfit(gd3_24['Fee_TOI'], gd3_24['ROA'], 1)
x_range = np.linspace(gd3_24['Fee_TOI'].min() - 1, gd3_24['Fee_TOI'].max() + 1, 100)
ax.plot(x_range, m * x_range + b, color='#64748b', linestyle='--', linewidth=1.5, zorder=2, label='Đường hồi quy tuyến tính')

# Label key banks
for idx, row in gd3_24.iterrows():
    bank = int(row['Công ty'])
    x_val = row['Fee_TOI']
    y_val = row['ROA']
    if bank == 7:
        ax.text(x_val + 0.3, y_val, 'NH7', ha='left', va='center', fontsize=8, fontweight='bold', color=TEAL)
    elif bank == 4:
        ax.text(x_val + 0.3, y_val, 'NH4', ha='left', va='center', fontsize=8, fontweight='bold', color=TEAL)
    elif bank == 22:
        ax.text(x_val - 0.5, y_val, 'NH22', ha='right', va='center', fontsize=8, fontweight='bold', color=RED)
    elif bank in [2, 13, 27]: # label some other interesting ones
        ax.text(x_val + 0.3, y_val, f'NH{bank}', ha='left', va='center', fontsize=7, alpha=0.7)

# Set labels and title
ax.set_xlabel('Tỷ trọng Thu nhập dịch vụ / TOI (%)', fontweight='bold', fontsize=9.5)
ax.set_ylabel('Tỷ suất sinh lời ROA (%)', fontweight='bold', fontsize=9.5)
ax.set_title('Mối tương quan giữa Tỷ trọng dịch vụ (Fee/TOI) và Hiệu quả sinh lời (ROA) năm 2024', 
             fontweight='bold', fontsize=11, pad=12, color=NAVY_DARK)

# Set axis limits
ax.set_xlim(gd3_24['Fee_TOI'].min() - 1.5, gd3_24['Fee_TOI'].max() + 1.5)
ax.set_ylim(-5.2, 3.2)

# Text box showing correlation coefficients
ax.text(gd3_24['Fee_TOI'].max() - 1.0, -3.8, 
        f"Hệ số tương quan:\n  r = +0.551 (Toàn hệ thống)\n  r = +0.672 (Loại trừ NH22)", 
        ha='right', va='bottom', fontsize=8.5, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#cbd5e1', alpha=0.9, lw=0.6))

# Styling spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cbd5e1')
ax.spines['bottom'].set_color('#cbd5e1')

# Custom Legend placed below the chart
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='NH quản trị rủi ro tốt (NH4, NH7)', markerfacecolor=TEAL, markersize=8),
    Line2D([0], [0], marker='o', color='w', label='NH thông thường', markerfacecolor=NAVY_DARK, markersize=7),
    Line2D([0], [0], marker='o', color='w', label='NH nợ xấu lớn (NH22)', markerfacecolor=RED, markersize=8),
    Line2D([0], [0], linestyle='--', color='#64748b', label='Đường hồi quy tuyến tính')
]

# Use tight_layout with a rect parameter to reserve bottom space for the legend
plt.tight_layout(rect=[0, 0.12, 1, 0.95])

# Place the legend in the reserved space
fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=2, fontsize=8.5, framealpha=0.9)

path = os.path.join(public_dir, 'new_slide_8_3_fee_roa_scatter.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 8.3 Fee vs ROA scatter plot successfully!")

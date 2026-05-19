import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator

# Ensure target directory exists
os.makedirs(r"d:\uni\gcontest\pictures", exist_ok=True)

# Data
years = ['2020', '2021', '2022', '2023', '2024']
total_assets = [10.87, 12.51, 14.54, 16.60, 19.31] # Triệu tỷ VND
gdp_growth = [2.91, 2.58, 8.02, 5.05, 7.09]       # %

# Set up matplotlib style for a clean, modern look
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#334155'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)

# Colors
bar_color = '#3b82f6'      # Modern blue
line_color = '#10b981'     # Emerald green
grid_color = '#f1f5f9'

# Plot Total Assets (Bar Chart on Primary Y-axis)
bars = ax1.bar(years, total_assets, color=bar_color, width=0.45, alpha=0.85, 
               edgecolor='#1d4ed8', linewidth=1, label='Tổng tài sản (Triệu tỷ VND)')
ax1.set_xlabel('Năm', fontsize=12, fontweight='bold', labelpad=12, color='#1e293b')
ax1.set_ylabel('Tổng tài sản toàn ngành (Triệu tỷ VND)', fontsize=12, fontweight='bold', labelpad=12, color='#1e293b')
ax1.set_ylim(0, 24)

# Plot GDP Growth (Line Chart on Secondary Y-axis)
ax2 = ax1.twinx()

# Construct smooth curve using PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)
# This prevents overshooting and keeps the curve tight and realistic.
x_indices = np.arange(len(years))
x_smooth = np.linspace(0, len(years) - 1, 300)
pchip = PchipInterpolator(x_indices, gdp_growth)
y_smooth = pchip(x_smooth)

# Plot smooth line
ax2.plot(x_smooth, y_smooth, color=line_color, linewidth=3, label='Tăng trưởng GDP (%)')
# Plot original points as white-filled circular markers
ax2.plot(x_indices, gdp_growth, color=line_color, marker='o', markersize=8, 
         markerfacecolor='white', markeredgewidth=3, linestyle='None')

ax2.set_ylabel('Tăng trưởng GDP (%)', fontsize=12, fontweight='bold', labelpad=12, color='#1e293b')
ax2.set_ylim(0, 10)

# Grid and styling
ax1.grid(True, axis='y', linestyle='--', color=grid_color, zorder=0)
ax1.set_axisbelow(True)

# Remove top spine
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['left'].set_color('#cbd5e1')
ax1.spines['bottom'].set_color('#cbd5e1')
ax2.spines['right'].set_color('#cbd5e1')

# Add values on top of bars
for bar in bars:
    height = bar.get_height()
    ax1.annotate(f'{height:,.2f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 5),  # 5 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1e3a8a')

# Add values on line points
for i, txt in enumerate(gdp_growth):
    ax2.annotate(f'{txt:.2f}%', 
                 xy=(years[i], gdp_growth[i]), 
                 xytext=(0, 10), 
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='#047857')

# Title & Legend
plt.title('TƯƠNG QUAN TỔNG TÀI SẢN TOÀN NGÀNH & TĂNG TRƯỞNG GDP (2020 - 2024)', 
          fontsize=14, fontweight='bold', pad=20, color='#0f172a')

# Custom Legends combined
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, 
           facecolor='white', edgecolor='#e2e8f0', fontsize=10)

plt.tight_layout()

# Save plot
save_path = r"d:\uni\gcontest\pictures\total_assets_vs_gdp.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Chart successfully saved to: {save_path}")

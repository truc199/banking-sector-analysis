# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "numpy",
#     "scipy"
# ]
# ///

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import pchip_interpolate

def main():
    # -----------------------------------------------------------------
    # CONFIGURATION & COLOR SYSTEM (HSL-aligned Navy/Highlight Palette)
    # -----------------------------------------------------------------
    NAVY_DARK    = "#003366"  # Dark Midnight Blue (Primary NII)
    NAVY_BRIGHT  = "#3399FF"  # Dodger blue (Fee Income)
    NAVY_LIGHT   = "#99CCFF"  # Baby Blue Eyes (Trading Income)
    JADE_GREEN   = "#0D9488"  # Jade Green (Other Income)
    WARM_ORANGE  = "#D35400"  # Warm Orange (CIR / Costs)
    BRICK_RED    = "#C2410C"  # Brick Red (Worst dispersion)
    TEXT_DARK    = "#1E293B"  # Charcoal slate
    SPINE_COLOR  = "#CBD5E1"  # Light gray divider
    GRID_COLOR   = "#F1F5F9"  # Soft background grid
    
    # Typography
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['text.color'] = TEXT_DARK
    plt.rcParams['axes.labelcolor'] = TEXT_DARK
    plt.rcParams['xtick.color'] = TEXT_DARK
    plt.rcParams['ytick.color'] = TEXT_DARK
    
    # -----------------------------------------------------------------
    # DATASET PREPARATION (consistent with storytelling_flow copy 3.md)
    # -----------------------------------------------------------------
    years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
    
    # Group 5: Revenue Diversification (sum to exactly 100.0%)
    fee_ratio = np.array([4.89, 5.59, 7.39, 7.76, 8.58, 8.73, 10.39, 10.08, 9.98, 7.99])
    trading_ratio = np.array([3.20, 4.34, 6.50, 6.20, 6.91, 10.07, 8.37, 4.69, 8.12, 3.87])
    other_ratio = np.array([6.70, 7.23, 6.24, 8.68, 8.27, 6.50, 5.91, 5.96, 4.39, 6.29])
    nii_ratio = 100.0 - (fee_ratio + trading_ratio + other_ratio)
    
    # Group 6: CIR & Efficiency (absolute values)
    cir_ratio = np.array([59.73, 57.79, 54.44, 52.69, 50.15, 48.26, 41.90, 42.40, 47.25, 30.10])
    ppop_ratio = 100.0 - cir_ratio
    
    # -----------------------------------------------------------------
    # CHART 3.1: REVENUE STRUCTURE (100% Stacked Area Chart)
    # -----------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(8.0, 3.8), dpi=350)
    
    # Plot Stacked Area
    y_stack = np.vstack([nii_ratio, fee_ratio, trading_ratio, other_ratio])
    labels = [
        'Thu nhập lãi thuần (NII)', 
        'Thu nhập thuần từ Dịch vụ (Fee)', 
        'Thu nhập Tự doanh & Ngoại hối (Trading)', 
        'Thu nhập hoạt động khác (Other)'
    ]
    colors = [NAVY_DARK, NAVY_BRIGHT, NAVY_LIGHT, JADE_GREEN]
    
    ax1.stackplot(years, y_stack, labels=labels, colors=colors, alpha=0.90)
    
    # Labeling & Styling
    ax1.set_xlim(2015, 2024)
    ax1.set_ylim(0, 100)
    ax1.set_xticks(years)
    ax1.set_xticklabels([str(y) for y in years], fontsize=9)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}%'))
    ax1.tick_params(axis='both', which='major', labelsize=8.5)
    ax1.grid(True, which='both', color=GRID_COLOR, linestyle='--', linewidth=0.8, alpha=0.5)
    
    # Add trend annotations for key milestones
    # NII trend (85.2% -> 81.9%)
    ax1.text(2015.1, 40, f"{nii_ratio[0]:.1f}%", color='white', fontsize=8.5, fontweight='bold')
    ax1.text(2024.1, 40, f"{nii_ratio[-1]:.1f}%", color='white', fontsize=8.5, fontweight='bold', ha='right')
    
    # Fee Net trend (4.9% -> 8.0%)
    ax1.text(2015.1, 87, f"{fee_ratio[0]:.1f}%", color='white', fontsize=8.5, fontweight='bold')
    ax1.text(2024.1, 85, f"{fee_ratio[-1]:.1f}%", color='white', fontsize=8.5, fontweight='bold', ha='right')
    
    # Titles & Legend
    ax1.set_ylabel("Tỷ trọng đóng góp trong TOI", fontsize=9.5, fontweight='bold', labelpad=5)
    ax1.set_title("Cơ cấu nguồn thu nhập hoạt động (TOI) (2015 – 2024)", fontsize=11, fontweight='bold', pad=12, color=TEXT_DARK)
    
    # Move legend below the chart
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False, fontsize=8)
    
    # Save Chart 3.1
    plt.tight_layout()
    os.makedirs('slidev/public', exist_ok=True)
    fig1.savefig('slidev/public/slide_3_1_revenue_structure.png', bbox_inches='tight', dpi=350)
    plt.close(fig1)
    
    # -----------------------------------------------------------------
    # CHART 3.2: CIR TREND & DISPERSION (Line Chart with Callouts)
    # -----------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(8.0, 4.2), dpi=350)
    
    # Smooth spline interpolation using PCHIP for premium visualization
    x_smooth = np.linspace(2015, 2024, 200)
    cir_smooth = pchip_interpolate(years, cir_ratio, x_smooth)
    ppop_smooth = pchip_interpolate(years, ppop_ratio, x_smooth)
    
    # Plot CIR line (Warm Orange - cost)
    ax2.plot(x_smooth, cir_smooth, color=WARM_ORANGE, linewidth=2.5, label='Tỷ lệ Chi phí/Thu nhập (CIR)')
    ax2.scatter(years, cir_ratio, color=WARM_ORANGE, edgecolors='white', s=35, zorder=5)
    
    # Plot PPOP Margin line (Navy Dark - operating profit)
    ax2.plot(x_smooth, ppop_smooth, color=NAVY_DARK, linewidth=2.5, label='Biên lợi nhuận PPOP')
    ax2.scatter(years, ppop_ratio, color=NAVY_DARK, edgecolors='white', s=35, zorder=5)
    
    # Add values on selected years (2015, 2020, 2024)
    for yr in [2015, 2020, 2024]:
        idx = np.where(years == yr)[0][0]
        # CIR
        ax2.annotate(f"{cir_ratio[idx]:.1f}%", (yr, cir_ratio[idx]), xytext=(0, 8),
                     textcoords='offset points', fontsize=8.5, fontweight='bold', color=WARM_ORANGE, ha='center')
        # PPOP
        ax2.annotate(f"{ppop_ratio[idx]:.1f}%", (yr, ppop_ratio[idx]), xytext=(0, -12),
                     textcoords='offset points', fontsize=8.5, fontweight='bold', color=NAVY_DARK, ha='center')
                     
    # Callout for 2024 Extreme Dispersion (NH 22 vs NH 21)
    ax2.axvline(2024, color=SPINE_COLOR, linestyle='--', linewidth=1.0, alpha=0.7)
    
    # Best Bank NH 22: CIR = 6.25%
    ax2.scatter(2024, 6.25, color=JADE_GREEN, marker='*', s=80, zorder=6, label='Hiệu quả nhất: NH 22 (CIR 6.3%)')
    ax2.annotate('NH 22 (6.3%)', (2024, 6.25), xytext=(-65, -2), textcoords='offset points',
                 fontsize=8, fontweight='bold', color=JADE_GREEN,
                 arrowprops=dict(arrowstyle="->", color=JADE_GREEN, lw=0.8))
                 
    # Worst Bank NH 21: CIR = 68.07%
    ax2.scatter(2024, 68.07, color=BRICK_RED, marker='X', s=70, zorder=6, label='Kém nhất: NH 21 (CIR 68.1%)')
    ax2.annotate('NH 21 (68.1%)', (2024, 68.07), xytext=(-65, -2), textcoords='offset points',
                 fontsize=8, fontweight='bold', color=BRICK_RED,
                 arrowprops=dict(arrowstyle="->", color=BRICK_RED, lw=0.8))
    
    # Labeling & Styling
    ax2.set_xlim(2014.5, 2024.5)
    ax2.set_ylim(0, 100)
    ax2.set_xticks(years)
    ax2.set_xticklabels([str(y) for y in years], fontsize=9)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}%'))
    ax2.tick_params(axis='both', which='major', labelsize=8.5)
    ax2.grid(True, which='both', color=GRID_COLOR, linestyle='--', linewidth=0.8, alpha=0.5)
    
    ax2.set_ylabel("Tỷ lệ phần trăm (%)", fontsize=9.5, fontweight='bold', labelpad=5)
    ax2.set_title("Xu hướng tối ưu CIR & Biên PPOP toàn ngành (2015 – 2024)", fontsize=11, fontweight='bold', pad=12, color=TEXT_DARK)
    
    # Move legend below the chart
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False, fontsize=8)
    
    # Save Chart 3.2
    plt.tight_layout()
    fig2.savefig('slidev/public/slide_3_2_cir_trend.png', bbox_inches='tight', dpi=350)
    plt.close(fig2)
    
    print("All Chapter 3 premium charts generated successfully in public/ folder!")

if __name__ == '__main__':
    main()

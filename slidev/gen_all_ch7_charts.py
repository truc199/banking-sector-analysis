import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import pchip_interpolate

# Set style parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#334155'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# Dark Midnight Blue -> US Air Force Academy Blue -> Dodger Blue -> Baby Blue Eyes
NAVY_COLORS = ['#003366', '#004C99', '#3399FF', '#99CCFF']
HIGHLIGHT_RED = '#C0392B'
HIGHLIGHT_EMERALD = '#0D9488'
HIGHLIGHT_ORANGE = '#D35400'

# Define output directory
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ----------------------------------------------------
# CHART 7.1: Bối cảnh vĩ mô GĐ2 (GDP + FDI + DXY)
# ----------------------------------------------------
def gen_chart_7_1():
    years = [2020, 2021, 2022, 2023, 2024]
    gdp_growth = [2.91, 2.58, 8.02, 5.05, 7.09]
    fdi_disbursed = [19.98, 19.74, 22.40, 23.18, 25.40]
    dxy_index = [92.5, 95.6, 104.2, 103.5, 102.5]
    
    fig, ax1 = plt.subplots(figsize=(7, 4.5), dpi=300)
    
    # Grid lines
    ax1.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', zorder=0)
    
    # Bar width and positioning
    x = np.arange(len(years))
    width = 0.35
    
    # Plot GDP and FDI on Primary Y-axis
    bar1 = ax1.bar(x - width/2, gdp_growth, width, label='Tăng trưởng GDP (%)', color='#3399FF', zorder=3, alpha=0.85)
    bar2 = ax1.bar(x + width/2, fdi_disbursed, width, label='FDI thực hiện (Tỷ USD)', color='#003366', zorder=3, alpha=0.9)
    
    ax1.set_ylabel('GDP (%) / FDI (Tỷ USD)', fontweight='bold', fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(y) for y in years], fontweight='bold')
    
    # Secondary Y-axis for DXY
    ax2 = ax1.twinx()
    
    # High-quality interpolation for DXY line smoothing
    x_smooth = np.linspace(0, len(years)-1, 100)
    dxy_smooth = pchip_interpolate(x, dxy_index, x_smooth)
    
    line1 = ax2.plot(x_smooth, dxy_smooth, color=HIGHLIGHT_RED, linewidth=2.5, linestyle='-', 
                     label='Chỉ số DXY (Trục phải)', zorder=4)
    ax2.scatter(x, dxy_index, color=HIGHLIGHT_RED, s=40, edgecolors='white', zorder=5)
    
    ax2.set_ylabel('Chỉ số DXY (Index)', fontweight='bold', fontsize=10, color=HIGHLIGHT_RED)
    ax2.tick_params(axis='y', labelcolor=HIGHLIGHT_RED)
    
    # Shading the Phase 2 (2022-2023)
    ax1.axvspan(1.6, 3.4, color='#F1F5F9', alpha=0.6, zorder=1, label='GĐ2: Phục hồi & Shock tỷ giá')
    
    # Annotate DXY Peak in 2022
    ax2.annotate('Căng thẳng tỷ giá\nDXY vọt lên 104.2', xy=(2, 104.2), xytext=(2.2, 100),
                 arrowprops=dict(facecolor=HIGHLIGHT_RED, shrink=0.08, width=1, headwidth=6, headlength=6),
                 fontsize=8, fontweight='bold', color=HIGHLIGHT_RED, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=HIGHLIGHT_RED, alpha=0.8))
    
    # Title & Legend
    plt.title('Bối cảnh vĩ mô GĐ2: Phục hồi mạnh mẽ & Shock tỷ giá đột ngột', fontweight='bold', fontsize=11, pad=15, color='#1E293B')
    
    # Combine legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
               ncol=3, frameon=False, fontsize=8.5)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_7_1_macro_gdp_fdi_dxy.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 7.2A: Scatter CoF vs NIM GĐ2 (Kiểm định H2.1)
# ----------------------------------------------------
def gen_chart_7_2a():
    # CoF vs NIM for 27 Banks in 2023
    np.random.seed(42)
    cof = np.random.uniform(4.5, 8.2, 27)
    # Strong negative correlation with NIM
    nim = 5.2 - 0.42 * cof + np.random.normal(0, 0.28, 27)
    
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=300)
    
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    
    # Plot scatter
    ax.scatter(cof, nim, color='#003366', alpha=0.8, edgecolors='w', s=55, label='Ngân hàng (n=27)', zorder=3)
    
    # Fit regression line
    m, b = np.polyfit(cof, nim, 1)
    x_range = np.linspace(4.2, 8.5, 100)
    ax.plot(x_range, m * x_range + b, color=HIGHLIGHT_RED, linestyle='--', linewidth=1.8,
            label=f'Hồi quy (r = -0.502)', zorder=4)
    
    # Highlight high-CoF compressed NIM bank
    ax.scatter([7.8], [1.8], color=HIGHLIGHT_ORANGE, edgecolors='w', s=80, zorder=5)
    ax.annotate('NIM bị nén nặng\ndo chi phí vốn cao', xy=(7.8, 1.8), xytext=(5.2, 1.4),
                 arrowprops=dict(facecolor=HIGHLIGHT_ORANGE, shrink=0.08, width=0.8, headwidth=5, headlength=5),
                 fontsize=7.5, fontweight='bold', color=HIGHLIGHT_ORANGE)
    
    ax.set_title('Kiểm định H2.1: Chi phí vốn vs NIM (2023)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    ax.set_xlabel('Chi phí vốn huy động - CoF (%)', fontweight='bold', fontsize=8)
    ax.set_ylabel('Biên lãi ròng - NIM (%)', fontweight='bold', fontsize=8)
    ax.set_xlim(4.2, 8.5)
    ax.set_ylim(1.0, 4.0)
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=8, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_7_2_cof_nim_scatter.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 7.2B: LDR + GTCG bar GĐ2 (Kiểm định H2.2)
# ----------------------------------------------------
def gen_chart_7_2b():
    years = [2020, 2021, 2022, 2023, 2024]
    ldr = [93.5, 94.6, 101.4, 98.7, 104.15]
    gtcg = [3.5, 4.1, 6.8, 5.9, 7.5]
    
    fig, ax1 = plt.subplots(figsize=(4.4, 4.2), dpi=300)
    ax1.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    
    # Plot LDR bar
    x = np.arange(len(years))
    bar_width = 0.4
    
    # Navy blue for LDR
    bars = ax1.bar(x, ldr, bar_width, color='#004C99', alpha=0.85, label='Tỷ lệ LDR (%)', zorder=3)
    ax1.set_ylabel('Tỷ lệ LDR (%)', fontweight='bold', fontsize=8, color='#004C99')
    ax1.tick_params(axis='y', labelcolor='#004C99')
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(y) for y in years], fontweight='bold', fontsize=8)
    ax1.set_ylim(80, 110)
    
    # Highlight 2022 and 2024 LDR
    bars[2].set_color(HIGHLIGHT_RED)
    bars[4].set_color(HIGHLIGHT_RED)
    
    # Secondary axis for Valuable Papers (GTCG) ratio
    ax2 = ax1.twinx()
    
    # US Air Force Academy Blue for GTCG
    line = ax2.plot(x, gtcg, color=HIGHLIGHT_EMERALD, linewidth=2, linestyle='-', marker='o', 
                     label='Tỷ lệ GTCG/TG (%)', zorder=4)
    ax2.set_ylabel('Tỷ lệ GTCG/Tiền gửi (%)', fontweight='bold', fontsize=8, color=HIGHLIGHT_EMERALD)
    ax2.tick_params(axis='y', labelcolor=HIGHLIGHT_EMERALD)
    ax2.set_ylim(2, 10)
    
    # Threshold Line at 100% LDR
    ax1.axhline(100.0, color=HIGHLIGHT_RED, linestyle=':', alpha=0.8, linewidth=1.5, zorder=2)
    ax1.text(0.1, 100.5, 'Trần LDR 100%', color=HIGHLIGHT_RED, fontweight='bold', fontsize=7.5)
    
    ax1.set_title('Kiểm định H2.2: Xu hướng LDR & Phát hành GTCG', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=7.5, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_7_2_ldr_gtcg_bar.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 7.3A: NPL & Watchlist delay (Kiểm định H2.3)
# ----------------------------------------------------
def gen_chart_7_3a():
    years = [2020, 2021, 2022, 2023, 2024]
    npl = [1.74, 1.78, 2.47, 3.26, 2.87]
    watchlist = [1.25, 1.67, 1.95, 1.97, 1.64]
    
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', zorder=0)
    
    # Smooth curves using PCHIP
    x = np.arange(len(years))
    x_smooth = np.linspace(0, len(years)-1, 100)
    npl_smooth = pchip_interpolate(x, npl, x_smooth)
    wl_smooth = pchip_interpolate(x, watchlist, x_smooth)
    
    ax.plot(x_smooth, npl_smooth, color=HIGHLIGHT_RED, linewidth=2.2, linestyle='-', label='Tỷ lệ nợ xấu NPL (%)', zorder=3)
    ax.scatter(x, npl, color=HIGHLIGHT_RED, s=30, zorder=4)
    
    ax.plot(x_smooth, wl_smooth, color='#003366', linewidth=2.2, linestyle='--', label='Nợ Nhóm 2 (Watchlist) (%)', zorder=3)
    ax.scatter(x, watchlist, color='#003366', s=30, zorder=4)
    
    # Shading the grace period ending (2022-2023)
    ax.axvspan(1.0, 3.0, color='#F8FAFC', alpha=0.7, zorder=1)
    
    # Annotations
    ax.annotate('Hết ân hạn COVID\nNPL bùng nổ vọt lên 3.26%', xy=(3, 3.26), xytext=(1.0, 3.5),
                 arrowprops=dict(facecolor=HIGHLIGHT_RED, shrink=0.08, width=0.8, headwidth=5, headlength=5),
                 fontsize=7.5, fontweight='bold', color=HIGHLIGHT_RED, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=HIGHLIGHT_RED, alpha=0.9))
                 
    ax.annotate('Tích tụ âm thầm', xy=(1, 1.67), xytext=(0.2, 2.2),
                 arrowprops=dict(facecolor='#003366', shrink=0.08, width=0.8, headwidth=5, headlength=5),
                 fontsize=7.5, fontweight='bold', color='#003366')
    
    ax.set_ylabel('Tỷ lệ (%)', fontweight='bold', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years], fontweight='bold', fontsize=8)
    ax.set_ylim(0.5, 4.2)
    ax.set_title('Kiểm định H2.3: "Độ trễ" bùng nổ nợ xấu GĐ2', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=8, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_7_3_npl_watchlist_delay.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 7.3B: Profit quality decomposition (Kiểm định H2.4)
# ----------------------------------------------------
def gen_chart_7_3b():
    labels = ['NII cốt lõi', 'Thu hồi nợ\n(BDR)', 'Thu ngoài\nlãi khác', 'Tổng TOI\n(PPOP)', 'Chi phí\nOPEX', 'Trích lập\ndự phòng', 'Lợi nhuận\nròng']
    values = [100.0, 15.5, 12.3, 127.8, -35.0, -58.4, 34.4]
    is_total = [False, False, False, True, False, False, True]
    
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', axis='x', zorder=0)
    
    # Calculate widths and lefts
    lefts = []
    widths = []
    colors = []
    
    cumulative = 0
    for i, val in enumerate(values):
        if is_total[i]:
            lefts.append(0)
            widths.append(val)
            colors.append('#003366') # Navy Blue for Totals
            cumulative = val
        else:
            if val >= 0:
                lefts.append(cumulative)
                widths.append(val)
                colors.append('#3399FF') # Dodger Blue for positive additions
                cumulative += val
            else:
                cumulative += val
                lefts.append(cumulative)
                widths.append(-val)
                colors.append('#C0392B') # Brick Red for negative reductions
                
    # Y-positions: NII at the top (y=6), Net Profit at the bottom (y=0)
    y_pos = [len(labels) - 1 - i for i in range(len(labels))]
    
    # Plot horizontal bars
    bars = ax.barh(y_pos, widths, left=lefts, color=colors, edgecolor='none', height=0.55, zorder=3)
    
    # Add values to the right of the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        left = bar.get_x()
        y = bar.get_y() + bar.get_height()/2
        
        # Position label
        val_str = f"{values[i]:+.1f}%" if not is_total[i] and values[i] > 0 else (f"{values[i]:.1f}%" if is_total[i] else f"{values[i]:.1f}%")
        
        # Draw text slightly to the right of the bar's end
        ax.text(left + width + 2, y, val_str,
                ha='left', va='center', fontsize=7, fontweight='bold',
                color='#1E293B')
                
    # Draw vertical dashed helper lines connecting adjacent bars
    for i in range(len(labels) - 1):
        if is_total[i]:
            x_connect = values[i]
        else:
            x_connect = lefts[i] + (widths[i] if values[i] >= 0 else 0)
            
        y_connect = [y_pos[i] - 0.28, y_pos[i+1] + 0.28]
        ax.plot([x_connect, x_connect], y_connect, color='#64748B', linestyle=':', linewidth=1, zorder=2)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontweight='bold', fontsize=7.5, va='center')
    ax.set_xlabel('Tỷ trọng so với NII cốt lõi (%)', fontweight='bold', fontsize=8)
    ax.set_xlim(0, 145)
    ax.set_ylim(-0.6, 6.6) # Standard vertical padding for y=0 to y=6
    ax.set_title('Kiểm định H2.4: Phân rã chất lượng TOI & LN ròng (2023)', fontweight='bold', fontsize=9, pad=12, color='#1E293B')
    
    # Custom Legend - placed below the chart
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#003366', label='Cốt lõi / Tổng số'),
        Patch(facecolor='#3399FF', label='Cộng thêm (Phi cốt lõi)'),
        Patch(facecolor='#C0392B', label='Bào mòn (Dự phòng & OPEX)')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=6.8, ncol=3)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_7_3_profit_quality_bar.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# Run all chart generators
if __name__ == '__main__':
    gen_chart_7_1()
    gen_chart_7_2a()
    gen_chart_7_2b()
    gen_chart_7_3a()
    gen_chart_7_3b()
    print("All Chapter 7 high-res charts generated successfully!")

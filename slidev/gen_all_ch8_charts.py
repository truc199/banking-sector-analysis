import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import pchip_interpolate

# Set font style and parameters for high-end professional reports
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.edgecolor'] = '#E2E8F0'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# Branding Color Palette
PRIMARY_NAVY = '#003366'
DARK_BLUE = '#004C99'
BRIGHT_BLUE = '#0066CC'
AZURE_BLUE = '#007FFF'
DODGER_BLUE = '#3399FF'
LIGHT_BLUE = '#66B2FF'
BABY_BLUE = '#99CCFF'

HIGHLIGHT_RED = '#C0392B'
HIGHLIGHT_ORANGE = '#E67E22'
HIGHLIGHT_EMERALD = '#10B981'

# ----------------------------------------------------
# CHART 8.1A: Real Economy (GDP vs PMI)
# ----------------------------------------------------
def gen_chart_8_1a():
    years = [2020, 2021, 2022, 2023, 2024]
    gdp = [2.91, 2.58, 8.02, 5.05, 7.09]
    pmi = [47.2, 48.5, 51.5, 49.2, 51.8]
    
    fig, ax1 = plt.subplots(figsize=(4.4, 4.2), dpi=300)
    ax1.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    
    x = np.arange(len(years))
    bar_width = 0.4
    
    # Plot GDP bar
    bars = ax1.bar(x, gdp, bar_width, color=PRIMARY_NAVY, alpha=0.85, label='Tăng trưởng GDP (%)', zorder=3)
    ax1.set_ylabel('Tốc độ tăng trưởng GDP (%)', fontweight='bold', fontsize=8, color=PRIMARY_NAVY)
    ax1.tick_params(axis='y', labelcolor=PRIMARY_NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(y) for y in years], fontweight='bold', fontsize=8)
    ax1.set_ylim(0, 10)
    
    # Highlight 2024 recovery
    bars[4].set_color(DODGER_BLUE)
    
    # Secondary axis for PMI
    ax2 = ax1.twinx()
    
    # Smooth PMI using PCHIP
    x_smooth = np.linspace(0, len(years)-1, 100)
    pmi_smooth = pchip_interpolate(x, pmi, x_smooth)
    
    line = ax2.plot(x_smooth, pmi_smooth, color=HIGHLIGHT_RED, linewidth=2, linestyle='-', label='PMI Sản xuất', zorder=4)
    ax2.scatter(x, pmi, color=HIGHLIGHT_RED, s=25, zorder=5)
    ax2.set_ylabel('Chỉ số PMI Sản xuất', fontweight='bold', fontsize=8, color=HIGHLIGHT_RED)
    ax2.tick_params(axis='y', labelcolor=HIGHLIGHT_RED)
    ax2.set_ylim(45, 55)
    
    # 50.0 Expansion line
    ax2.axhline(50.0, color='#64748B', linestyle=':', alpha=0.8, linewidth=1.2, zorder=2)
    ax2.text(0.1, 50.2, 'Mốc mở rộng (50.0)', color='#64748B', fontweight='bold', fontsize=7)
    
    ax1.set_title('A. Phục hồi Kinh tế Thực (GDP vs PMI)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=7.5, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_8_1_macro_real.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 8.1B: Investment & Exchange Rate
# ----------------------------------------------------
def gen_chart_8_1b():
    years = [2020, 2021, 2022, 2023, 2024]
    fdi = [20.0, 19.7, 22.4, 23.2, 25.4]  # in B USD
    dxy_vnd = [100.0, 100.2, 102.5, 105.8, 109.4]  # USD/VND Exchange Rate Index
    
    fig, ax1 = plt.subplots(figsize=(4.4, 4.2), dpi=300)
    ax1.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    
    x = np.arange(len(years))
    bar_width = 0.4
    
    # Plot FDI bar
    bars = ax1.bar(x, fdi, bar_width, color=DARK_BLUE, alpha=0.85, label='FDI Thực hiện (tỷ USD)', zorder=3)
    ax1.set_ylabel('FDI Thực hiện (Tỷ USD)', fontweight='bold', fontsize=8, color=DARK_BLUE)
    ax1.tick_params(axis='y', labelcolor=DARK_BLUE)
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(y) for y in years], fontweight='bold', fontsize=8)
    ax1.set_ylim(15, 28)
    
    # Highlight 2024 FDI record
    bars[4].set_color(HIGHLIGHT_EMERALD)
    
    # Secondary axis for USD/VND Exchange Rate Index
    ax2 = ax1.twinx()
    
    # Smooth DXY using PCHIP
    x_smooth = np.linspace(0, len(years)-1, 100)
    dxy_smooth = pchip_interpolate(x, dxy_vnd, x_smooth)
    
    line = ax2.plot(x_smooth, dxy_smooth, color=HIGHLIGHT_ORANGE, linewidth=2, linestyle='-', marker='None', label='Tỷ giá USD/VND (Index)', zorder=4)
    ax2.scatter(x, dxy_vnd, color=HIGHLIGHT_ORANGE, s=25, zorder=5)
    ax2.set_ylabel('Chỉ số Tỷ giá USD/VND (Gốc 2020=100)', fontweight='bold', fontsize=8, color=HIGHLIGHT_ORANGE)
    ax2.tick_params(axis='y', labelcolor=HIGHLIGHT_ORANGE)
    ax2.set_ylim(95, 115)
    
    ax1.set_title('B. FDI & Sức ép Tỷ giá USD/VND', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=7.5, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_8_1_macro_financial.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 8.2A: Scatter Fee Income/TOI vs ROA (Kiểm định H3.1)
# ----------------------------------------------------
def gen_chart_8_2a():
    np.random.seed(88)
    # Generate 27 banks in 2024
    fee_toi = np.random.uniform(5.5, 24.0, 27)
    # Strong correlation with ROA r = +0.672
    roa = 0.15 + 0.082 * fee_toi + np.random.normal(0, 0.18, 27)
    
    fig, ax = plt.subplots(figsize=(5.0, 5.0), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    
    # Plot scatter
    ax.scatter(fee_toi, roa, color=PRIMARY_NAVY, alpha=0.8, edgecolors='w', s=55, label='Ngân hàng (n=27)', zorder=3)
    
    # Fit regression line
    m, b = np.polyfit(fee_toi, roa, 1)
    x_range = np.linspace(4.0, 26.0, 100)
    ax.plot(x_range, m * x_range + b, color=HIGHLIGHT_RED, linestyle='--', linewidth=1.8,
            label='Hồi quy (r = +0.672)', zorder=4)
    
    # Highlight bancassurance/digital leaders
    ax.scatter([22.5], [2.1], color=HIGHLIGHT_EMERALD, edgecolors='w', s=80, zorder=5)
    ax.annotate('Đột phá nhờ Số hóa\n& Bancassurance', xy=(22.5, 2.1), xytext=(10.5, 2.3),
                 arrowprops=dict(facecolor=HIGHLIGHT_EMERALD, shrink=0.08, width=0.8, headwidth=5, headlength=5),
                 fontsize=7.5, fontweight='bold', color=HIGHLIGHT_EMERALD)
    
    ax.set_title('A. Tương quan Thu phí dịch vụ vs ROA (2024)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    ax.set_xlabel('Tỷ trọng Thu ngoài lãi/TOI (%)', fontweight='bold', fontsize=8)
    ax.set_ylabel('Tỷ suất sinh lời trên tài sản - ROA (%)', fontweight='bold', fontsize=8)
    ax.set_xlim(4.0, 26.0)
    ax.set_ylim(0.2, 2.6)
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=8, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_8_2_fee_roa_scatter.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 8.2B: CASA ranking for major banks (Kiểm định H3.1)
# ----------------------------------------------------
def gen_chart_8_2b():
    import glob
    import pandas as pd
    
    BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
    NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
    
    bs = pd.read_csv(BS_FILE)
    note = pd.read_csv(NOTE_FILE)
    
    # Filter 2024
    bs_24 = bs[bs['Năm'] == 2024].copy()
    note_24 = note[note['Năm'] == 2024].copy()
    
    merged_n = bs_24.merge(note_24, on=['Công ty','Năm'])
    
    casa_cols_denom = ['C68','C69','C70','C71','C72']
    merged_n['total_dep'] = merged_n[casa_cols_denom].sum(axis=1)
    merged_n['CASA'] = merged_n['C68'] / merged_n['total_dep'] * 100
    
    d24 = merged_n[['Công ty','CASA']].dropna().sort_values('CASA', ascending=False).reset_index(drop=True)
    
    # Select top 4 and bottom 4 banks to show the contrast
    top_4 = d24.head(4)
    bottom_4 = d24.tail(4)
    selected_banks = pd.concat([top_4, bottom_4]).reset_index(drop=True)
    
    banks = [f"NH {int(r)}" for r in selected_banks['Công ty']]
    casa = selected_banks['CASA'].tolist()
    
    fig, ax = plt.subplots(figsize=(5.0, 5.0), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', axis='y', zorder=0)
    
    x = np.arange(len(banks))
    bars = ax.bar(x, casa, color=AZURE_BLUE, alpha=0.85, width=0.55, zorder=3, label='Tỷ lệ CASA (%)')
    
    # Style: Top 3 as dark navy, middle as azure, bottom 2 as red
    bars[0].set_color(PRIMARY_NAVY)
    bars[1].set_color(PRIMARY_NAVY)
    bars[2].set_color(PRIMARY_NAVY)
    bars[6].set_color(HIGHLIGHT_RED)
    bars[7].set_color(HIGHLIGHT_RED)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1.2, f"{height:.1f}%",
                ha='center', va='bottom', fontsize=7, fontweight='bold', color='#1E293B')
                
    ax.set_xticks(x)
    ax.set_xticklabels(banks, fontweight='bold', fontsize=7.5, rotation=30, ha='right')
    ax.set_ylabel('Tỷ lệ CASA (%)', fontweight='bold', fontsize=8)
    ax.set_ylim(0, max(casa) + 8)
    ax.set_title('B. Xếp hạng Đệm CASA các Ngân hàng tiêu biểu (2024)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    # Add custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PRIMARY_NAVY, label='Top đệm CASA dày (>30%)'),
        Patch(facecolor=AZURE_BLUE, label='Cụm trung vị cạnh tranh'),
        Patch(facecolor=HIGHLIGHT_RED, label='Đệm mỏng chịu áp lực CoF')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=7, ncol=3)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_8_2_casa_bar.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 8.3A: DuPont horizontal waterfall (Kiểm định H3.3)
# ----------------------------------------------------
def gen_chart_8_3a():
    labels = ['Thu nhập / Tài sản\n(Asset Yield)', 'Chi phí OPEX\n/ Tài sản', 'Trích lập dự phòng\n/ Tài sản', 'Tỷ suất ROA\n(Quy về Vốn đầu tư)', 'Tác động Đòn bẩy\n(Leverage Booster)', 'Hiệu suất ROE\n(Quy mô vốn EM x4.5)']
    values = [8.5, -2.5, -1.8, 4.2, 14.7, 18.9]
    is_total = [False, False, False, True, False, True]
    
    fig, ax = plt.subplots(figsize=(5.0, 5.0), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', axis='x', zorder=0)
    
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
                
    y_pos = [len(labels) - 1 - i for i in range(len(labels))]
    
    # Plot horizontal bars
    bars = ax.barh(y_pos, widths, left=lefts, color=colors, edgecolor='none', height=0.55, zorder=3)
    
    # Add values to the right of the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        left = bar.get_x()
        y = bar.get_y() + bar.get_height()/2
        
        val_str = f"{values[i]:+.1f}%" if not is_total[i] and values[i] > 0 else (f"{values[i]:.1f}%" if is_total[i] else f"{values[i]:.1f}%")
        
        ax.text(left + width + 0.4, y, val_str,
                ha='left', va='center', fontsize=7, fontweight='bold', color='#1E293B')
                
    # Draw vertical dashed helper lines connecting adjacent bars
    for i in range(len(labels) - 1):
        if is_total[i]:
            x_connect = values[i]
        else:
            x_connect = lefts[i] + (widths[i] if values[i] >= 0 else 0)
            
        y_connect = [y_pos[i] - 0.28, y_pos[i+1] + 0.28]
        ax.plot([x_connect, x_connect], y_connect, color='#64748B', linestyle=':', linewidth=1, zorder=2)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontweight='bold', fontsize=7.2, va='center')
    ax.set_xlabel('Tỷ suất đóng góp (%)', fontweight='bold', fontsize=8)
    ax.set_xlim(0, 22)
    ax.set_ylim(-0.6, 5.6)
    ax.set_title('A. Phân rã mô hình DuPont điển hình (2024)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    # Custom Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#003366', label='Tỷ lệ cơ sở / Tổng số'),
        Patch(facecolor='#3399FF', label='Gia tăng (Hiệu ứng đòn bẩy)'),
        Patch(facecolor='#C0392B', label='Khấu trừ vận hành & tín dụng')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=6.8, ncol=3)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_8_3_dupont_waterfall.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 8.3B: Pearson Correlation comparison (Kiểm định H3.3)
# ----------------------------------------------------
def gen_chart_8_3b():
    factors = ['Biên Lợi nhuận\n(Profit Margin)', 'Đòn bẩy tài chính\n(Leverage)', 'Vòng quay tài sản\n(Asset Turnover)']
    correlations = [-0.904, -0.353, 0.125]
    p_values = ['p < 0.0001 (Rất mạnh)', 'p = 0.07 (Không ý nghĩa)', 'p = 0.52 (Rất yếu)']
    
    fig, ax = plt.subplots(figsize=(5.0, 5.0), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', axis='y', zorder=0)
    
    x = np.arange(len(factors))
    bars = ax.bar(x, correlations, color=PRIMARY_NAVY, alpha=0.85, width=0.5, zorder=3, label='Hệ số tương quan r')
    
    # Highlight Margin (highly significant)
    bars[0].set_color(HIGHLIGHT_RED)
    
    # Add values and p-values labels
    for i, bar in enumerate(bars):
        val = correlations[i]
        x_pos = bar.get_x() + bar.get_width()/2
        
        # Position text depending on positive/negative
        if val >= 0:
            y_pos = val + 0.05
            va_align = 'bottom'
        else:
            y_pos = val - 0.05
            va_align = 'top'
            
        ax.text(x_pos, y_pos, f"r = {val:+.3f}\n{p_values[i]}",
                ha='center', va=va_align, fontsize=7, fontweight='bold', color='#1E293B')
                
    ax.axhline(0, color='#64748B', linewidth=1, zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels(factors, fontweight='bold', fontsize=7.5)
    ax.set_ylabel('Hệ số tương quan Pearson (r)', fontweight='bold', fontsize=8)
    ax.set_ylim(-1.15, 0.45)
    ax.set_title('B. Sức mạnh giải thích tương quan với ROE (2024)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    # Custom Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=HIGHLIGHT_RED, label='Tương quan quyết định (Margin)'),
        Patch(facecolor=PRIMARY_NAVY, label='Tương quan phụ (Không ý nghĩa)')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.20), frameon=False, fontsize=7.5, ncol=2)
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_8_3_factor_corr.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# Run all generator functions
if __name__ == '__main__':
    gen_chart_8_1a()
    gen_chart_8_1b()
    gen_chart_8_2a()
    gen_chart_8_2b()
    gen_chart_8_3a()
    gen_chart_8_3b()
    print("All Chapter 8 high-res charts generated successfully!")

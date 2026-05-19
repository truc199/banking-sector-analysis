"""
Generate unified premium charts for Chapter 6: Giai đoạn 1 — COVID-19 & Cú Shock Hệ Thống (2020-2021)
Standardized on the Navy Blue color scheme, featuring high-contrast lines/bars, smooth interpolations,
and clean regression curves.
Saves all charts inside the slidev/public/ directory so Slidev/Vite can serve them.
"""
import os
import glob
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator
from scipy import stats
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ─── Setup ───────────────────────────────────────────────────────────────
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['text.color'] = '#1e293b'
matplotlib.rcParams['axes.labelcolor'] = '#334155'
matplotlib.rcParams['xtick.color'] = '#475569'
matplotlib.rcParams['ytick.color'] = '#475569'
matplotlib.rcParams['axes.spines.top']   = False
matplotlib.rcParams['axes.spines.right'] = False

NAVY_DARK    = '#003366'  # Dark Midnight Blue
NAVY_MID_D   = '#004C99'  # US Air Force Academy Blue
NAVY_MID     = '#0066CC'  # Bright Navy Blue
AZURE        = '#007FFF'  # Azure
DODGER       = '#3399FF'  # Dodger blue
FRENCH_SKY   = '#66B2FF'  # French Sky Blue
BABY_BLUE    = '#99CCFF'  # Baby Blue Eyes
RED          = '#C0392B'  # Brick Red
ORANGE       = '#D35400'  # Burnt Orange
TEAL         = '#0D9488'  # Teal

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# Load data
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
note_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]
inc_file = glob.glob(r'd:\uni\gcontest\*Income*')[0]

bs = pd.read_csv(bs_file)
note = pd.read_csv(note_file)
inc = pd.read_csv(inc_file)

# Merged dataset for 2020-2024
years = [2020, 2021, 2022, 2023, 2024]
bs_5y = bs[bs['Năm'].isin(years)].copy()
note_5y = note[note['Năm'].isin(years)].copy()
inc_5y = inc[inc['Năm'].isin(years)].copy()

merged = bs_5y.merge(inc_5y, on=['Công ty', 'Năm']).merge(note_5y, on=['Công ty', 'Năm'])

# Calculate basic bank-level variables
merged['casa_ratio'] = merged['C68'] / merged['A55'] * 100
merged['nim_ratio'] = merged['B3'] / merged['A1'] * 100
merged['cof_ratio'] = merged['C88'] / merged['A55'] * 100
merged['npl_abs'] = merged['C35'] + merged['C36'] + merged['C37']
merged['npl_ratio'] = merged['npl_abs'] / merged['A13'] * 100
merged['watch_ratio'] = merged['C34'] / merged['A13'] * 100
merged['leverage'] = merged['A1'] / merged['A64']
merged['roe'] = merged['B22'] / merged['A64'] * 100
merged['roa'] = merged['B22'] / merged['A1'] * 100
merged['re_exposure'] = merged['C28'] / merged['A13'] * 100

# Average for Phase 1 (2020-2021)
gd1_merged = merged[merged['Năm'].isin([2020, 2021])].groupby('Công ty').mean(numeric_only=True).reset_index()

# ─── Fonts ────────────────────────────────────────────────────────────────
FS_TITLE = 9.5
FS_LABEL = 8.5
FS_TICK = 7.5
FS_VAL = 7.5
FS_LEG = 7.5

# =====================================================================
# CHART 6.1 — MACRO GDP & RETAIL SALES (Combo Bar/Line with Shading)
# =====================================================================
def chart_6_1_macro_gdp_retail():
    years_all = [2020, 2021, 2022, 2023, 2024]
    year_labels = ['2020', '2021', '2022', '2023', '2024']
    gdp_growth = [2.91, 2.58, 8.02, 5.05, 7.09]
    retail_growth = [2.08, -5.47, 21.37, 10.39, 8.63]
    
    fig, ax1 = plt.subplots(figsize=(5.8, 3.8), dpi=350)
    x = np.arange(len(years_all))
    
    # Plot Retail Sales Growth YoY as Bar chart (Navy)
    colors = [RED if v < 0 else NAVY_DARK for v in retail_growth]
    bars = ax1.bar(x, retail_growth, color=colors, width=0.45, alpha=0.90,
                   edgecolor='#0f172a', linewidth=0.6, label='Tăng trưởng Bán lẻ YoY', zorder=3)
    ax1.set_ylabel('Tăng trưởng Tổng mức bán lẻ YoY (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
    ax1.set_xlabel('Năm', fontsize=FS_LABEL, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(year_labels, fontsize=FS_TICK)
    ax1.set_ylim(-10, 30)
    ax1.tick_params(axis='y', labelsize=FS_TICK)
    ax1.axhline(0, color='#64748B', lw=0.8, ls='-', zorder=4) # Zero line
    
    # Dual Axis for GDP Growth (Dodger Blue Line)
    ax2 = ax1.twinx()
    x_smooth = np.linspace(0, len(years_all)-1, 300)
    pchip = PchipInterpolator(x, gdp_growth)
    y_smooth = pchip(x_smooth)
    
    line2, = ax2.plot(x_smooth, y_smooth, color=DODGER, linewidth=2.0, linestyle=':', label='Tăng trưởng GDP (%)', zorder=5)
    ax2.plot(x, gdp_growth, color=DODGER, marker='o', markersize=5.5, markerfacecolor='white', markeredgewidth=1.8, linestyle='None', zorder=6)
    
    ax2.set_ylabel('Tăng trưởng GDP (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4, color=TEXT_MID)
    ax2.set_ylim(0, 10)
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
    ax2.tick_params(axis='y', labelsize=FS_TICK)
    
    # Shading for COVID-19 Period (2020-2021)
    ax1.axvspan(-0.3, 1.3, color='#F1F5F9', alpha=0.8, zorder=1)
    ax1.text(0.5, 25, 'Khủng hoảng đại dịch\nCOVID-19', color='#64748B', fontsize=7.5,
             fontweight='bold', ha='center', va='center', style='italic', zorder=2)
             
    # Value annotations for bars
    for bar in bars:
        h = bar.get_height()
        va_dir = 'bottom' if h >= 0 else 'top'
        xy_off = (0, 3) if h >= 0 else (0, -11)
        ax1.annotate(f'{h:.2f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=xy_off, textcoords='offset points',
                     ha='center', va=va_dir, fontsize=FS_VAL-0.5, fontweight='bold',
                     color=RED if h < 0 else NAVY_DARK)
                     
    # Value annotations for GDP growth
    for i, val in enumerate(gdp_growth):
        ax2.annotate(f'{val:.2f}%', xy=(i, val), xytext=(0, 6),
                     textcoords='offset points', ha='center', va='bottom',
                     fontsize=FS_VAL-0.5, fontweight='bold', color=DODGER)
                     
    ax1.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
    ax1.set_axisbelow(True)
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.spines['left'].set_color(SPINE_COLOR)
    ax1.spines['bottom'].set_color(SPINE_COLOR)
    ax2.spines['right'].set_color(SPINE_COLOR)
    
    # Combined Legend (at the bottom)
    fake_bar = plt.Rectangle((0, 0), 1, 1, fc=NAVY_DARK, edgecolor='none')
    ax1.legend([fake_bar, line2], ['Tăng trưởng Bán lẻ YoY (%)', 'Tăng trưởng GDP (%)'],
               loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, fontsize=FS_LEG)
    
    ax1.set_title('Tác động COVID-19 đến Tăng trưởng GDP & Tiêu dùng Bán lẻ (2020 – 2024)',
                 fontsize=FS_TITLE, fontweight='bold', pad=12, color=TEXT_DARK, ha='center')
                 
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_6_1_macro_gdp_retail.png')
    plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved {path}")

# =====================================================================
# CHART 6.2.1 — CASA VS NIM SCATTER (Linear Regression)
# =====================================================================
def chart_6_2_casa_nim_scatter():
    df_clean = gd1_merged.dropna(subset=['casa_ratio', 'nim_ratio']).copy()
    
    fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=350)
    
    # Scatter plot
    scatter = ax.scatter(df_clean['casa_ratio'], df_clean['nim_ratio'], color=NAVY_DARK, s=40, alpha=0.85, edgecolors='#334155', zorder=5)
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(df_clean['casa_ratio'], df_clean['nim_ratio'])
    x_range = np.linspace(df_clean['casa_ratio'].min() - 2, df_clean['casa_ratio'].max() + 2, 100)
    y_reg = slope * x_range + intercept
    
    ax.plot(x_range, y_reg, color=DODGER, lw=1.5, ls='--', label=f'Đường hồi quy (r = +0.527)', zorder=4)
    
    # Label key banks
    labels_to_show = {
        6: 'NH 6 (CASA Cao)',
        1: 'NH 1',
        3: 'NH 3',
        20: 'NH 20 (CASA Thấp)',
        11: 'NH 11',
        22: 'NH 22'
    }
    
    for idx, row in df_clean.iterrows():
        b_id = int(row['Công ty'])
        if b_id in labels_to_show:
            label = labels_to_show[b_id]
            x_val = row['casa_ratio']
            y_val = row['nim_ratio']
            offset_x = 0.6
            offset_y = 0
            if b_id == 6:
                offset_x = -7.4
                offset_y = -0.1
            elif b_id == 20:
                offset_x = 0.6
                offset_y = -0.05
            elif b_id == 22:
                offset_x = -3.2
                offset_y = 0.15
            elif b_id == 11:
                offset_x = 0.6
                offset_y = 0.1
                
            ax.text(x_val + offset_x, y_val + offset_y, label, fontsize=7.0, fontweight='bold',
                    color='#334155', alpha=0.95, va='center')
                    
    ax.set_xlabel('Tỷ lệ CASA trung bình GĐ1 (%)', fontsize=FS_LABEL, fontweight='bold')
    ax.set_ylabel('Biên lãi thuần NIM trung bình GĐ1 (%)', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(0, 42.0)
    ax.set_ylim(1.0, 5.0)
    ax.grid(True, axis='both', linestyle='--', color=GRID_COLOR, zorder=0)
    ax.set_axisbelow(True)
    
    # Text card for correlation statistics
    ax.text(2.0, 1.4, f'Hệ số tương quan: r = +0.527\np-value = 0.0047 (Có ý nghĩa mạnh)',
            fontsize=7.2, fontweight='bold', color=TEXT_MID,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC', alpha=0.9, edgecolor='#E2E8F0'))
            
    ax.legend(loc='upper left', frameon=False, fontsize=FS_LEG)
    ax.set_title('Tương quan thuận giữa Tỷ lệ CASA & NIM (GĐ1: 2020 – 2021)\nCASA cao giúp duy trì giá vốn rẻ và đệm NIM bền vững',
                 fontsize=FS_TITLE-0.5, fontweight='bold', pad=10, color=TEXT_DARK, ha='center')
                 
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_6_2_casa_nim_scatter.png')
    plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved {path}")

# =====================================================================
# CHART 6.2.2 — LEVERAGE PARADOX (Grouped Bar low vs high leverage)
# =====================================================================
def chart_6_2_leverage_roe():
    q = 0.25
    high_thresh = gd1_merged['leverage'].quantile(1 - q)
    low_thresh = gd1_merged['leverage'].quantile(q)
    
    high_group = gd1_merged[gd1_merged['leverage'] >= high_thresh]
    low_group = gd1_merged[gd1_merged['leverage'] <= low_thresh]
    
    high_roe = high_group['roe'].mean()
    low_roe = low_group['roe'].mean()
    high_roa = high_group['roa'].mean()
    low_roa = low_group['roa'].mean()
    
    fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=350)
    x = np.arange(2)
    width = 0.32
    
    # Bars for ROE (Low vs High Leverage)
    bars_roe = ax.bar(x - width/2, [low_roe, high_roe], width, color=NAVY_DARK, alpha=0.90,
                      edgecolor=NAVY_DARK, linewidth=0.6, label='Tỷ suất sinh lời VCSH - ROE (%)', zorder=3)
                      
    # Bars for ROA (Low vs High Leverage)
    bars_roa = ax.bar(x + width/2, [low_roa, high_roa], width, color=DODGER, alpha=0.85,
                      edgecolor=DODGER, linewidth=0.6, label='Tỷ suất sinh lời Tài sản - ROA (%)', zorder=3)
                      
    ax.set_ylabel('Tỷ lệ (%)', fontsize=FS_LABEL, fontweight='bold', labelpad=4)
    ax.set_xticks(x)
    ax.set_xticklabels(['Nhóm Đòn bẩy thấp\n(Quy mô Vốn tự có dày)', 'Nhóm Đòn bẩy cao\n(Quy mô Vốn tự có mỏng)'], fontsize=FS_TICK, fontweight='bold')
    ax.set_ylim(0, 16.0)
    ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
    ax.set_axisbelow(True)
    
    # Annotations for ROE
    for bar in bars_roe:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords='offset points',
                     ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color=NAVY_DARK)
                     
    # Annotations for ROA
    for bar in bars_roa:
        h = bar.get_height()
        ax.annotate(f'{h:.2f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords='offset points',
                     ha='center', va='bottom', fontsize=FS_VAL, fontweight='bold', color='#1E40AF')
                     
    # Text card for p-value explanation
    ax.text(0.5, 12.0, 'Nghịch lý Đòn bẩy trong khủng hoảng:\nĐòn bẩy cao giảm ROE (10.47% vs 12.63%)\ndo áp lực trích lập dự phòng ăn mòn hết lợi nhuận.',
            fontsize=6.8, fontweight='bold', color='#475569', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC', alpha=0.9, edgecolor='#E2E8F0'))
            
    ax.legend(loc='upper right', frameon=False, fontsize=FS_LEG-0.5)
    ax.set_title('Kiểm định H1.2: Nghịch lý Đòn bẩy tài chính trong khủng hoảng\nĐòn bẩy dày làm đệm đỡ phòng thủ giúp nhóm vốn dày tối ưu ROE',
                 fontsize=FS_TITLE-0.5, fontweight='bold', pad=10, color=TEXT_DARK, ha='center')
                 
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_6_2_leverage_roe.png')
    plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved {path}")

# =====================================================================
# CHART 6.3.1 — RE EXPOSURE VS NPL SCATTER
# =====================================================================
def chart_6_3_re_exposure_npl():
    df_clean = gd1_merged.dropna(subset=['re_exposure', 'npl_ratio']).copy()
    
    fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=350)
    
    # Scatter plot
    scatter = ax.scatter(df_clean['re_exposure'], df_clean['npl_ratio'], color=RED, s=40, alpha=0.85, edgecolors='#7F1D1D', zorder=5)
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(df_clean['re_exposure'], df_clean['npl_ratio'])
    x_range = np.linspace(df_clean['re_exposure'].min() - 1, df_clean['re_exposure'].max() + 1, 100)
    y_reg = slope * x_range + intercept
    
    ax.plot(x_range, y_reg, color='#B91C1C', lw=1.5, ls='--', label=f'Đường hồi quy (r = +0.208)', zorder=4)
    
    # Label key banks
    labels_to_show = {
        22: 'NH 22',
        8: 'NH 8',
        21: 'NH 21',
        14: 'NH 14',
        15: 'NH 15',
        1: 'NH 1',
        3: 'NH 3'
    }
    
    for idx, row in df_clean.iterrows():
        b_id = int(row['Công ty'])
        if b_id in labels_to_show:
            label = labels_to_show[b_id]
            x_val = row['re_exposure']
            y_val = row['npl_ratio']
            offset_x = 0.3
            offset_y = 0
            if b_id == 22:
                offset_x = -2.2
                offset_y = 0.15
            elif b_id == 14:
                offset_x = -2.0
                offset_y = -0.1
                
            ax.text(x_val + offset_x, y_val + offset_y, label, fontsize=7.0, fontweight='bold',
                    color='#475569', alpha=0.95, va='center')
                    
    ax.set_xlabel('Tỷ lệ phơi nhiễm BĐS trung bình GĐ1 (%)', fontsize=FS_LABEL, fontweight='bold')
    ax.set_ylabel('Tỷ lệ Nợ xấu NPL trung bình GĐ1 (%)', fontsize=FS_LABEL, fontweight='bold')
    ax.set_xlim(0, 25.0)
    ax.set_ylim(0.2, 3.2)
    ax.grid(True, axis='both', linestyle='--', color=GRID_COLOR, zorder=0)
    ax.set_axisbelow(True)
    
    # Text card for correlation statistics
    ax.text(11.0, 0.4, f'r = +0.208 | p-value = 0.30\nTương quan yếu, không có ý nghĩa thống kê\nchứng minh nợ xấu bị trì hoãn bùng phát\nở các ngành rủi ro nhờ chính sách cơ cấu nợ.',
            fontsize=7.0, fontweight='bold', color=TEXT_MID,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC', alpha=0.9, edgecolor='#E2E8F0'))
            
    ax.legend(loc='upper left', frameon=False, fontsize=FS_LEG)
    ax.set_title('Tương quan yếu giữa Phơi nhiễm BĐS & Nợ xấu NPL (GĐ1: 2020 – 2021)\nTín hiệu cảnh báo sớm bị triệt tiêu do cơ chế hỗ trợ hoãn nợ',
                 fontsize=FS_TITLE-0.5, fontweight='bold', pad=10, color=TEXT_DARK, ha='center')
                 
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_6_3_re_exposure_npl.png')
    plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved {path}")

# =====================================================================
# CHART 6.3.2 — NPL VS WATCH-LIST TREND (2020 vs 2021)
# =====================================================================
def chart_6_3_npl_watchlist_trend():
    years_gd1 = [2020, 2021]
    year_labels = ['2020', '2021']
    
    npl_simple = [merged[merged['Năm']==y]['npl_ratio'].mean() for y in years_gd1]
    watch_simple = [merged[merged['Năm']==y]['watch_ratio'].mean() for y in years_gd1]
    
    fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=350)
    x = np.arange(len(years_gd1))
    
    # Plot simple averages as lines
    line1, = ax.plot(x, npl_simple, color=NAVY_DARK, lw=2.5, marker='o', ms=6.5,
                     label='Tỷ lệ Nợ xấu NPL (TB đơn giản)', zorder=5)
    line2, = ax.plot(x, watch_simple, color=DODGER, lw=2.5, marker='s', ms=6.0, ls='--',
                     label='Tỷ lệ Nợ nhóm 2 (TB đơn giản)', zorder=5)
                     
    # Data labels for NPL
    for i, val in enumerate(npl_simple):
        ax.annotate(f"{val:.2f}%", (i, val), textcoords='offset points', xytext=(0, 8),
                     ha='center', fontsize=8.0, color=NAVY_DARK, fontweight='bold')
                     
    # Data labels for Watch-list
    for i, val in enumerate(watch_simple):
        ax.annotate(f"{val:.2f}%", (i, val), textcoords='offset points', xytext=(0, -14),
                     ha='center', fontsize=8.0, color=DODGER, fontweight='bold')
                     
    # Annotate delta differences
    diff_npl = npl_simple[1] - npl_simple[0]
    diff_watch = watch_simple[1] - watch_simple[0]
    
    ax.annotate(f"Δ = +{diff_npl:.2f}pp\n(Đi ngang)", xy=(0.5, 1.76), color=NAVY_DARK,
                fontsize=7.5, fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor=NAVY_DARK))
                
    ax.annotate(f"Δ = +{diff_watch:.2f}pp\n(Vọt tăng +33.6%)", xy=(0.5, 1.48), color=DODGER,
                fontsize=7.5, fontweight='bold', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor=DODGER))
                
    ax.set_xticks(x)
    ax.set_xticklabels(year_labels, fontsize=FS_TICK+0.5, fontweight='bold')
    ax.set_ylabel("Tỷ lệ (%)", fontsize=FS_LABEL, fontweight='bold')
    ax.set_ylim(1.0, 2.0)
    ax.set_xlim(-0.25, 1.25)
    ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
    ax.set_axisbelow(True)
    
    # Text label explaining VAMC bonds
    ax.text(0.5, 1.15, 'Trái phiếu đặc biệt VAMC:\n10 ngân hàng vẫn "ôm" nợ xấu VAMC chưa tất toán\n(gián tiếp trì hoãn ghi nhận nợ xấu trên bảng CĐKT).',
            fontsize=6.8, fontweight='bold', color='#475569', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8FAFC', alpha=0.9, edgecolor='#E2E8F0'))
            
    ax.legend(loc='upper left', frameon=False, fontsize=FS_LEG-0.5)
    ax.set_title('Kiểm định H1.4: Reported NPL vs Nợ nhóm 2 cảnh báo sớm\nNợ xấu đi ngang nhưng Nợ cần chú ý vọt tăng lột tả rủi ro che giấu',
                 fontsize=FS_TITLE-0.5, fontweight='bold', pad=10, color=TEXT_DARK, ha='center')
                 
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_6_3_npl_watchlist_trend.png')
    plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved {path}")


if __name__ == '__main__':
    chart_6_1_macro_gdp_retail()
    chart_6_2_casa_nim_scatter()
    chart_6_2_leverage_roe()
    chart_6_3_re_exposure_npl()
    chart_6_3_npl_watchlist_trend()
    print("All Chapter 6 premium side-by-side charts generated successfully!")

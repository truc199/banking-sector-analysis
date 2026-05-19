"""
Generate Chapter 5 charts:
  slide_5_1_npl_watch_trend.png   – Line chart NPL and Watch-list (Group 2) simple average trend (2020-2024) + COVID-19 shading
  slide_5_2_npl_coverage_scatter.png – Scatter plot of NPL vs Coverage ratio (2024) divided into 4 safety quadrants
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator, FixedLocator
import glob, sys, os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.spines.top']   = False
matplotlib.rcParams['axes.spines.right'] = False

BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
INC_FILE  = glob.glob(r'd:\uni\gcontest\*Income*')[0]
OUT_DIR   = r'd:\uni\gcontest\slidev\public'

YEARS = [2020, 2021, 2022, 2023, 2024]

# Design Palette
NAVY   = '#003366'
BLUE1  = '#004C99'
BLUE2  = '#0066CC'
AZURE  = '#007FFF'
DODGER = '#3399FF'
SKY    = '#66B2FF'
BABY   = '#99CCFF'
RED    = '#C0392B'
ORANGE = '#D35400'
TEAL   = '#0D9488'
GRAY   = '#94A3B8'

bs   = pd.read_csv(BS_FILE)
note = pd.read_csv(NOTE_FILE)
inc  = pd.read_csv(INC_FILE)

bs5   = bs  [bs  ['Năm'].isin(YEARS)].copy()
note5 = note[note['Năm'].isin(YEARS)].copy()
inc5  = inc [inc ['Năm'].isin(YEARS)].copy()

merged = bs5.merge(inc5, on=['Công ty','Năm']).merge(note5, on=['Công ty','Năm'])

# Calculate main metrics
merged['npl_abs'] = merged['C35'] + merged['C36'] + merged['C37']
merged['npl_ratio'] = merged['npl_abs'] / merged['C32'] * 100
merged['watch_ratio'] = merged['C34'] / merged['C32'] * 100
merged['coverage'] = abs(merged['A14']) / merged['npl_abs'] * 100

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5.1 – NPL & WATCH-LIST TREND
# ─────────────────────────────────────────────────────────────────────────────
def chart_npl_watch_trend():
    # Simple average per year
    npl_simple = merged.groupby('Năm')['npl_ratio'].mean()
    watch_simple = merged.groupby('Năm')['watch_ratio'].mean()
    
    # Weighted average per year
    npl_weighted = merged.groupby('Năm').apply(lambda d: d['npl_abs'].sum() / d['C32'].sum() * 100)
    watch_weighted = merged.groupby('Năm').apply(lambda d: d['C34'].sum() / d['C32'].sum() * 100)

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    
    xs = YEARS
    
    # Draw simple averages as primary lines
    line1, = ax.plot(xs, [npl_simple[y] for y in xs], color=NAVY, lw=2.4, marker='o', ms=6,
                     label='NPL (TB đơn giản)', zorder=5)
    line2, = ax.plot(xs, [watch_simple[y] for y in xs], color=DODGER, lw=2.0, marker='s', ms=5, ls='--',
                     label='Nợ nhóm 2 (TB đơn giản)', zorder=5)
    
    # Draw weighted averages as dotted reference lines
    line3, = ax.plot(xs, [npl_weighted[y] for y in xs], color=NAVY, lw=1.2, ls=':', alpha=0.7,
                     label='NPL (TB gia quyền)', zorder=4)
    line4, = ax.plot(xs, [watch_weighted[y] for y in xs], color=DODGER, lw=1.2, ls=':', alpha=0.7,
                     label='Nợ nhóm 2 (TB gia quyền)', zorder=4)

    # Shading for COVID period (2020-2021)
    ax.axvspan(2020, 2021, color='#F1F5F9', alpha=0.8, zorder=1)
    ax.text(2020.5, 0.4, 'GĐ Đại dịch\nCOVID-19', color='#64748B', fontsize=8,
            fontweight='bold', ha='center', va='center', style='italic', zorder=2)

    # Data Labels for NPL Simple Average
    for y in xs:
        ax.annotate(f"{npl_simple[y]:.2f}%", (y, npl_simple[y]),
                     textcoords='offset points', xytext=(0, 8),
                     ha='center', fontsize=8, color=NAVY, fontweight='bold')
        
    # Data Labels for Watch-list Simple Average
    for y in xs:
        ax.annotate(f"{watch_simple[y]:.2f}%", (y, watch_simple[y]),
                     textcoords='offset points', xytext=(0, -12),
                     ha='center', fontsize=8, color=DODGER, fontweight='bold')

    ax.set_xticks(YEARS)
    ax.set_xticklabels([str(y) for y in YEARS], fontsize=9)
    ax.set_ylabel("Tỷ lệ (%)", fontsize=9, color=NAVY)
    ax.set_xlabel("Năm", fontsize=9)
    ax.set_ylim(0, 3.8)
    ax.set_xlim(2019.7, 2024.3)
    ax.yaxis.set_minor_locator(MultipleLocator(0.2))
    
    ax.set_title("NPL & Nợ Cần Chú Ý (Nhóm 2) Toàn Hệ Thống (2020–2024)\nXu hướng bùng nổ có độ trễ hậu COVID-19",
                 fontsize=9.5, fontweight='bold', pad=8, color='#1E293B')

    ax.legend(handles=[line1, line2, line3, line4], loc='lower right', fontsize=7.5, framealpha=0.9)
    ax.grid(axis='y', ls='--', alpha=0.35, zorder=0)

    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_5_1_npl_watch_trend.png')
    fig.savefig(path, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5.2 – NPL VS COVERAGE SCATTER 2024 (4 QUADRANTS)
# ─────────────────────────────────────────────────────────────────────────────
def chart_npl_coverage_scatter():
    d24 = merged[merged['Năm']==2024].copy()
    d24 = d24.dropna(subset=['npl_ratio', 'coverage'])
    
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    
    # 4 Quadrants Thresholds
    npl_thresh = 3.0
    cov_thresh = 100.0
    
    # Color mapping per quadrant
    colors = []
    for idx, row in d24.iterrows():
        npl = row['npl_ratio']
        cov = row['coverage']
        if npl < npl_thresh and cov >= cov_thresh:
            colors.append(TEAL)    # Safe / Strong Buffer
        elif npl < npl_thresh and cov < cov_thresh:
            colors.append(DODGER)  # Low NPL but Thin Buffer
        elif npl >= npl_thresh and cov < cov_thresh:
            colors.append(RED)     # High Risk / Thin Buffer
        else:
            colors.append(NAVY)    # High NPL but High Buffer
            
    scatter = ax.scatter(d24['npl_ratio'], d24['coverage'], c=colors, s=55, alpha=0.85, edgecolors='#475569', zorder=5)
    
    # Draw quadrant lines
    ax.axvline(npl_thresh, color='#C0392B', lw=1.2, ls='--', alpha=0.7, zorder=3)
    ax.axhline(cov_thresh, color='#0F172A', lw=1.2, ls='--', alpha=0.7, zorder=3)
    
    # Text labels for quadrants
    ax.text(0.2, 180, 'QUẢN TRỊ AN TOÀN\n(NPL < 3% | Coverage ≥ 100%)', color='#0F766E', fontsize=6.8, fontweight='bold', va='center')
    ax.text(0.2, 35, 'ĐỆM DỰ PHÒNG MỎNG\n(NPL < 3% | Coverage < 100%)', color='#0369A1', fontsize=6.8, fontweight='bold', va='center')
    ax.text(3.5, 35, 'RỦI RO CỰC HẠN\n(NPL ≥ 3% | Coverage < 100%)', color='#991B1B', fontsize=6.8, fontweight='bold', va='center')
    ax.text(3.5, 180, 'RỦI RO / TRÍCH LẬP TỐT\n(NPL ≥ 3% | Coverage ≥ 100%)', color='#1E3A8A', fontsize=6.8, fontweight='bold', va='center')

    # Annotate key representative banks
    # NH 4, NH 2 (Stars)
    # NH 22, NH 8, NH 19, NH 14, NH 15, NH 21 (High Risk)
    annotations = {
        4: 'NH 4 (Star)',
        2: 'NH 2',
        22: 'NH 22 (Outlier)',
        8: 'NH 8',
        19: 'NH 19',
        14: 'NH 14',
        15: 'NH 15',
        21: 'NH 21',
        1: 'NH 1',
        3: 'NH 3',
        20: 'NH 20',
        11: 'NH 11'
    }
    
    for idx, row in d24.iterrows():
        b_id = int(row['Công ty'])
        if b_id in annotations:
            label = annotations[b_id]
            x_val = row['npl_ratio']
            y_val = row['coverage']
            # Offset adjustments for labels to avoid overlap
            offset_x = 0.25
            offset_y = 0
            if b_id == 22:
                offset_x = -3.8
                offset_y = 4
            elif b_id == 4:
                offset_x = 0.35
                offset_y = -3
            elif b_id == 2:
                offset_x = 0.3
                offset_y = -2
            elif b_id == 11:
                offset_x = -2.1
                offset_y = -4
            elif b_id == 14:
                offset_x = -2.0
                offset_y = 4
            elif b_id == 19:
                offset_x = 0.3
                offset_y = 4
            elif b_id == 8:
                offset_x = 0.3
                offset_y = -2
            elif b_id == 21:
                offset_x = 0.3
                offset_y = -3
            elif b_id == 15:
                offset_x = 0.3
                offset_y = 3
                
            ax.text(x_val + offset_x, y_val + offset_y, label, fontsize=6.8, fontweight='bold',
                    color='#334155', alpha=0.9, va='center')

    ax.set_xlabel("Tỷ lệ Nợ xấu - NPL (%)", fontsize=9)
    ax.set_ylabel("Tỷ lệ Bao phủ Nợ xấu - Coverage (%)", fontsize=9)
    ax.set_xlim(0, 21.0)
    ax.set_ylim(0, 240)
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(20))
    
    ax.set_title("Bản Đồ Phân Hóa Sức Khỏe Tài Sản Hệ Thống (2024)\nĐệm vốn dự phòng suy yếu trước áp lực nợ xấu gia tăng",
                 fontsize=9.5, fontweight='bold', pad=8, color='#1E293B')
    
    # Legend
    legend_patches = [
        mpatches.Patch(color=TEAL,   label='Quản trị an toàn (NPL < 3% & Coverage ≥ 100%)'),
        mpatches.Patch(color=DODGER, label='Low NPL / Đệm mỏng (NPL < 3% & Coverage < 100%)'),
        mpatches.Patch(color=RED,    label='Rủi ro cực hạn (NPL ≥ 3% & Coverage < 100%)'),
        plt.Line2D([0], [0], color='#C0392B', lw=1.2, ls='--', label='Warning NPL = 3.0%'),
        plt.Line2D([0], [0], color='#0F172A', lw=1.2, ls='--', label='Warning Coverage = 100.0%'),
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=6.8, framealpha=0.9)
    ax.grid(axis='both', ls='--', alpha=0.25, zorder=0)

    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_5_2_npl_coverage_scatter.png')
    fig.savefig(path, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path}")


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    chart_npl_watch_trend()
    chart_npl_coverage_scatter()
    print("All Chapter 5 charts generated successfully.")

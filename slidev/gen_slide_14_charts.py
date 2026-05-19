import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob
import os

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
matplotlib.rcParams['axes.spines.top']   = False
matplotlib.rcParams['axes.spines.right'] = False

# Find files
BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
OUT_DIR   = r'd:\uni\gcontest\slidev\public'

# Load data
bs = pd.read_csv(BS_FILE)
note = pd.read_csv(NOTE_FILE)

# Merge
m = bs.merge(note, on=['Công ty', 'Năm'], how='inner')

# Palette
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

# -----------------------------------------------------------------------------
# CHART A: CASA Ranking 2024 with Inset Industry Trend
# -----------------------------------------------------------------------------
def generate_chart_a():
    dep_cols = ['C68', 'C69', 'C70', 'C71', 'C72']
    
    # Pre-calculate for all years to get weighted average trend
    m_all = m.copy()
    m_all['total_dep'] = m_all[dep_cols].sum(axis=1)
    
    # Calculate CASA for 2024
    m24 = m_all[m_all['Năm'] == 2024].copy()
    m24['CASA'] = (m24['C68'] / m24['total_dep']) * 100
    m24 = m24.sort_values('CASA', ascending=True).reset_index(drop=True)
    
    n_banks = len(m24)
    wt_avg_24 = (m24['C68'].sum() / m24['total_dep'].sum()) * 100
    sm_avg_24 = m24['CASA'].mean()
    
    # Calculate weighted average trend for years 2020-2024
    years = [2020, 2021, 2022, 2023, 2024]
    trend_wt = []
    for y in years:
        my = m_all[m_all['Năm'] == y]
        trend_wt.append((my['C68'].sum() / my['total_dep'].sum()) * 100)
        
    fig, ax = plt.subplots(figsize=(6.2, 6.6), dpi=200)
    
    # Color mapping
    colors = [DODGER if v >= wt_avg_24 else BABY for v in m24['CASA']]
    # Top 3 highlight
    for i in range(n_banks - 3, n_banks):
        colors[i] = NAVY
        
    bars = ax.barh(range(n_banks), m24['CASA'], color=colors, height=0.7, zorder=3)
    
    # Add value labels
    for i, v in enumerate(m24['CASA']):
        ax.text(v + 0.4, i, f"{v:.1f}%", va='center', fontsize=6.8, 
                color=NAVY if v >= wt_avg_24 else '#444', fontweight='bold' if v >= wt_avg_24 else 'normal')
        
    # Vertical average lines
    ax.axvline(sm_avg_24, color=RED, lw=1.2, ls='--', zorder=4)
    ax.axvline(wt_avg_24, color=ORANGE, lw=1.2, ls=':', zorder=4)
    
    ax.set_yticks(range(n_banks))
    ax.set_yticklabels([f"NH {int(r)}" for r in m24['Công ty']], fontsize=7.2, fontweight='bold')
    ax.set_xlabel("Tỷ lệ CASA (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_title("A. Xếp hạng Tỷ lệ CASA năm 2024\n(So sánh chi tiết 27 ngân hàng Việt Nam)", 
                 fontsize=9.5, fontweight='bold', pad=10, color='#1E293B')
    
    ax.grid(axis='x', which='major', ls='--', alpha=0.3, zorder=0)
    ax.set_xlim(0, 45)
    
    # Add Inset for Trend (Industry Weighted Average Trend)
    ax_inset = ax.inset_axes([0.52, 0.12, 0.44, 0.28])
    ax_inset.plot(years, trend_wt, color=NAVY, lw=2, marker='o', ms=4, label='Trend gia quyền', zorder=5)
    
    # Value labels for inset
    for x, y in zip(years, trend_wt):
        ax_inset.annotate(f"{y:.1f}%", (x, y), textcoords='offset points', xytext=(0, 5),
                          ha='center', fontsize=6.8, color=NAVY, fontweight='bold')
        
    ax_inset.set_title("Xu hướng CASA toàn ngành (2020-2024)", fontsize=7, fontweight='bold', color='#1E293B')
    ax_inset.set_xticks(years)
    ax_inset.set_xticklabels([str(y) for y in years], fontsize=6.5)
    ax_inset.tick_params(axis='y', labelsize=6.5)
    ax_inset.set_ylim(14, 23)
    ax_inset.grid(axis='y', ls='--', alpha=0.25)
    
    # Legend for Main Chart
    patches = [
        mpatches.Patch(color=NAVY,   label='Top 3 (CASA ≥ 35%)'),
        mpatches.Patch(color=DODGER, label=f'Trên TB gia quyền (>{wt_avg_24:.1f}%)'),
        mpatches.Patch(color=BABY,   label='Dưới TB gia quyền'),
        plt.Line2D([0],[0], color=RED,    lw=1.2, ls='--', label=f'Mean đơn giản ({sm_avg_24:.1f}%)'),
        plt.Line2D([0],[0], color=ORANGE, lw=1.2, ls=':',  label=f'Mean gia quyền ({wt_avg_24:.1f}%)'),
    ]
    ax.legend(handles=patches, loc='lower right', fontsize=6.5, framealpha=0.9, bbox_to_anchor=(0.98, 0.43))
    
    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_14_casa_ranked.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path} successfully!")

# -----------------------------------------------------------------------------
# CHART B: Scatter Plot LDR vs GTCG/DEP (Warning Zones)
# -----------------------------------------------------------------------------
def generate_chart_b():
    m24 = m[m['Năm'] == 2024].copy()
    m24['LDR'] = (m24['A13'] / m24['A55']) * 100
    m24['GTCG_DEP'] = (m24['A58'] / m24['A55']) * 100
    
    fig, ax = plt.subplots(figsize=(6.2, 6.6), dpi=200)
    
    # Scatter points - s=32 for smaller markers as requested
    colors = []
    for idx, r in m24.iterrows():
        if r['LDR'] > 100 and r['GTCG_DEP'] > 5:
            colors.append(RED)
        elif r['LDR'] > 100:
            colors.append(ORANGE)
        elif r['GTCG_DEP'] > 5:
            colors.append('#E67E22') # Amber
        else:
            colors.append(TEAL)
            
    ax.scatter(m24['LDR'], m24['GTCG_DEP'], color=colors, s=32, edgecolor='black', linewidth=0.4, zorder=5)
    
    # Add labels for each bank - just the number (no "NH" prefix) as requested
    for idx, r in m24.iterrows():
        ax.annotate(str(int(r['Công ty'])), (r['LDR'], r['GTCG_DEP']), xytext=(2.5, 2.5), 
                    textcoords='offset points', fontsize=6.8, color='#1E293B', fontweight='bold', alpha=0.9)
        
    # Draw limits
    ax.axvline(100, color=RED, lw=1.2, ls='--', zorder=3, alpha=0.8)
    ax.axhline(5, color=ORANGE, lw=1.2, ls='--', zorder=3, alpha=0.8)
    
    # Highlight zones with shading
    # Quadrant Top-Right: LDR > 100% & GTCG/DEP > 5%
    ax.fill_between([100, 150], 5, 35, color=RED, alpha=0.06, label='Vùng Căng thẳng (LDR > 100% & GTCG > 5%)')
    # Quadrant Bottom-Right: LDR > 100% & GTCG/DEP <= 5%
    ax.fill_between([100, 150], 0, 5, color=ORANGE, alpha=0.06, label='Vùng Thanh khoản Mỏng (LDR > 100%)')
    # Quadrant Top-Left: LDR <= 100% & GTCG/DEP > 5%
    ax.fill_between([60, 100], 5, 35, color='#E67E22', alpha=0.04, label='Vùng Chi phí vốn Cao (GTCG > 5%)')
    # Quadrant Bottom-Left: LDR <= 100% & GTCG/DEP <= 5%
    ax.fill_between([60, 100], 0, 5, color=TEAL, alpha=0.06, label='Vùng An toàn (LDR ≤ 100% & GTCG ≤ 5%)')
    
    ax.set_xlabel("Tỷ lệ LDR (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_ylabel("Tỷ lệ GTCG / Tiền gửi (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_title("B. Bản đồ LDR vs Tỷ lệ GTCG / Tiền gửi 2024\n(Phân vùng cảnh báo Rủi ro Thanh khoản & Kỳ hạn)", 
                 fontsize=9.5, fontweight='bold', pad=10, color='#1E293B')
    
    ax.set_xlim(60, 150)
    ax.set_ylim(0, 35)
    
    ax.grid(True, ls='--', alpha=0.25, zorder=0)
    
    # Legend
    handles, labels_leg = ax.get_legend_handles_labels()
    # Unique labels
    by_label = dict(zip(labels_leg, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=6.8, framealpha=0.9)
    
    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_14_ldr_gtcg_scatter.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path} successfully!")

if __name__ == '__main__':
    generate_chart_a()
    generate_chart_b()
    print("All Slide 14 charts generated successfully!")

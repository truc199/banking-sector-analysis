import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.spines.top']   = False
matplotlib.rcParams['axes.spines.right'] = False

# Find files
BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
IS_FILE   = glob.glob(r'd:\uni\gcontest\*Income*')[0]
NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
OUT_DIR   = r'd:\uni\gcontest\slidev\public'

# Load data
bs = pd.read_csv(BS_FILE)
ic = pd.read_csv(IS_FILE)
note = pd.read_csv(NOTE_FILE)

# Merge
m = bs.merge(ic, on=['Công ty', 'Năm'], how='inner')
m = m.merge(note, on=['Công ty', 'Năm'], how='inner')

for c in m.columns:
    if c not in ['Công ty', 'Năm']:
        m[c] = pd.to_numeric(m[c], errors='coerce')

# Filter 2024
m24 = m[m['Năm'] == 2024].copy()
npl_sum = m24[['C35','C36','C37']].sum(axis=1)
m24['NPL'] = (npl_sum / m24['A13']) * 100
m24['LLR'] = (m24['A14'].abs() / npl_sum) * 100
m24['Fee_TOI'] = (m24['B6'] / m24['B14']) * 100

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
# CHART A: Scatter Plot NPL vs LLR Coverage
# -----------------------------------------------------------------------------
def generate_chart_a():
    fig, ax = plt.subplots(figsize=(6.2, 6.6), dpi=200)
    
    # Classify colors
    colors = []
    for idx, r in m24.iterrows():
        if r['NPL'] >= 3 and r['LLR'] < 100:
            colors.append(RED)
        elif r['NPL'] < 3 and r['LLR'] < 100:
            colors.append('#E67E22') # Orange/Amber
        elif r['NPL'] < 3 and r['LLR'] >= 100:
            colors.append(TEAL)
        else:
            colors.append(NAVY)
            
    # Scatter points - s=32 for small markers as requested
    ax.scatter(m24['NPL'], m24['LLR'], color=colors, s=32, edgecolor='black', linewidth=0.4, zorder=5)
    
    # Labels containing just raw bank numbers as requested
    for idx, r in m24.iterrows():
        # Fine-tune annotation positioning to avoid overlay
        x_off, y_off = 2.5, 2.5
        if int(r['Công ty']) == 4:
            x_off, y_off = -14, -10
        elif int(r['Công ty']) == 2:
            x_off, y_off = 3, -10
        elif int(r['Công ty']) == 22:
            x_off, y_off = -14, 5
            
        ax.annotate(str(int(r['Công ty'])), (r['NPL'], r['LLR']), xytext=(x_off, y_off), 
                    textcoords='offset points', fontsize=6.8, color='#1E293B', fontweight='bold', alpha=0.9)
        
    # Draw reference thresholds
    ax.axvline(3.0, color='#64748B', lw=1.2, ls='--', zorder=3, alpha=0.8)
    ax.axhline(100.0, color='#64748B', lw=1.2, ls='--', zorder=3, alpha=0.8)
    
    # Quadrant Shading
    ax.fill_between([0, 3], 100, 240, color=TEAL, alpha=0.06, label='Quản trị An toàn (NPL < 3% & LLR ≥ 100%)')
    ax.fill_between([0, 3], 0, 100, color='#E67E22', alpha=0.06, label='Đệm Dự phòng Mỏng (NPL < 3% & LLR < 100%)')
    ax.fill_between([3, 21], 0, 100, color=RED, alpha=0.06, label='Rủi ro Cực hạn (NPL ≥ 3% & LLR < 100%)')
    ax.fill_between([3, 21], 100, 240, color=NAVY, alpha=0.04, label='Rủi ro / Trích lập Tốt (NPL ≥ 3% & LLR ≥ 100%)')
    
    ax.set_xlabel("Tỷ lệ Nợ xấu NPL (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_ylabel("Tỷ lệ Bao phủ Nợ xấu LLR Coverage (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_title("A. Bản đồ Tương quan NPL vs LLR Coverage 2024\n(Phân vùng cảnh báo Kỷ luật Trích lập dự phòng)", 
                 fontsize=9.5, fontweight='bold', pad=10, color='#1E293B')
    
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 240)
    ax.grid(True, ls='--', alpha=0.25, zorder=0)
    
    # Legend at the bottom
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=6.8, framealpha=0.9)
    
    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_15_npl_coverage_scatter.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path} successfully!")

# -----------------------------------------------------------------------------
# CHART B: Ranked Fee / TOI Horizontal Bar Chart
# -----------------------------------------------------------------------------
def generate_chart_b():
    m24_sorted = m24.sort_values('Fee_TOI', ascending=True).reset_index(drop=True)
    n_banks = len(m24_sorted)
    
    fig, ax = plt.subplots(figsize=(6.2, 6.6), dpi=200)
    
    wt_avg = (m24['B6'].sum() / m24['B14'].sum()) * 100
    sm_avg = m24['Fee_TOI'].mean()
    
    # Color mapping
    colors = []
    for idx, r in m24_sorted.iterrows():
        if r['Fee_TOI'] < 0:
            colors.append(RED) # Negative highlight
        elif r['Fee_TOI'] >= wt_avg:
            colors.append(DODGER)
        else:
            colors.append(BABY)
            
    # Highlight top 3
    for i in range(n_banks - 3, n_banks):
        if m24_sorted.loc[i, 'Fee_TOI'] > 0:
            colors[i] = NAVY
            
    bars = ax.barh(range(n_banks), m24_sorted['Fee_TOI'], color=colors, height=0.7, zorder=3)
    
    # Add value labels
    for i, v in enumerate(m24_sorted['Fee_TOI']):
        if v >= 0:
            ax.text(v + 0.25, i, f"{v:.1f}%", va='center', fontsize=6.8, 
                    color=NAVY if v >= wt_avg else '#444', fontweight='bold' if v >= wt_avg else 'normal')
        else:
            ax.text(v - 1.8, i, f"{v:.1f}%", va='center', fontsize=6.8, 
                    color=RED, fontweight='bold')
            
    # Reference lines
    ax.axvline(sm_avg, color=RED, lw=1.2, ls='--', zorder=4)
    ax.axvline(wt_avg, color=ORANGE, lw=1.2, ls=':', zorder=4)
    
    ax.set_yticks(range(n_banks))
    ax.set_yticklabels([f"NH {int(r)}" for r in m24_sorted['Công ty']], fontsize=7.2, fontweight='bold')
    ax.set_xlabel("Tỷ lệ Fee Income / TOI (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_title("B. Xếp hạng Tỷ lệ Fee Income / TOI năm 2024\n(Mức độ đa dạng hóa nguồn thu ngoài tín dụng)", 
                 fontsize=9.5, fontweight='bold', pad=10, color='#1E293B')
    
    ax.grid(axis='x', which='major', ls='--', alpha=0.3, zorder=0)
    ax.set_xlim(-8, 22)
    
    # Legend
    patches = [
        mpatches.Patch(color=NAVY,   label='Top 3 Dẫn đầu'),
        mpatches.Patch(color=DODGER, label=f'Trên TB gia quyền (>{wt_avg:.1f}%)'),
        mpatches.Patch(color=BABY,   label='Dưới TB gia quyền'),
        mpatches.Patch(color=RED,    label='Tỷ lệ Âm (NH 22)'),
        plt.Line2D([0],[0], color=RED,    lw=1.2, ls='--', label=f'Mean đơn giản ({sm_avg:.1f}%)'),
        plt.Line2D([0],[0], color=ORANGE, lw=1.2, ls=':',  label=f'Mean gia quyền ({wt_avg:.1f}%)'),
    ]
    ax.legend(handles=patches, loc='lower right', fontsize=6.8, framealpha=0.9)
    
    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_15_fee_toi_ranked.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path} successfully!")

if __name__ == '__main__':
    generate_chart_a()
    generate_chart_b()
    print("All Slide 15 charts generated successfully!")

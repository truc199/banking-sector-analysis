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
m24['equity_ratio'] = (m24['A64'] / m24['A1']) * 100
m24['ROE'] = (m24['B22'] / m24['A64']) * 100
m24['ROA'] = (m24['B22'] / m24['A1']) * 100
m24['Leverage'] = m24['A1'] / m24['A64']
m24['NPM'] = (m24['B22'] / m24['B14']) * 100

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
# CHART A: Ranked Equity Ratio (Horizontal Bar Chart)
# -----------------------------------------------------------------------------
def generate_chart_a():
    m24_sorted = m24.sort_values('equity_ratio', ascending=True).reset_index(drop=True)
    n_banks = len(m24_sorted)
    
    fig, ax = plt.subplots(figsize=(6.2, 6.6), dpi=200)
    
    # Color mapping
    colors = []
    for idx, r in m24_sorted.iterrows():
        if r['equity_ratio'] < 6.0:
            colors.append(RED) # High risk capital inadequacy
        elif r['equity_ratio'] < 8.0:
            colors.append(ORANGE) # Warning threshold
        elif r['equity_ratio'] >= 10.0:
            colors.append(NAVY) # Exceptionally well-capitalized
        else:
            colors.append(BABY)
            
    bars = ax.barh(range(n_banks), m24_sorted['equity_ratio'], color=colors, height=0.7, zorder=3)
    
    # Add value labels
    for i, v in enumerate(m24_sorted['equity_ratio']):
        ax.text(v + 0.2, i, f"{v:.1f}%", va='center', fontsize=6.8, 
                color=RED if v < 6.0 else (NAVY if v >= 10.0 else '#444'), 
                fontweight='bold' if (v < 6.0 or v >= 10.0) else 'normal')
        
    # Standard threshold lines
    ax.axvline(6.0, color=RED, lw=1.2, ls='--', zorder=4)
    ax.axvline(8.0, color=ORANGE, lw=1.2, ls=':', zorder=4)
    
    ax.set_yticks(range(n_banks))
    ax.set_yticklabels([f"NH {int(r)}" for r in m24_sorted['Công ty']], fontsize=7.2, fontweight='bold')
    ax.set_xlabel("Đệm vốn Equity Ratio (VCSH / TTS) (%)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax.set_title("A. Xếp hạng Tỷ lệ Đệm Vốn Equity Ratio 2024\n(Cảnh báo an toàn hệ thống & Rủi ro mỏng vốn)", 
                 fontsize=9.5, fontweight='bold', pad=10, color='#1E293B')
    
    ax.grid(axis='x', which='major', ls='--', alpha=0.3, zorder=0)
    ax.set_xlim(0, 18)
    
    # Legend
    patches = [
        mpatches.Patch(color=NAVY,   label='Đệm vốn Dày dặn (≥ 10%)'),
        mpatches.Patch(color=BABY,   label='Mức bình thường'),
        mpatches.Patch(color=ORANGE, label='Warning (6% - 8%)'),
        mpatches.Patch(color=RED,    label='Rủi ro cực mỏng (< 6%)'),
        plt.Line2D([0],[0], color=RED,    lw=1.2, ls='--', label='Basel Min = 6.0%'),
        plt.Line2D([0],[0], color=ORANGE, lw=1.2, ls=':',  label='Basel Target = 8.0%'),
    ]
    ax.legend(handles=patches, loc='lower right', fontsize=6.8, framealpha=0.9)
    
    fig.tight_layout(pad=0.8)
    path = os.path.join(OUT_DIR, 'slide_16_equity_ratio_ranked.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path} successfully!")

# -----------------------------------------------------------------------------
# CHART B: DuPont ROE Driver Analysis (Top 5 vs Bottom 5)
# -----------------------------------------------------------------------------
def generate_chart_b():
    # Sort and exclude NH 22 due to extreme anomaly (negative equity / massive credit loss)
    # in order to maintain a legible operational scale for healthy banks
    m24_clean = m24[m24['Công ty'] != 22].copy()
    m24_sorted = m24_clean.sort_values('ROE', ascending=False).reset_index(drop=True)
    
    top5 = m24_sorted.head(5)
    bottom4 = m24_sorted.tail(4) # Excluded NH 22, so we take the bottom 4
    
    # Averages
    top5_avg = {
        'ROE': top5['ROE'].mean(),
        'ROA': top5['ROA'].mean(),
        'NPM': top5['NPM'].mean(),
        'Leverage': top5['Leverage'].mean()
    }
    bottom_avg = {
        'ROE': bottom4['ROE'].mean(),
        'ROA': bottom4['ROA'].mean(),
        'NPM': bottom4['NPM'].mean(),
        'Leverage': bottom4['Leverage'].mean()
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.2, 5.8), dpi=200)
    
    # Left Plot: Operational Efficiency (NPM vs ROA)
    categories = ['Top 5 (ROE dẫn đầu)', 'Bottom 4 (ROE thấp nhất)']
    x = np.arange(len(categories))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, [top5_avg['NPM'], bottom_avg['NPM']], width, label='Profit Margin (NPM)', color=NAVY, zorder=3)
    rects2 = ax1.bar(x + width/2, [top5_avg['ROA']*10, bottom_avg['ROA']*10], width, label='ROA x 10', color=TEAL, zorder=3)
    
    # Add values
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords='offset points', ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=NAVY)
                    
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f"{h/10:.2f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords='offset points', ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=TEAL)
                    
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=7.5, fontweight='bold')
    ax1.set_ylabel("Tỷ lệ (%)", fontsize=8.2, fontweight='bold')
    ax1.set_title("1. Biên Lợi Nhuận NPM & ROA\n(Động lực từ hiệu quả hoạt động)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax1.legend(loc='upper right', fontsize=6.8, framealpha=0.9)
    ax1.grid(axis='y', ls='--', alpha=0.3)
    ax1.set_ylim(0, 60)
    
    # Right Plot: Leverage Multiplier
    rects3 = ax2.bar(x, [top5_avg['Leverage'], bottom_avg['Leverage']], 0.4, color=[DODGER, ORANGE], edgecolor='black', linewidth=0.4, zorder=3)
    
    # Add values
    for rect in rects3:
        h = rect.get_height()
        ax2.annotate(f"{h:.1f}x", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                    textcoords='offset points', ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#1E293B')
                    
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, fontsize=7.5, fontweight='bold')
    ax2.set_ylabel("Hệ số đòn bẩy (x)", fontsize=8.2, fontweight='bold')
    ax2.set_title("2. Đòn bẩy Tài chính Leverage\n(Hệ số TTS / Vốn chủ sở hữu)", fontsize=8.5, fontweight='bold', color='#1E293B')
    ax2.grid(axis='y', ls='--', alpha=0.3)
    ax2.set_ylim(0, 18)
    
    plt.suptitle("B. Phân rã DuPont: Động lực thúc đẩy ROE năm 2024\n(Top 5 ROE dẫn đầu vs Bottom 4 ROE thấp nhất - Loại trừ NH 22)", 
                 fontsize=9.2, fontweight='bold', color='#1E293B', y=0.98)
    
    fig.tight_layout(pad=1.2)
    path = os.path.join(OUT_DIR, 'slide_16_dupont_comparison.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path} successfully!")

if __name__ == '__main__':
    generate_chart_a()
    generate_chart_b()
    print("All Slide 16 charts generated successfully!")

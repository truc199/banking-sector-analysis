import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# --- Đường dẫn tương đối theo vị trí file (không phụ thuộc máy) ---
import sys as _sys
_sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
PUBLIC = ROOT / "slidev" / "public"
FONTS = ROOT / "slidev" / "fonts"
# ------------------------------------------------------------------

# Setup fonts
for font_file in glob.glob(str(FONTS / "*.ttf")):
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
GRAY_LIGHT   = '#94A3B8'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# Load data
bs_df = pd.read_csv(DATA / "[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
inc_df = pd.read_csv(DATA / "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
note_df = pd.read_csv(DATA / "[G'Contest 2026] Đề Vòng 2_3. Note.csv")

for df in [bs_df, inc_df, note_df]:
    for col in df.columns:
        if col not in ['Công ty', 'Năm']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Merge
m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm'])

# NPL and CASA
cols = ['C33', 'C34', 'C35', 'C36', 'C37']
note_df['Total_Loans'] = note_df[cols].sum(axis=1)
note_df['NPL_Amount'] = note_df['C35'] + note_df['C36'] + note_df['C37']
note_df['NPL_Ratio'] = np.where(note_df['Total_Loans'] > 0, note_df['NPL_Amount'] / note_df['Total_Loans'] * 100, 0)

dep_cols = ['C68', 'C69', 'C70', 'C71', 'C72']
note_df['Total_Dep'] = note_df[dep_cols].sum(axis=1)
note_df['CASA_Ratio'] = np.where(note_df['Total_Dep'] > 0, note_df['C68'] / note_df['Total_Dep'] * 100, 0)

m_df = m_df.merge(note_df[['Công ty', 'Năm', 'NPL_Ratio', 'CASA_Ratio']], on=['Công ty', 'Năm'], how='left')
m_df['ROA'] = m_df['B22'] / m_df['A1'] * 100

# Compute for phases
p1 = m_df[m_df['Năm'].isin([2020, 2021])].groupby('Công ty')[['NPL_Ratio', 'CASA_Ratio', 'ROA']].mean().reset_index()
p2 = m_df[m_df['Năm'].isin([2022, 2023])].groupby('Công ty')[['NPL_Ratio', 'CASA_Ratio', 'ROA']].mean().reset_index()
p3 = m_df[m_df['Năm'] == 2024][['Công ty', 'NPL_Ratio', 'CASA_Ratio', 'ROA']].copy()

# Setup subplots (3 panels horizontally)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13.0, 5.0), dpi=350, sharey=True)

ylim_min = -5.0
ylim_max = 3.5

# ----------------------------------------------------
# PANEL A (GĐ1): CASA vs ROA
# ----------------------------------------------------
ax1.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', zorder=0)
sizes_a = p1['CASA_Ratio'] * 7.5 + 20
sc1 = ax1.scatter(p1['CASA_Ratio'], p1['ROA'], s=sizes_a, color=TEAL, alpha=0.8, edgecolors='white', linewidths=0.8, zorder=3)

# Fit line CASA vs ROA
m1, b1 = np.polyfit(p1['CASA_Ratio'], p1['ROA'], 1)
x_range_1 = np.linspace(p1['CASA_Ratio'].min() - 2.0, p1['CASA_Ratio'].max() + 2.0, 100)
ax1.plot(x_range_1, m1 * x_range_1 + b1, color=TEAL, linestyle='-', linewidth=2.0, zorder=2)

ax1.text(48, ylim_max * 0.75, "Tương quan thuận mạnh:\n  r = +0.675\nCASA thống trị lợi nhuận", 
         ha='right', va='top', fontsize=8.5, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#cbd5e1', alpha=0.9, lw=0.6))
ax1.set_title('Panel A (GĐ1: 2020-2021)\nTrục hoành CASA vs. ROA', fontweight='bold', fontsize=10.5, pad=10, color=TEAL)
ax1.set_xlabel('Tỷ lệ CASA (%)', fontweight='bold', fontsize=9)
ax1.set_xlim(5, 50)

# ----------------------------------------------------
# PANEL B (GĐ2): Giai đoạn chuyển giao (NPL vs ROA)
# ----------------------------------------------------
ax2.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', zorder=0)
sizes_b = p2['CASA_Ratio'] * 7.5 + 20
colors_b = [RED if npl_val > 5.0 or bank == 22 else NAVY_DARK for bank, npl_val in zip(p2['Công ty'], p2['NPL_Ratio'])]
sc2 = ax2.scatter(p2['NPL_Ratio'], p2['ROA'], s=sizes_b, color=colors_b, alpha=0.8, edgecolors='white', linewidths=0.8, zorder=3)

# Fit line NPL vs ROA
m2, b2 = np.polyfit(p2['NPL_Ratio'], p2['ROA'], 1)
x_range_2 = np.linspace(0, p2['NPL_Ratio'].max() + 0.5, 100)
ax2.plot(x_range_2, m2 * x_range_2 + b2, color=NAVY_DARK, linestyle='--', linewidth=1.5, zorder=2)

ax2.text(20, ylim_max * 0.75, "Tương quan âm tăng dần:\n  r = -0.471\nNợ xấu bắt đầu bào mòn", 
         ha='right', va='top', fontsize=8.5, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#cbd5e1', alpha=0.9, lw=0.6))
ax2.set_title('Panel B (GĐ2: 2022-2023)\nTrục hoành NPL vs. ROA', fontweight='bold', fontsize=10.5, pad=10, color=NAVY_DARK)
ax2.set_xlabel('Tỷ lệ nợ xấu NPL (%)', fontweight='bold', fontsize=9)
ax2.set_xlim(-0.8, 21.0)

# Label NH22
nh22_gd2 = p2[p2['Công ty'] == 22].iloc[0]
ax2.text(nh22_gd2['NPL_Ratio'] + 0.5, nh22_gd2['ROA'], 'NH22', ha='left', va='center', fontsize=7.5, color=RED, fontweight='bold')

# ----------------------------------------------------
# PANEL C (GĐ3): NPL thống trị (NPL vs ROA)
# ----------------------------------------------------
ax3.grid(True, linestyle='--', alpha=0.3, color='#94a3b8', zorder=0)
sizes_c = p3['CASA_Ratio'] * 7.5 + 20
colors_c = [RED if npl_val > 5.0 or bank == 22 else NAVY_DARK for bank, npl_val in zip(p3['Công ty'], p3['NPL_Ratio'])]
sc3 = ax3.scatter(p3['NPL_Ratio'], p3['ROA'], s=sizes_c, color=colors_c, alpha=0.8, edgecolors='white', linewidths=0.8, zorder=3)

# Fit line NPL vs ROA
m3, b3 = np.polyfit(p3['NPL_Ratio'], p3['ROA'], 1)
x_range_3 = np.linspace(0, p3['NPL_Ratio'].max() + 0.5, 100)
ax3.plot(x_range_3, m3 * x_range_3 + b3, color=RED, linestyle='-', linewidth=2.0, zorder=2)

ax3.text(20, ylim_max * 0.75, "NPL thống trị tuyệt đối:\n  r = -0.894\nCASA mất ngôi vương", 
         ha='right', va='top', fontsize=8.5, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#cbd5e1', alpha=0.9, lw=0.6))
ax3.set_title('Panel C (GĐ3: 2024)\nTrục hoành NPL vs. ROA', fontweight='bold', fontsize=10.5, pad=10, color=RED)
ax3.set_xlabel('Tỷ lệ nợ xấu NPL (%)', fontweight='bold', fontsize=9)
ax3.set_xlim(-0.8, 21.0)

# Label NH22, NH7, NH4
nh22_gd3 = p3[p3['Công ty'] == 22].iloc[0]
nh7_gd3 = p3[p3['Công ty'] == 7].iloc[0]
nh4_gd3 = p3[p3['Công ty'] == 4].iloc[0]
ax3.text(nh22_gd3['NPL_Ratio'] - 0.5, nh22_gd3['ROA'], 'NH22', ha='right', va='center', fontsize=7.5, color=RED, fontweight='bold')
ax3.text(nh7_gd3['NPL_Ratio'] + 0.5, nh7_gd3['ROA'], 'NH7', ha='left', va='center', fontsize=7.5, color=TEAL, fontweight='bold')
ax3.text(nh4_gd3['NPL_Ratio'] - 0.5, nh4_gd3['ROA'] + 0.2, 'NH4', ha='right', va='center', fontsize=7.5, color=TEAL, fontweight='bold')

# Y axis labels and limit
ax1.set_ylabel('Tỷ suất sinh lời ROA (%)', fontweight='bold', fontsize=9)
ax1.set_ylim(ylim_min, ylim_max)

# Style spines
for ax in [ax1, ax2, ax3]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cbd5e1')
    ax.spines['bottom'].set_color('#cbd5e1')

plt.suptitle('Sự dịch chuyển tương quan qua 3 giai đoạn (Kích cỡ bong bóng = Tỷ lệ CASA %)', 
             fontsize=12, fontweight='bold', color=TEXT_DARK, y=0.98)

# Legend details
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Nhóm nợ xấu thấp (<1.2%)', markerfacecolor=TEAL, markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Nhóm nợ trung vị', markerfacecolor=NAVY_DARK, markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Nhóm nợ xấu cao (>5% hoặc NH22)', markerfacecolor=RED, markersize=8),
    Line2D([0], [0], marker='o', color='w', label='CASA dày (Bong bóng lớn)', markerfacecolor='gray', markersize=12, alpha=0.5),
    Line2D([0], [0], marker='o', color='w', label='CASA mỏng (Bong bóng nhỏ)', markerfacecolor='gray', markersize=6, alpha=0.5),
    Line2D([0], [0], linestyle='-', color=RED, label='Đường hồi quy tương quan')
]

# Use tight_layout with a rect parameter to reserve bottom space for the legend
plt.tight_layout(rect=[0, 0.14, 1, 0.95])

# Place the legend in the reserved space
fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=3, fontsize=9.0, framealpha=0.9)

path = os.path.join(public_dir, 'new_slide_8_2_correlation_shift.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 8.2 Correlation Shift Bubble chart successfully with custom axes!")

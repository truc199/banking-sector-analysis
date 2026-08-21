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
RED          = '#C0392B'
ORANGE       = '#E67E22'
TEAL         = '#0D9488'
GRAY_LIGHT   = '#CBD5E1'
TEXT_DARK    = '#0f172a'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# Load data
note_df = pd.read_csv(DATA / "[G'Contest 2026] Đề Vòng 2_3. Note.csv")

cols = ['C33', 'C34', 'C35', 'C36', 'C37']
for col in cols:
    note_df[col] = pd.to_numeric(note_df[col], errors='coerce').fillna(0)

# Calculate NPL Ratio
note_df['Total_Loans'] = note_df[cols].sum(axis=1)
note_df['NPL_Amount'] = note_df['C35'] + note_df['C36'] + note_df['C37']
note_df['NPL_Ratio'] = np.where(note_df['Total_Loans'] > 0, note_df['NPL_Amount'] / note_df['Total_Loans'] * 100, 0)

# Filter for 2021 and 2023
df_21 = note_df[note_df['Năm'] == 2021][['Công ty', 'NPL_Ratio']].rename(columns={'NPL_Ratio': 'NPL_2021'})
df_23 = note_df[note_df['Năm'] == 2023][['Công ty', 'NPL_Ratio']].rename(columns={'NPL_Ratio': 'NPL_2023'})

merged = pd.merge(df_21, df_23, on='Công ty')

fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=350)

# Define bank categories
high_risk = [22, 8, 15]
safe_banks = [4, 7, 20]

# Calculate single line for Safe group
safe_df = merged[merged['Công ty'].isin(safe_banks)]
safe_y21 = safe_df['NPL_2021'].mean()
safe_y23 = safe_df['NPL_2023'].mean()

# Plot other banks and high-risk banks
for idx, r in merged.iterrows():
    bank_id = int(r['Công ty'])
    y21 = r['NPL_2021']
    y23 = r['NPL_2023']
    
    # Skip safe banks (they will be plotted as a single group line)
    if bank_id in safe_banks:
        continue
        
    if bank_id in high_risk:
        color = RED if bank_id == 22 else ORANGE
        linewidth = 2.0
        zorder = 5
        alpha = 1.0
        ax.plot([2021, 2023], [y21, y23], color=color, linewidth=linewidth, zorder=zorder, alpha=alpha, marker='o', markersize=4)
        
        # Annotate
        label = f"NH{bank_id} ({y23:.1f}%)"
        if bank_id == 22:
            ax.text(2023.05, y23, label, color=RED, fontsize=8, fontweight='bold', va='center')
        elif bank_id == 8:
            ax.text(2023.05, y23 + 0.4, label, color=ORANGE, fontsize=8, fontweight='bold', va='center')
        elif bank_id == 15:
            ax.text(2023.05, y23 - 0.4, label, color=ORANGE, fontsize=8, fontweight='bold', va='center')
            
    else:
        # Do not plot other banks to declutter the chart
        pass

# Plot single average line for the safe banks group
ax.plot([2021, 2023], [safe_y21, safe_y23], color=TEAL, linewidth=2.5, zorder=6, marker='o', markersize=5)
ax.text(2023.05, safe_y23, f"Nhóm an toàn ({safe_y23:.1f}%)", color=TEAL, fontsize=8, fontweight='bold', va='center')

# Axis styling
ax.set_xticks([2021, 2023])
ax.set_xticklabels(['Năm 2021\n(Trước bão)', 'Năm 2023\n(Sau ân hạn)'], fontsize=9.5, fontweight='bold')
ax.set_ylabel('Tỷ lệ nợ xấu NPL (%)', fontsize=9.5, fontweight='bold', labelpad=6)
ax.set_title('Bản đồ Trajectory NPL 27 ngân hàng (2021 vs 2023)\nPhân hóa rõ nét nhóm rủi ro BĐS vs nhóm an toàn', 
             fontsize=11, fontweight='bold', pad=15, color=TEXT_DARK)

ax.set_xlim(2020.6, 2023.8)
ax.set_ylim(-1, 33)

ax.grid(True, axis='y', ls='--', color='#f1f5f9', alpha=0.8, zorder=0)

# Legend (Removed "các ngân hàng khác đi" and changed "kỉ luật cao" to "an toàn")
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=RED, label='Rủi ro cực cao (NH22): NPL vọt tăng sát 30%'),
    Patch(facecolor=ORANGE, label='Rủi ro cao (NH8, NH15): NPL tăng mạnh'),
    Patch(facecolor=TEAL, label='An toàn (NH4, NH7, NH20): NPL duy trì cực thấp (<1.2%)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8.5, framealpha=0.9)

# Hide top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cbd5e1')
ax.spines['bottom'].set_color('#cbd5e1')

plt.tight_layout()
path = os.path.join(public_dir, 'new_slide_7_3_npl_trajectory.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 7.3 chart successfully with updated legend and safe group line!")

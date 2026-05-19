import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle

# Setup fonts
for font_file in glob.glob(r'd:\uni\gcontest\slidev\fonts\*.ttf'):
    try:
        fm.fontManager.addfont(font_file)
    except Exception:
        pass

plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['text.color'] = '#1e293b'

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# Helper function
def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

# Load data
bs_df = pd.read_csv(glob.glob(r'd:\uni\gcontest\*Balance*')[0])
inc_df = pd.read_csv(glob.glob(r'd:\uni\gcontest\*Income*')[0])
note_df = pd.read_csv(glob.glob(r'd:\uni\gcontest\*Note*')[0])

for df in [bs_df, inc_df, note_df]:
    for col in df.columns:
        if col not in ['Công ty', 'Năm']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm']).merge(note_df, on=['Công ty', 'Năm'])

# Filter 2024
m24 = m_df[m_df['Năm'] == 2024].copy()

# Compute 5 metrics
m24['CASA'] = safe_div(m24['C68'], m24['A55']) * 100
m24['LDR'] = safe_div(m24['A13'], m24['A55']) * 100
m24['Equity_Ratio'] = safe_div(m24['A64'], m24['A1']) * 100

npl_sum = m24[['C35','C36','C37']].sum(axis=1)
total_loans = m24[['C33','C34','C35','C36','C37']].sum(axis=1)
m24['NPL'] = safe_div(npl_sum, total_loans) * 100
m24['Coverage'] = safe_div(m24['A14'].abs(), npl_sum) * 100

m24 = m24[['Công ty', 'CASA', 'LDR', 'Equity_Ratio', 'Coverage', 'NPL']].dropna().sort_values(by='Công ty').reset_index(drop=True)

# Define color thresholds
def get_colors_and_text(row):
    # CASA: >= 25% Green, 15-25% Yellow, < 15% Red
    casa = row['CASA']
    if casa >= 25:
        c_casa = '#d1fae5'  # Emerald 100
        tc_casa = '#065f46'
    elif casa >= 15:
        c_casa = '#fef3c7'  # Amber 100
        tc_casa = '#92400e'
    else:
        c_casa = '#fee2e2'  # Red 100
        tc_casa = '#991b1b'

    # LDR: <= 85% Green, 85-100% Yellow, > 100% Red
    ldr = row['LDR']
    if ldr <= 85:
        c_ldr = '#d1fae5'
        tc_ldr = '#065f46'
    elif ldr <= 100:
        c_ldr = '#fef3c7'
        tc_ldr = '#92400e'
    else:
        c_ldr = '#fee2e2'
        tc_ldr = '#991b1b'

    # Equity Ratio: >= 10% Green, 6-10% Yellow, < 6% Red
    eq = row['Equity_Ratio']
    if eq >= 10:
        c_eq = '#d1fae5'
        tc_eq = '#065f46'
    elif eq >= 6:
        c_eq = '#fef3c7'
        tc_eq = '#92400e'
    else:
        c_eq = '#fee2e2'
        tc_eq = '#991b1b'

    # Coverage: >= 100% Green, 50-100% Yellow, < 50% Red
    cov = row['Coverage']
    if cov >= 100:
        c_cov = '#d1fae5'
        tc_cov = '#065f46'
    elif cov >= 50:
        c_cov = '#fef3c7'
        tc_cov = '#92400e'
    else:
        c_cov = '#fee2e2'
        tc_cov = '#991b1b'

    # NPL: <= 1.5% Green, 1.5-3.0% Yellow, > 3.0% Red
    npl = row['NPL']
    if npl <= 1.5:
        c_npl = '#d1fae5'
        tc_npl = '#065f46'
    elif npl <= 3.0:
        c_npl = '#fef3c7'
        tc_npl = '#92400e'
    else:
        c_npl = '#fee2e2'
        tc_npl = '#991b1b'

    return {
        'CASA': (c_casa, tc_casa, f"{casa:.1f}%"),
        'LDR': (c_ldr, tc_ldr, f"{ldr:.1f}%"),
        'Equity_Ratio': (c_eq, tc_eq, f"{eq:.1f}%"),
        'Coverage': (c_cov, tc_cov, f"{cov:.1f}%" if cov < 999 else "N/A"),
        'NPL': (c_npl, tc_npl, f"{npl:.2f}%")
    }

# Draw custom table using matplotlib
# 27 rows + header. We want a tall figure.
num_rows = len(m24)
fig, ax = plt.subplots(figsize=(6.5, 9.2), dpi=350)
ax.set_xlim(0, 6)
ax.set_ylim(-0.5, num_rows + 1)
ax.axis('off')

# Header
cols_meta = [
    {'name': 'Ngân hàng', 'x': 0.5, 'w': 0.8},
    {'name': 'CASA (wt)', 'x': 1.4, 'w': 0.8},
    {'name': 'LDR', 'x': 2.3, 'w': 0.8},
    {'name': 'Đệm vốn', 'x': 3.2, 'w': 0.8},
    {'name': 'Bao phủ nợ', 'x': 4.1, 'w': 0.8},
    {'name': 'Nợ xấu NPL', 'x': 5.0, 'w': 0.8}
]

# Draw header row
y_header = num_rows + 0.3
ax.add_patch(Rectangle((0.1, y_header - 0.35), 5.8, 0.7, facecolor='#003366', edgecolor='none', zorder=1))
for col in cols_meta:
    ax.text(col['x'], y_header, col['name'], ha='center', va='center', color='white', fontweight='bold', fontsize=8.5, zorder=2)

# Draw bank rows
for idx, row in m24.iterrows():
    bank_id = int(row['Công ty'])
    y = num_rows - 1 - idx
    
    # Alternating row background for bank names
    bg_row = '#f8fafc' if idx % 2 == 0 else '#ffffff'
    ax.add_patch(Rectangle((0.1, y - 0.4), 0.8, 0.8, facecolor=bg_row, edgecolor='#e2e8f0', linewidth=0.4, zorder=1))
    ax.text(0.5, y, f"NH {bank_id}", ha='center', va='center', fontweight='bold', fontsize=8, color='#0f172a', zorder=2)
    
    # Get colors for metrics
    m_colors = get_colors_and_text(row)
    
    # Draw cells
    metrics_keys = ['CASA', 'LDR', 'Equity_Ratio', 'Coverage', 'NPL']
    for m_idx, key in enumerate(metrics_keys):
        col_info = cols_meta[m_idx + 1]
        c_bg, tc, text_val = m_colors[key]
        
        # Draw background patch for cell
        ax.add_patch(Rectangle((col_info['x'] - col_info['w']/2, y - 0.4), col_info['w'], 0.8, 
                               facecolor=c_bg, edgecolor='#e2e8f0', linewidth=0.4, zorder=1))
        # Draw text
        ax.text(col_info['x'], y, text_val, ha='center', va='center', color=tc, fontweight='bold', fontsize=7.8, zorder=2)

# Draw a title & legend box at the bottom
legend_y = -0.5
ax.add_patch(Rectangle((0.1, legend_y - 0.2), 5.8, 0.6, facecolor='white', edgecolor='#e2e8f0', linewidth=0.5, zorder=1))

# Legend items
ax.add_patch(Rectangle((0.3, legend_y - 0.05), 0.3, 0.3, facecolor='#d1fae5', edgecolor='none', zorder=2))
ax.text(0.7, legend_y + 0.1, 'Đạt tiêu chuẩn', fontsize=7, color='#065f46', fontweight='bold', va='center')

ax.add_patch(Rectangle((2.3, legend_y - 0.05), 0.3, 0.3, facecolor='#fef3c7', edgecolor='none', zorder=2))
ax.text(2.7, legend_y + 0.1, 'Cảnh báo / Trung bình', fontsize=7, color='#92400e', fontweight='bold', va='center')

ax.add_patch(Rectangle((4.5, legend_y - 0.05), 0.3, 0.3, facecolor='#fee2e2', edgecolor='none', zorder=2))
ax.text(4.9, legend_y + 0.1, 'Rủi ro / Yếu kém', fontsize=7, color='#991b1b', fontweight='bold', va='center')

# Title
ax.text(3.0, num_rows + 0.85, 'BẢNG ĐIỂM SỨC KHỎE TÀI CHÍNH TOÀN HỆ THỐNG (2024)', 
        ha='center', va='center', color='#003366', fontweight='bold', fontsize=10)

plt.tight_layout()
path = os.path.join(public_dir, 'new_slide_9_2_scorecard_heatmap.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 9.2 Scorecard Heatmap Table successfully!")

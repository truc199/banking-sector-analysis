"""
Generate Chart for NEW Slide 1.3: Phân hóa Đệm vốn toàn hệ thống (2024)
Horizontal bar chart - Equity/TTS % for all 27 banks
Saves to slidev/public/new_slide_1_3_equity_dispersion.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ─── Setup ───────────────────────────────────────────────────────────────
import matplotlib.font_manager as fm
for font_file in glob.glob(r'd:\uni\gcontest\slidev\fonts\*.ttf'):
    try:
        fm.fontManager.addfont(font_file)
    except Exception:
        pass

plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['font.sans-serif'] = ['Roboto', 'Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# ─── Color Palette ───────────────────────────────────────────────────────
NAVY_DARK    = '#003366'
NAVY_MID_D   = '#004C99'
NAVY_MID     = '#0066CC'
AZURE        = '#007FFF'
DODGER       = '#3399FF'
FRENCH_SKY   = '#66B2FF'
BABY_BLUE    = '#99CCFF'

GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'
TEXT_MID     = '#1e293b'

# ─── Font Sizes ──────────────────────────────────────────────────────────
FS_TITLE = 12.5
FS_LABEL = 10.5
FS_TICK  = 9.5
FS_VAL   = 9
FS_LEG   = 9.5

# ─── Output ──────────────────────────────────────────────────────────────
public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
bs = pd.read_csv(bs_file)
bs_2024 = bs[bs['Năm'] == 2024].copy()
bs_2024['equity_ratio'] = bs_2024['A64'] / bs_2024['A1'] * 100
bs_2024 = bs_2024.sort_values('equity_ratio', ascending=True)

bank_labels = [f'NH {int(b)}' for b in bs_2024['Công ty']]
er_vals = bs_2024['equity_ratio'].values
mean_er = bs_2024['equity_ratio'].mean()

# ─── Chart ───────────────────────────────────────────────────────────────
# Tall figure to fit 27 banks horizontally
fig, ax = plt.subplots(figsize=(7.0, 5.5), dpi=350)

# Navy gradient based on value
colors = [
    '#CC3333' if v < 6.0 else      # Red for danger zone
    BABY_BLUE if v < 8.0 else
    FRENCH_SKY if v < 9.0 else
    DODGER if v < 10.0 else
    NAVY_MID if v < 12.0 else
    NAVY_DARK for v in er_vals
]

bars = ax.barh(bank_labels, er_vals, color=colors, height=0.55,
               edgecolor='white', linewidth=0.4, zorder=3)

# 6% Warning Line — LOW OPACITY so bars stand out
ax.axvline(x=6.0, color='#CC3333', linewidth=1.0, linestyle='--',
           alpha=0.35, zorder=2, label='Ngưỡng cảnh báo 6%')

# Mean Line — LOW OPACITY
ax.axvline(x=mean_er, color=AZURE, linewidth=1.0, linestyle='-.',
           alpha=0.35, zorder=2, label=f'Trung bình ({mean_er:.2f}%)')

# Annotate bar values
for bar, val in zip(bars, er_vals):
    w = bar.get_width()
    txt_color = '#CC3333' if val < 6.0 else NAVY_DARK
    ax.text(w + 0.15, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}%', va='center', ha='left',
            fontsize=FS_VAL, fontweight='bold', color=txt_color)

max_er = er_vals.max()

ax.set_xlabel('Tỷ lệ an toàn vốn (Equity / TTS %)', fontsize=FS_LABEL,
              fontweight='bold', labelpad=4, color=TEXT_MID)
ax.set_xlim(0, max_er + 2.5)
ax.grid(True, axis='x', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)
ax.tick_params(axis='y', labelsize=FS_TICK)
ax.tick_params(axis='x', labelsize=FS_TICK)

# Legend at bottom
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
          ncol=2, frameon=False, fontsize=FS_LEG)

# Title
ax.set_title('Phân hóa Đệm vốn toàn Hệ thống Ngân hàng (2024)',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_1_3_equity_dispersion.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE')

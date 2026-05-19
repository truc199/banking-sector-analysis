"""
Generate Chart for Slide 4.3: Retail Credit Structure (2020-2024)
Stacked bar chart: Retail vs Wholesale
Saves to slidev/public/new_slide_4_3_retail.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ─── Setup ───────────────────────────────────────────────────────────────
for font_file in glob.glob(r'd:\uni\gcontest\slidev\fonts\*.ttf'):
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
TEAL         = '#00897B'
GRID_COLOR   = '#f1f5f9'
SPINE_COLOR  = '#cbd5e1'
TEXT_DARK    = '#0f172a'

FS_TITLE = 11.5
FS_LABEL = 10
FS_TICK  = 8.5
FS_VAL   = 9
FS_LEG   = 9

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# ─── Data ────────────────────────────────────────────────────────────────
bs_file = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
n_file = glob.glob(r'd:\uni\gcontest\*Note*')[0]
bs = pd.read_csv(bs_file)
note = pd.read_csv(n_file)

years = [2020, 2021, 2022, 2023, 2024]
bs_y = bs[bs['Năm'].isin(years)]
note_y = note[note['Năm'].isin(years)]

df = pd.merge(bs_y[['Công ty', 'Năm', 'A12']], note_y[['Công ty', 'Năm', 'C42', 'C47']], on=['Công ty', 'Năm'])

# Calculate weighted average
agg = df.groupby('Năm').agg({
    'C47': 'sum',
    'A12': 'sum'
}).reindex(years)

agg['Retail'] = agg['C47'] / agg['A12'] * 100
agg['Wholesale'] = 100 - agg['Retail']

# ─── Chart ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=350)
x = np.arange(len(years))
width = 0.5

bars_wholesale = ax.bar(x, agg['Wholesale'], width, color=NAVY_DARK, label='Doanh nghi\u1ec7p / T\u1ed5 ch\u1ee9c')
bars_retail = ax.bar(x, agg['Retail'], width, bottom=agg['Wholesale'], color=TEAL, label='B\u00e1n l\u1ebb (C\u00e1 nh\u00e2n)')

for i, (w, r) in enumerate(zip(agg['Wholesale'], agg['Retail'])):
    ax.text(x[i], w / 2, f'{w:.1f}%', ha='center', va='center', color='white', fontweight='bold', fontsize=FS_VAL)
    ax.text(x[i], w + r / 2, f'{r:.1f}%', ha='center', va='center', color='white', fontweight='bold', fontsize=FS_VAL)

ax.set_ylabel('T\u1ef7 tr\u1ecdng (% T\u1ed5ng d\u01b0 n\u1ee3)', fontsize=FS_LABEL, fontweight='bold', labelpad=6)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=FS_TICK, fontweight='bold')
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.tick_params(axis='y', labelsize=FS_TICK)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=FS_LEG)

ax.set_title('C\u1ea5u tr\u00fac T\u00edn d\u1ee5ng theo Nh\u00f3m kh\u00e1ch h\u00e0ng',
             fontsize=FS_TITLE, fontweight='bold', pad=10, color=TEXT_DARK)

plt.tight_layout()
plt.savefig(os.path.join(public_dir, 'new_slide_4_3_retail.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()

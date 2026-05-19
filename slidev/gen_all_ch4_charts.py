"""
Generate Chapter 4 charts:
  slide_4_1_casa_ranked.png   – Horizontal bar CASA 2024, ranked
  slide_4_2_ldr_trend.png     – Line chart LDR trend + 100% threshold
  slide_4_3_loan_structure.png – Stacked bar loan mix 2020-2024
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator, FixedLocator
import glob, sys, os

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
matplotlib.rcParams['axes.spines.top']   = False
matplotlib.rcParams['axes.spines.right'] = False

BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
INC_FILE  = glob.glob(r'd:\uni\gcontest\*Income*')[0]
OUT_DIR   = r'd:\uni\gcontest\slidev\public'

YEARS = [2020, 2021, 2022, 2023, 2024]

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

bs   = pd.read_csv(BS_FILE)
note = pd.read_csv(NOTE_FILE)
inc  = pd.read_csv(INC_FILE)

bs5   = bs  [bs  ['Năm'].isin(YEARS)].copy()
note5 = note[note['Năm'].isin(YEARS)].copy()
inc5  = inc [inc ['Năm'].isin(YEARS)].copy()

merged   = bs5.merge(inc5,   on=['Công ty','Năm'])
merged_n = bs5.merge(note5,  on=['Công ty','Năm'])

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4.1 – CASA RANKED BAR (horizontal)
# ─────────────────────────────────────────────────────────────────────────────
def chart_casa():
    casa_cols_denom = ['C68','C69','C70','C71','C72']
    mn = merged_n.copy()
    mn['total_dep'] = mn[casa_cols_denom].sum(axis=1)
    mn['CASA'] = mn['C68'] / mn['total_dep'] * 100

    # 2024 snapshot
    d24 = mn[mn['Năm']==2024][['Công ty','CASA']].copy()
    d24 = d24.sort_values('CASA', ascending=True).reset_index(drop=True)
    n_banks = len(d24)

    # Industry mean
    tot_c68  = mn[mn['Năm']==2024]['C68'].sum()
    tot_dep  = mn[mn['Năm']==2024]['total_dep'].sum()
    wt_avg   = tot_c68 / tot_dep * 100
    sm_avg   = d24['CASA'].mean()

    fig, ax = plt.subplots(figsize=(5.8, 6.4))

    # colour by position
    colors = [DODGER if v >= wt_avg else BABY for v in d24['CASA']]
    # top 3 highlight
    for i in range(n_banks-3, n_banks):
        colors[i] = NAVY

    bars = ax.barh(range(n_banks), d24['CASA'], color=colors,
                   height=0.7, zorder=3)

    # value labels
    for i, v in enumerate(d24['CASA']):
        ax.text(v + 0.4, i, f"{v:.1f}%", va='center', fontsize=7,
                color=NAVY if v >= wt_avg else '#555')

    # vertical mean lines
    ax.axvline(sm_avg, color=RED, lw=1.4, ls='--', zorder=4)
    ax.axvline(wt_avg, color=ORANGE, lw=1.2, ls=':', zorder=4)

    ax.set_yticks(range(n_banks))
    ax.set_yticklabels([f"NH {int(r)}" for r in d24['Công ty']], fontsize=7.5)
    ax.set_xlabel("CASA Ratio (%)", fontsize=8)
    ax.set_title("CASA Ratio 2024 – Xếp hạng theo tỷ lệ tiền gửi không kỳ hạn",
                 fontsize=9, fontweight='bold', pad=6)

    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.grid(axis='x', which='major', ls='--', alpha=0.35, zorder=0)
    ax.grid(axis='x', which='minor', ls=':', alpha=0.2, zorder=0)
    ax.set_xlim(0, 45)

    # legend
    patches = [
        mpatches.Patch(color=NAVY,   label=f'Top 3 (CASA ≥ 35%)'),
        mpatches.Patch(color=DODGER, label=f'Trên trung bình gia quyền ({wt_avg:.1f}%)'),
        mpatches.Patch(color=BABY,   label=f'Dưới trung bình gia quyền'),
        plt.Line2D([0],[0], color=RED,    lw=1.4, ls='--', label=f'Mean đơn giản ({sm_avg:.1f}%)'),
        plt.Line2D([0],[0], color=ORANGE, lw=1.2, ls=':',  label=f'Mean gia quyền ({wt_avg:.1f}%)'),
    ]
    ax.legend(handles=patches, loc='lower right', fontsize=6.5, framealpha=0.85)

    fig.tight_layout(pad=0.6)
    path = os.path.join(OUT_DIR, 'slide_4_1_casa_ranked.png')
    fig.savefig(path, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4.2 – LDR TREND + THRESHOLD
# ─────────────────────────────────────────────────────────────────────────────
def chart_ldr():
    merged['LDR'] = merged['A13'] / merged['A55'] * 100

    # Industry means
    ldr_wt = merged.groupby('Năm').apply(
        lambda d: d['A13'].sum()/d['A55'].sum()*100
    )
    ldr_sm = merged.groupby('Năm')['LDR'].mean()

    # Loan vs deposit growth
    loans   = merged.groupby('Năm')['A13'].sum()
    deps    = merged.groupby('Năm')['A55'].sum()
    loan_g  = loans.pct_change()*100
    dep_g   = deps.pct_change()*100

    fig, ax1 = plt.subplots(figsize=(5.8, 3.8))

    xs = YEARS
    # LDR lines (left axis)
    ax1.plot(xs, [ldr_wt[y] for y in xs], color=NAVY, lw=2.2, marker='o',
             ms=5, label='LDR trung bình gia quyền', zorder=5)
    ax1.plot(xs, [ldr_sm[y] for y in xs], color=DODGER, lw=1.8, marker='s',
             ms=4, ls='--', label='LDR trung bình đơn giản', zorder=5)

    # Threshold 100%
    ax1.axhline(100, color=RED, lw=1.5, ls='--', zorder=4, alpha=0.9)
    ax1.text(2024.08, 100.5, '100%', color=RED, fontsize=8, fontweight='bold')

    # Fill above threshold
    ax1.fill_between(xs, [ldr_wt[y] for y in xs], 100,
                     where=[ldr_wt[y]>=100 for y in xs],
                     alpha=0.13, color=RED, interpolate=True)

    # Value labels
    for y in xs:
        ax1.annotate(f"{ldr_wt[y]:.1f}%", (y, ldr_wt[y]),
                     textcoords='offset points', xytext=(0, 7),
                     ha='center', fontsize=7.5, color=NAVY, fontweight='bold')

    ax1.set_ylabel("LDR (%)", fontsize=8.5, color=NAVY)
    ax1.tick_params(axis='y', labelcolor=NAVY)
    ax1.set_ylim(80, 115)
    ax1.yaxis.set_minor_locator(MultipleLocator(5))

    # Growth bars (right axis)
    ax2 = ax1.twinx()
    xs_growth = YEARS[1:]  # 2021-2024
    bw = 0.32
    x_idx = np.array(xs_growth)
    ax2.bar(x_idx - bw/2, [loan_g[y] for y in xs_growth],
            width=bw, color=BLUE1, alpha=0.55, label='Tăng trưởng tín dụng (%)', zorder=2)
    ax2.bar(x_idx + bw/2, [dep_g[y] for y in xs_growth],
            width=bw, color=TEAL, alpha=0.55, label='Tăng trưởng huy động (%)', zorder=2)
    ax2.set_ylabel("Tăng trưởng YoY (%)", fontsize=8.5, color=GRAY)
    ax2.tick_params(axis='y', labelcolor=GRAY)
    ax2.set_ylim(0, 30)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(GRAY)

    ax1.set_xticks(YEARS)
    ax1.set_xlabel("Năm", fontsize=8)
    ax1.set_title("LDR & Tăng trưởng Tín dụng – Huy động (2020–2024)",
                  fontsize=9, fontweight='bold', pad=6)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               loc='upper left', fontsize=6.8, framealpha=0.88, ncol=2)

    ax1.grid(axis='y', ls='--', alpha=0.3, zorder=0)
    fig.tight_layout(pad=0.6)
    path = os.path.join(OUT_DIR, 'slide_4_2_ldr_trend.png')
    fig.savefig(path, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4.3 – STACKED BAR LOAN STRUCTURE
# ─────────────────────────────────────────────────────────────────────────────
def chart_loan_structure():
    loan_cols = ['C43','C44','C45','C46','C47','C48']
    mn = merged_n.copy()
    mn[loan_cols] = mn[loan_cols].fillna(0)
    mn['total_loan'] = mn[loan_cols].sum(axis=1)

    # Aggregate by year
    rows = []
    for yr in YEARS:
        d = mn[mn['Năm']==yr]
        tot = d[loan_cols].sum()
        grand = tot.sum()
        rows.append({
            'Năm': yr,
            'DNNN':    tot['C43']/grand*100,
            'Cty TNHH & CP': tot['C44']/grand*100,
            'NN & HTX': (tot['C45']+tot['C46'])/grand*100,
            'Cá nhân': tot['C47']/grand*100,
            'Khác':    tot['C48']/grand*100,
        })
    df = pd.DataFrame(rows).set_index('Năm')

    labels   = ['DNNN','Cty TNHH & CP','NN & HTX','Cá nhân','Khác']
    colors   = [BLUE1, DODGER, SKY, NAVY, GRAY]

    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    bottoms = np.zeros(len(YEARS))
    x = np.arange(len(YEARS))
    bw = 0.55

    bars_all = {}
    for lbl, col in zip(labels, colors):
        vals = df[lbl].values
        bars_all[lbl] = ax.bar(x, vals, bottom=bottoms, color=col,
                               width=bw, label=lbl, zorder=3)
        # Label inside bar if tall enough
        for i, (v, b) in enumerate(zip(vals, bottoms)):
            if v > 3:
                ax.text(x[i], b + v/2, f"{v:.1f}%", ha='center', va='center',
                        fontsize=7.5, color='white', fontweight='bold')
        bottoms += vals

    # Annotate cá nhân trend
    ca_nhans = df['Cá nhân'].values
    ca_bottoms = df[['DNNN','Cty TNHH & CP','NN & HTX']].sum(axis=1).values
    ax.plot(x, ca_bottoms + ca_nhans/2, color=RED, lw=1.5, ls='--',
            marker='D', ms=4, zorder=5, label='Xu hướng Cá nhân')

    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in YEARS], fontsize=9)
    ax.set_ylabel("Tỷ trọng (%)", fontsize=8.5)
    ax.set_ylim(0, 105)
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.set_title("Cơ cấu tín dụng theo nhóm khách hàng (2020–2024)",
                 fontsize=9, fontweight='bold', pad=6)
    ax.set_xlabel("Năm", fontsize=8)

    handles, lbls = ax.get_legend_handles_labels()
    ax.legend(handles, lbls, loc='lower center', fontsize=7,
              bbox_to_anchor=(0.5, -0.30), ncol=3, framealpha=0.9)

    ax.grid(axis='y', ls='--', alpha=0.3, zorder=0)
    fig.tight_layout(pad=0.6)
    path = os.path.join(OUT_DIR, 'slide_4_3_loan_structure.png')
    fig.savefig(path, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {path}")


if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    chart_casa()
    chart_ldr()
    chart_loan_structure()
    print("All Chapter 4 charts generated.")

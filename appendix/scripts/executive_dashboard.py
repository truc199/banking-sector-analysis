# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "numpy",
# ]
# ///

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# --- Đường dẫn tương đối theo vị trí file (không phụ thuộc máy) ---
import sys as _sys
from pathlib import Path as _Path
_sys.stdout.reconfigure(encoding="utf-8")
ROOT = _Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FIGURES = ROOT / "appendix" / "figures"
FIGURES_S = str(FIGURES)
FIGURES.mkdir(parents=True, exist_ok=True)
# ------------------------------------------------------------------

def load_and_merge_data():
    bs_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
    is_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
    note_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_3. Note.csv")

    # Read the data. Assuming the first row is now columns 'Công ty', 'Năm', ... based on previous interaction
    df_bs = pd.read_csv(bs_file)
    df_is = pd.read_csv(is_file)
    df_note = pd.read_csv(note_file)

    # Convert ID and Year to int/str to safely merge
    for df in [df_bs, df_is, df_note]:
        df['Công ty'] = df['Công ty'].astype(str)
        df['Năm'] = pd.to_numeric(df['Năm'], errors='coerce')
        
    df_merged = df_bs.merge(df_is, on=['Công ty', 'Năm'], how='inner')
    df_merged = df_merged.merge(df_note, on=['Công ty', 'Năm'], how='inner')
    
    return df_merged

def clean_to_numeric(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    return df

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("Đang tổng hợp dữ liệu từ Balance Sheet, Income Statement và Notes...")
    
    df = load_and_merge_data()
    
    # Các cột cần thiết
    req_cols = ['A1', 'A13', 'A55', 'B3', 'B14', 'B22', 'C35', 'C36', 'C37', 'C68']
    df = clean_to_numeric(df, req_cols)
    
    # Lọc bỏ nhiễu
    df = df[df['A1'] > 0]
    
    # --- TÍNH TOÁN CÁC CHỈ SỐ TÀI CHÍNH (KPIs) CỐT LÕI ---
    # 1. NPL (Tỷ lệ nợ xấu) = Nhóm 3+4+5 / Tổng dư nợ cho vay khách hàng
    df['NPL_Ratio'] = np.where(df['A13'] > 0, (df['C35'] + df['C36'] + df['C37']) / df['A13'] * 100, 0)
    
    # 2. ROA (Tỷ suất sinh lời trên tài sản) = Lợi nhuận sau thuế / Tổng tài sản
    df['ROA'] = np.where(df['A1'] > 0, df['B22'] / df['A1'] * 100, 0)
    
    # 3. CASA (Tỷ lệ tiền gửi không kỳ hạn) = C68 / Tổng tiền gửi A55
    df['CASA_Ratio'] = np.where(df['A55'] > 0, df['C68'] / df['A55'] * 100, 0)
    
    # 4. LDR (Loan to Deposit) = A13 / A55
    df['LDR'] = np.where(df['A55'] > 0, df['A13'] / df['A55'] * 100, 0)
    
    # 5. Non-Interest Income Ratio = (B14 - B3) / B14
    df['Non_Interest_Inc_Ratio'] = np.where(df['B14'] > 0, (df['B14'] - df['B3']) / df['B14'] * 100, 0)

    # --- TẠO DASHBOARD TRÌNH BÀY (EXECUTIVE DASHBOARD) ---
    print("Đang vẽ Bảng điều khiển Sức khỏe Hệ thống (Executive Dashboard)...")
    
    # Style
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    # Custom fonts and colors
    main_color = '#1f77b4'
    accent_color = '#d62728'
    gold_color = '#ffb300'
    
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('BANKING SECTOR HEALTH & PERFORMANCE DASHBOARD', fontsize=26, fontweight='bold', y=0.96)
    
    # Lưới 2x2
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)
    
    # -------------------------------------------------------------------------
    # CHART 1 (Top Left): Profitability vs Asset Quality Cycle (System Trend)
    # -------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    sys_trend = df.groupby('Năm').agg({'B22': 'sum', 'NPL_Ratio': 'mean'}).reset_index()
    sys_trend = sys_trend[sys_trend['Năm'] >= 2015] # Lọc dữ liệu chuẩn
    
    ax1_tw = ax1.twinx()
    # Bar for Profit (B22)
    sns.barplot(data=sys_trend, x='Năm', y='B22', color='lightsteelblue', ax=ax1, alpha=0.8)
    # Line for NPL
    sns.lineplot(data=sys_trend, x=np.arange(len(sys_trend)), y='NPL_Ratio', 
                 color=accent_color, marker='o', linewidth=3, markersize=10, ax=ax1_tw)
    
    ax1.set_title('I. Industry Cycle: Net Profit vs Bad Debt (NPL) Trend', fontsize=16, fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('Total Net Profit (Billion VND)', fontsize=12, color='#5b7c99')
    ax1_tw.set_ylabel('System Avg NPL Ratio (%)', fontsize=12, color=accent_color)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000:,.0f}k'))
    ax1.grid(False)
    
    # -------------------------------------------------------------------------
    # CHART 2 (Top Right): Liquidity Analysis (CASA vs LDR)
    # -------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])
    liq_trend = df.groupby('Năm').agg({'CASA_Ratio': 'mean', 'LDR': 'mean'}).reset_index()
    liq_trend = liq_trend[liq_trend['Năm'] >= 2015]
    
    ax2_tw = ax2.twinx()
    sns.lineplot(data=liq_trend, x='Năm', y='CASA_Ratio', color=gold_color, marker='s', linewidth=3, ax=ax2, label='Avg CASA Ratio (%)')
    sns.lineplot(data=liq_trend, x='Năm', y='LDR', color='teal', marker='^', linewidth=3, ax=ax2_tw, label='Avg LDR (%)')
    
    ax2.set_title('II. Liquidity & Cost of Funds: CASA vs LDR Evolution', fontsize=16, fontweight='bold')
    ax2.set_xlabel('')
    ax2.set_ylabel('CASA Ratio (%)', fontsize=12, color=gold_color)
    ax2_tw.set_ylabel('Loan to Deposit Ratio (LDR) (%)', fontsize=12, color='teal')
    
    # Force legends
    lines_1, labels_1 = ax2.get_legend_handles_labels()
    lines_2, labels_2 = ax2_tw.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', frameon=True)
    ax2_tw.get_legend().remove() if ax2_tw.get_legend() else None
    
    # -------------------------------------------------------------------------
    # CHART 3 (Bottom Left): Risk vs Reward Quadrant (Latest Year = 2024)
    # -------------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])
    # Assume latest robust year is 2024 or max year available
    latest_year = df['Năm'].max()
    df_latest = df[df['Năm'] == latest_year].copy()
    
    # Bubble plot
    scatter = ax3.scatter(df_latest['NPL_Ratio'], df_latest['ROA'], 
                          s=df_latest['A1']/2000, # Size by Total Assets
                          c=df_latest['ROA'], cmap='viridis', alpha=0.7, edgecolors='white', linewidth=1.5)
    
    # Add annotations for biggest/outlier banks
    for i, row in df_latest.iterrows():
        # Label if Assets are huge, or NPL is huge, or ROA is huge
        if row['A1'] > df_latest['A1'].quantile(0.8) or row['NPL_Ratio'] > 4 or row['ROA'] > 2:
            ax3.annotate(row['Công ty'], (row['NPL_Ratio'], row['ROA']), 
                         xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')
            
    # Draw quadrants (medians)
    npl_med = df_latest['NPL_Ratio'].median()
    roa_med = df_latest['ROA'].median()
    ax3.axvline(npl_med, color='gray', linestyle='--', alpha=0.5)
    ax3.axhline(roa_med, color='gray', linestyle='--', alpha=0.5)
    
    ax3.text(npl_med * 0.5, roa_med * 1.5, "High Return, Low Risk\n(STARS)", alpha=0.3, fontsize=18, ha='center')
    ax3.text(npl_med * 1.5, roa_med * 0.5, "Low Return, High Risk\n(DOGS)", alpha=0.3, fontsize=18, ha='center')
    
    ax3.set_title(f'III. Risk vs Return Positioning ({int(latest_year)})', fontsize=16, fontweight='bold')
    ax3.set_xlabel('Bad Debt Ratio - NPL (%)', fontsize=12)
    ax3.set_ylabel('Return on Assets - ROA (%)', fontsize=12)
    
    # -------------------------------------------------------------------------
    # CHART 4 (Bottom Right): Income Structure Diversification
    # -------------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])
    inc_trend = df.groupby('Năm').agg({'B3': 'sum', 'B14': 'sum'}).reset_index()
    inc_trend = inc_trend[inc_trend['Năm'] >= 2015]
    inc_trend['Non_Interest'] = inc_trend['B14'] - inc_trend['B3']
    
    # Stacked bar/area
    ax4.stackplot(inc_trend['Năm'], inc_trend['B3'], inc_trend['Non_Interest'], 
                  labels=['Interest Income', 'Non-Interest/Fee Income'],
                  colors=['#4c72b0', '#55a868'], alpha=0.8)
                  
    # Plot the Non-Interest ratio line on secondary axis
    inc_trend['Fee_Ratio'] = inc_trend['Non_Interest'] / inc_trend['B14'] * 100
    ax4_tw = ax4.twinx()
    sns.lineplot(data=inc_trend, x='Năm', y='Fee_Ratio', color='white', marker='D', 
                 linewidth=2, markersize=8, ax=ax4_tw, label='Fee Income Ratio (%)')
                 
    ax4.set_title('IV. Revenue Diversification Trend', fontsize=16, fontweight='bold')
    ax4.set_xlabel('')
    ax4.set_ylabel('Operating Income (Billion VND)', fontsize=12)
    ax4_tw.set_ylabel('Fee Income Ratio (%)', fontsize=12, color='white') # Make text white/invisible or style it
    ax4_tw.grid(False)
    
    lines_1, labels_1 = ax4.get_legend_handles_labels()
    lines_2, labels_2 = ax4_tw.get_legend_handles_labels()
    ax4.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    ax4_tw.get_legend().remove()
    
    # -------------------------------------------------------------------------
    # Finalize & Save
    # -------------------------------------------------------------------------
    # Add a footnote
    fig.text(0.5, 0.02, "Source: Synthesized from Contest Data (Balance Sheet, Income Statement, Notes) | Bubble size in Quadrant III represents Total Assets", 
             ha='center', fontsize=11, fontstyle='italic', color='gray')
             
    os.makedirs(FIGURES_S, exist_ok=True)
    out_path = os.path.join(FIGURES_S, "Banking_Executive_Dashboard.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"\n[THÀNH CÔNG] Đã tạo và lưu Dashboard Thuyết trình Đẳng cấp tại:\n -> {out_path}")
    print("\n[INSIGHTS GỢI Ý ĐỂ TRÌNH BÀY]:")
    print("1. Industry Cycle (Biểu đồ 1): Nêu bật sự tương quan ngược chiều giữa Tăng trưởng Lợi nhuận và Nợ xấu. Ví dụ năm NPL vọt lên thường lợi nhuận bị bào mòn (do trích lập dự phòng).")
    print("2. Liquidity (Biểu đồ 2): CASA là nguồn vốn giá rẻ. Sự thay đổi của CASA và LDR cho thấy thanh khoản hệ thống có đang căng thẳng hay không.")
    print("3. Risk vs Return (Biểu đồ 3): Cực kỳ trực quan để chỉ điểm các ngân hàng 'Ngôi sao' (Lợi nhuận cao, Nợ xấu thấp) so với các ngân hàng 'Đội sổ'. Bóng to = Ngân hàng lớn.")
    print("4. Diversification (Biểu đồ 4): Xu hướng chuyển dịch từ ăn chênh lệch lãi suất thuần túy sang thu phí dịch vụ. Tỷ trọng Non-interest income càng cao chứng tỏ HĐKD càng bền vững.")

if __name__ == "__main__":
    main()

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

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== PHÂN TÍCH TĂNG TRƯỞNG TÍN DỤNG ===\n")
    
    bs_file = "[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv"
    note_file = "[G'Contest 2026] Đề Vòng 2_3. Note.csv"
    
    df_bs = pd.read_csv(bs_file)
    df_note = pd.read_csv(note_file)
    
    for df in [df_bs, df_note]:
        df['Công ty'] = df['Công ty'].astype(str)
        df['Năm'] = pd.to_numeric(df['Năm'], errors='coerce')
        
    df_merged = df_bs.merge(df_note, on=['Công ty', 'Năm'], how='inner')
    
    # Chỉ số tín dụng: 
    # A13: Cho vay khách hàng (Total Loans)
    # A55: Tiền gửi khách hàng (Total Deposits)
    # C39: Cho vay ngắn hạn
    # C40: Cho vay trung hạn
    # C41: Cho vay dài hạn
    cols = ['A13', 'A55', 'C39', 'C40', 'C41']
    for c in cols:
        df_merged[c] = pd.to_numeric(df_merged[c], errors='coerce').fillna(0)
        
    # --- 1. TĂNG TRƯỞNG TÍN DỤNG TOÀN HỆ THỐNG ---
    sys_loans = df_merged.groupby('Năm').agg({
        'A13': 'sum',
        'A55': 'sum',
        'C39': 'sum',
        'C40': 'sum',
        'C41': 'sum'
    }).reset_index()
    sys_loans = sys_loans[sys_loans['Năm'] >= 2015]
    
    # Tính YoY Growth toàn hệ thống
    sys_loans['Credit_Growth_YoY'] = sys_loans['A13'].pct_change() * 100
    
    # Tính cơ cấu kỳ hạn
    sys_loans['Total_Term_Loans'] = sys_loans['C39'] + sys_loans['C40'] + sys_loans['C41']
    sys_loans['Short_Term_Ratio'] = np.where(sys_loans['Total_Term_Loans'] > 0, sys_loans['C39'] / sys_loans['Total_Term_Loans'] * 100, 0)
    sys_loans['Medium_Term_Ratio'] = np.where(sys_loans['Total_Term_Loans'] > 0, sys_loans['C40'] / sys_loans['Total_Term_Loans'] * 100, 0)
    sys_loans['Long_Term_Ratio'] = np.where(sys_loans['Total_Term_Loans'] > 0, sys_loans['C41'] / sys_loans['Total_Term_Loans'] * 100, 0)

    # --- 2. TĂNG TRƯỞNG TÍN DỤNG TỪNG NGÂN HÀNG (CAGR 2015 - Latest) ---
    df_sorted = df_merged.sort_values(by=['Công ty', 'Năm'])
    df_sorted['Bank_YoY_Growth'] = df_sorted.groupby('Công ty')['A13'].pct_change() * 100
    
    # Lấy trung bình tăng trưởng hàng năm của mỗi bank
    bank_avg_growth = df_sorted.groupby('Công ty')['Bank_YoY_Growth'].mean().reset_index()
    bank_avg_growth = bank_avg_growth.replace([np.inf, -np.inf], np.nan).dropna()
    bank_avg_growth = bank_avg_growth.sort_values('Bank_YoY_Growth', ascending=False)
    
    # In ra báo cáo thống kê
    print("--- THỐNG KÊ MÔ TẢ TĂNG TRƯỞNG TÍN DỤNG ---")
    print("1. Tốc độ tăng trưởng tín dụng toàn hệ thống (System YoY Growth):")
    sys_display = sys_loans[['Năm', 'A13', 'Credit_Growth_YoY']].copy()
    sys_display.columns = ['Năm', 'Tổng dư nợ (Tỷ VNĐ)', 'Tăng trưởng (%)']
    print(sys_display.to_string(index=False, float_format="%.2f"))
    
    print("\n2. Top 5 Ngân hàng có Tốc độ tăng trưởng tín dụng cao nhất (Trung bình năm):")
    print(bank_avg_growth.head(5).to_string(index=False, float_format="%.2f"))
    
    print("\n3. Top 5 Ngân hàng có Tốc độ tăng trưởng tín dụng thấp nhất (Trung bình năm):")
    print(bank_avg_growth.tail(5).to_string(index=False, float_format="%.2f"))

    # --- VẼ BIỂU ĐỒ ---
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('BÁO CÁO TĂNG TRƯỞNG VÀ CƠ CẤU TÍN DỤNG', fontsize=24, fontweight='bold', y=0.96)
    
    # Lưới 2x2
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)
    
    # Chart 1: Quy mô & Tốc độ tăng trưởng tín dụng hệ thống
    ax1 = fig.add_subplot(gs[0, 0])
    ax1_tw = ax1.twinx()
    
    sns.barplot(data=sys_loans, x='Năm', y='A13', color='#3498db', ax=ax1, alpha=0.8)
    sns.lineplot(data=sys_loans, x=np.arange(len(sys_loans)), y='Credit_Growth_YoY', 
                 color='#e74c3c', marker='o', linewidth=3, markersize=10, ax=ax1_tw)
                 
    ax1.set_title('I. Quy mô Dư nợ và Tốc độ Tăng trưởng Tín dụng Hệ thống', fontsize=16, fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('Tổng Dư nợ Cho vay (Tỷ VNĐ)', fontsize=12, color='#2980b9')
    ax1_tw.set_ylabel('Tăng trưởng Tín dụng YoY (%)', fontsize=12, color='#c0392b')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000000:,.1f} Tr'))
    ax1.grid(False)
    
    # Chart 2: Cơ cấu kỳ hạn tín dụng (Ngắn - Trung - Dài hạn)
    ax2 = fig.add_subplot(gs[0, 1])
    
    ax2.stackplot(sys_loans['Năm'], 
                  sys_loans['Short_Term_Ratio'], 
                  sys_loans['Medium_Term_Ratio'], 
                  sys_loans['Long_Term_Ratio'], 
                  labels=['Ngắn hạn', 'Trung hạn', 'Dài hạn'],
                  colors=['#2ecc71', '#f1c40f', '#9b59b6'], alpha=0.8)
                  
    ax2.set_title('II. Chuyển dịch Cơ cấu Kỳ hạn Tín dụng (%)', fontsize=16, fontweight='bold')
    ax2.set_ylabel('Tỷ trọng (%)', fontsize=12)
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper right', frameon=True)
    
    # Chart 3: LDR (Thanh khoản tín dụng)
    ax3 = fig.add_subplot(gs[1, 0])
    sys_loans['System_LDR'] = sys_loans['A13'] / sys_loans['A55'] * 100
    
    sns.lineplot(data=sys_loans, x='Năm', y='System_LDR', color='#e67e22', marker='D', linewidth=3, markersize=10, ax=ax3)
    ax3.set_title('III. Tỷ lệ Cấp tín dụng trên Nguồn vốn (LDR Hệ thống)', fontsize=16, fontweight='bold')
    ax3.set_ylabel('System LDR (%)', fontsize=12)
    ax3.axhline(85, color='red', linestyle='--', alpha=0.5, label='Mức trần quy định (85%)')
    ax3.legend()
    
    # Chart 4: Xếp hạng Tăng trưởng tín dụng của các Ngân hàng
    ax4 = fig.add_subplot(gs[1, 1])
    # Lấy top 10 tăng trưởng cao nhất và top 5 thấp nhất để biểu diễn cho đẹp
    top_banks = pd.concat([bank_avg_growth.head(10), bank_avg_growth.tail(5)])
    sns.barplot(data=top_banks, x='Bank_YoY_Growth', y='Công ty', palette='coolwarm', ax=ax4)
    
    ax4.set_title('IV. Xếp hạng Tăng trưởng Tín dụng (Trung bình hàng năm)', fontsize=16, fontweight='bold')
    ax4.set_xlabel('Tăng trưởng trung bình YoY (%)', fontsize=12)
    ax4.set_ylabel('Ngân hàng', fontsize=12)
    
    plt.tight_layout()
    os.makedirs('pictures', exist_ok=True)
    out_file = 'pictures/Credit_Growth_Analysis.png'
    plt.savefig(out_file, dpi=200, bbox_inches='tight')
    print(f"\n[THÀNH CÔNG] Đã lưu biểu đồ Tăng trưởng Tín dụng tại: {out_file}")

if __name__ == "__main__":
    main()

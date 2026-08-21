# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "numpy",
#     "scikit-learn",
#     "scipy",
# ]
# ///

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== TÌM KIẾM CÁC INSIGHT CHUYÊN SÂU MỚI ===\n")
    
    bs_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
    is_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
    note_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_3. Note.csv")

    # Đọc dữ liệu
    df_bs = pd.read_csv(bs_file)
    df_is = pd.read_csv(is_file)
    df_note = pd.read_csv(note_file)

    for df in [df_bs, df_is, df_note]:
        df['Công ty'] = df['Công ty'].astype(str)
        df['Năm'] = pd.to_numeric(df['Năm'], errors='coerce')
        
    df = df_bs.merge(df_is, on=['Công ty', 'Năm'], how='inner').merge(df_note, on=['Công ty', 'Năm'], how='inner')
    
    # Các trường quan tâm:
    # A13: Tổng dư nợ
    # B14: Tổng thu nhập hoạt động (TOI)
    # B15: Chi phí hoạt động (OPEX)
    # B17: Chi phí dự phòng rủi ro tín dụng
    # C12: Dư nợ Xây dựng
    # C28: Dư nợ Bất động sản và tư vấn
    # C35, C36, C37: Nợ xấu
    cols = ['A13', 'B14', 'B15', 'B17', 'C12', 'C28', 'C35', 'C36', 'C37']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
    df = df[df['B14'] > 0] # Lọc dữ liệu hợp lệ
    
    # --- INSIGHT 1: QUẢN TRỊ CHI PHÍ (CIR - Cost to Income Ratio) ---
    df['CIR'] = df['B15'] / df['B14'] * 100
    
    # Tính xu hướng CIR toàn hệ thống
    sys_cir = df.groupby('Năm').agg({'B15': 'sum', 'B14': 'sum'}).reset_index()
    sys_cir = sys_cir[sys_cir['Năm'] >= 2015]
    sys_cir['System_CIR'] = sys_cir['B15'] / sys_cir['B14'] * 100
    
    # Top banks hiệu quả nhất (Trung bình CIR thấp nhất)
    bank_cir = df.groupby('Công ty')['CIR'].mean().sort_values()
    
    # --- INSIGHT 2: GÁNH NẶNG DỰ PHÒNG (Provisioning Burden) ---
    # Tỷ lệ Lợi nhuận bị ăn mòn bởi dự phòng = Chi phí dự phòng / Tổng thu nhập hoạt động
    df['Provision_Burden'] = df['B17'] / df['B14'] * 100
    
    sys_prov = df.groupby('Năm').agg({'B17': 'sum', 'B14': 'sum'}).reset_index()
    sys_prov = sys_prov[sys_prov['Năm'] >= 2015]
    sys_prov['System_Prov_Burden'] = sys_prov['B17'] / sys_prov['B14'] * 100
    
    # --- INSIGHT 3: RỦI RO BẤT ĐỘNG SẢN & XÂY DỰNG (Real Estate Exposure) ---
    df['RE_Exposure'] = np.where(df['A13'] > 0, (df['C12'] + df['C28']) / df['A13'] * 100, 0)
    df['NPL_Ratio'] = np.where(df['A13'] > 0, (df['C35'] + df['C36'] + df['C37']) / df['A13'] * 100, 0)
    
    # Lấy dữ liệu 3 năm gần nhất (giai đoạn khó khăn của BĐS) để xem tương quan
    recent_years = df[df['Năm'] >= 2022].copy()
    re_risk = recent_years.groupby('Công ty').agg({
        'RE_Exposure': 'mean',
        'NPL_Ratio': 'mean',
        'Provision_Burden': 'mean'
    }).reset_index()

    print("--- 1. HIỆU QUẢ QUẢN TRỊ CHI PHÍ (CIR) ---")
    print("Xu hướng CIR toàn hệ thống (Hệ thống ngày càng hiệu quả nhờ số hóa?):")
    print(sys_cir[['Năm', 'System_CIR']].to_string(index=False, float_format="%.2f"))
    print("\nTop 5 Ngân hàng có quản trị chi phí (CIR) TỐT nhất (Trung bình):")
    print(bank_cir.head(5).to_string(float_format="%.2f"))
    print("\nTop 5 Ngân hàng có quản trị chi phí (CIR) KÉM nhất (Trung bình):")
    print(bank_cir.tail(5).to_string(float_format="%.2f"))

    print("\n--- 2. TƯƠNG QUAN BẤT ĐỘNG SẢN & RỦI RO (2022-2024) ---")
    # Tính Pearson correlation
    corr, p_value = stats.pearsonr(re_risk['RE_Exposure'], re_risk['NPL_Ratio'])
    print(f"Hệ số tương quan (Pearson) giữa Tỷ trọng vay BĐS/Xây dựng và Nợ xấu: {corr:.2f} (p-value: {p_value:.3f})")
    if p_value < 0.05 and corr > 0:
        print("=> CÓ SỰ TƯƠNG QUAN ĐÁNG KỂ: Ngân hàng cho vay BĐS/Xây dựng nhiều có xu hướng nợ xấu cao hơn rõ rệt trong giai đoạn này.")
    else:
        print("=> Không có sự tương quan thống kê rõ ràng (Có thể các khoản vay BĐS được thế chấp tốt hoặc chưa nhảy nhóm nợ).")

    # --- VẼ BIỂU ĐỒ ---
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    
    fig = plt.figure(figsize=(20, 10))
    fig.suptitle('CÁC INSIGHT CHUYÊN SÂU MỚI TỪ MAPPING', fontsize=22, fontweight='bold', y=0.98)
    
    gs = fig.add_gridspec(1, 3, wspace=0.3)
    
    # 1. Biểu đồ xu hướng CIR và Provision Burden toàn hệ thống
    ax1 = fig.add_subplot(gs[0, 0])
    sns.lineplot(data=sys_cir, x='Năm', y='System_CIR', marker='s', color='#27ae60', linewidth=3, label='Tỷ lệ CIR (%)', ax=ax1)
    sns.lineplot(data=sys_prov, x='Năm', y='System_Prov_Burden', marker='o', color='#e74c3c', linewidth=3, label='Gánh nặng Dự phòng (%)', ax=ax1)
    
    ax1.set_title('I. "Cái Giá" Của Lợi Nhuận', fontsize=15, fontweight='bold')
    ax1.set_ylabel('Tỷ lệ phần trăm / Tổng Thu nhập (%)', fontsize=12)
    ax1.set_xlabel('Năm', fontsize=12)
    ax1.annotate('CIR giảm = Tối ưu chi phí tốt hơn', xy=(2020, sys_cir['System_CIR'].mean()), 
                 xytext=(2015, sys_cir['System_CIR'].mean()-5), arrowprops=dict(arrowstyle="->", color='#27ae60'))
                 
    # 2. Xếp hạng CIR theo Ngân hàng
    ax2 = fig.add_subplot(gs[0, 1])
    top_bot_cir = pd.concat([bank_cir.head(10), bank_cir.tail(5)]).reset_index()
    sns.barplot(data=top_bot_cir, y='Công ty', x='CIR', palette='viridis', ax=ax2)
    ax2.set_title('II. Xếp hạng Quản trị Chi phí (CIR)', fontsize=15, fontweight='bold')
    ax2.set_xlabel('Tỷ lệ CIR Trung bình (%)', fontsize=12)
    ax2.set_ylabel('Ngân hàng', fontsize=12)
    ax2.axvline(bank_cir.mean(), color='red', linestyle='--', label=f'Trung bình HT ({bank_cir.mean():.1f}%)')
    ax2.legend()
    
    # 3. Scatter Plot: Phơi nhiễm BĐS/Xây dựng vs Nợ xấu (2022-2024)
    ax3 = fig.add_subplot(gs[0, 2])
    sns.regplot(data=re_risk, x='RE_Exposure', y='NPL_Ratio', scatter_kws={'s': 100, 'alpha':0.7, 'color':'#2980b9'}, line_kws={'color':'red'}, ax=ax3)
    
    for i, row in re_risk.iterrows():
        # Chỉ đánh dấu các ngân hàng quá nổi bật
        if row['RE_Exposure'] > re_risk['RE_Exposure'].quantile(0.8) or row['NPL_Ratio'] > re_risk['NPL_Ratio'].quantile(0.8):
            ax3.annotate(row['Công ty'], (row['RE_Exposure'], row['NPL_Ratio']), xytext=(5, 5), textcoords='offset points')
            
    ax3.set_title('III. Rủi ro Phơi nhiễm Bất động sản (22-24)', fontsize=15, fontweight='bold')
    ax3.set_xlabel('Tỷ trọng Dư nợ BĐS & Xây dựng (%)', fontsize=12)
    ax3.set_ylabel('Tỷ lệ Nợ xấu trung bình (%)', fontsize=12)
    
    plt.tight_layout()
    os.makedirs(FIGURES_S, exist_ok=True)
    out_file = os.path.join(FIGURES_S, "Advanced_Insights.png")
    plt.savefig(out_file, dpi=200, bbox_inches='tight')
    print(f"\n[THÀNH CÔNG] Đã lưu biểu đồ Insight mới tại: {out_file}")

if __name__ == "__main__":
    main()

# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "scikit-learn",
#     "numpy",
# ]
# ///

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.patches as mpatches

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
    is_file = str(DATA / "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
    
    df = pd.read_csv(is_file)
    df['Công ty'] = df['Công ty'].astype(str)
    
    # B3: Thu nhập lãi thuần, B14: Tổng thu nhập hoạt động
    cols = ['B3', 'B14']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
    # Tính trung bình B3 và B14 qua các năm của mỗi ngân hàng
    df_bank = df.groupby('Công ty').agg({'B3': 'mean', 'B14': 'mean'}).reset_index()
    
    # Thu nhập ngoài lãi = Tổng thu nhập (B14) - Thu nhập lãi thuần (B3)
    df_bank['Non_Interest'] = df_bank['B14'] - df_bank['B3']
    
    # Tính Fee Ratio (%)
    df_bank['Fee_Ratio'] = np.where(df_bank['B14'] > 0, df_bank['Non_Interest'] / df_bank['B14'] * 100, 0)
    
    # Loại bỏ các dòng bị lỗi (Fee Ratio không hợp lệ)
    df_bank = df_bank[(df_bank['Fee_Ratio'] >= 0) & (df_bank['Fee_Ratio'] <= 100)]
    
    # Áp dụng thuật toán K-Means Clustering để chia thành 3 nhóm đa dạng hóa
    X = df_bank[['Fee_Ratio']]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_bank['Cluster'] = kmeans.fit_predict(X)
    
    # Sắp xếp lại thứ tự Cluster sao cho 0 là Thấp, 1 là Trung bình, 2 là Cao
    centers = df_bank.groupby('Cluster')['Fee_Ratio'].mean().sort_values()
    cluster_mapping = {old_label: new_label for new_label, old_label in enumerate(centers.index)}
    df_bank['Cluster'] = df_bank['Cluster'].map(cluster_mapping)
    
    labels_map = {
        0: 'Phụ thuộc Tín dụng (Thấp)', 
        1: 'Đa dạng hóa Trung bình', 
        2: 'Đa dạng hóa Tốt (Cao)'
    }
    df_bank['Group_Name'] = df_bank['Cluster'].map(labels_map)
    
    # Sắp xếp df_bank theo Fee Ratio để vẽ Bar chart cho đẹp
    df_bank = df_bank.sort_values(by='Fee_Ratio', ascending=True)
    
    # Setup vẽ biểu đồ
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    fig.suptitle('PHÂN NHÓM NGÂN HÀNG THEO TỈ LỆ ĐA DẠNG HÓA DOANH THU (FEE INCOME RATIO)', fontsize=22, fontweight='bold', y=0.98)
    
    palette = {0: '#e74c3c', 1: '#f1c40f', 2: '#2ecc71'} # Đỏ, Vàng, Xanh lá
    
    # --- Biểu đồ 1: Bar chart ---
    sns.barplot(data=df_bank, x='Fee_Ratio', y='Công ty', hue='Cluster', palette=palette, dodge=False, ax=ax1)
    
    ax1.set_title('I. Bảng xếp hạng Tỉ lệ Thu nhập ngoài lãi (%)', fontsize=16, fontweight='bold', pad=15)
    ax1.set_xlabel('Tỉ lệ Thu nhập ngoài lãi - Fee Ratio (%)', fontsize=13)
    ax1.set_ylabel('Mã Ngân hàng (Công ty)', fontsize=13)
    
    # Custom Legend cho Bar Chart
    handles = [mpatches.Patch(color=palette[i], label=labels_map[i]) for i in range(3)]
    ax1.legend(handles=handles, title='Mức độ đa dạng hóa', loc='lower right', fontsize=11, title_fontsize=12)
    
    # --- Biểu đồ 2: Scatter plot (Quy mô vs Đa dạng hóa) ---
    for cluster_id in range(3):
        subset = df_bank[df_bank['Cluster'] == cluster_id]
        ax2.scatter(subset['B14'], subset['Fee_Ratio'], 
                    color=palette[cluster_id], 
                    s=np.clip(subset['B14']/50, 100, 1500), # Bong bóng dựa vào quy mô TOI
                    label=labels_map[cluster_id], alpha=0.8, edgecolors='black', linewidth=1)
        
        # Thêm tên ngân hàng vào bong bóng
        for _, row in subset.iterrows():
            ax2.annotate(row['Công ty'], (row['B14'], row['Fee_Ratio']), 
                         xytext=(6, 6), textcoords='offset points', fontsize=10, fontweight='bold')
            
    # Vẽ đường trung bình
    ax2.axhline(df_bank['Fee_Ratio'].median(), color='gray', linestyle='--', alpha=0.5)
    
    ax2.set_title('II. Tương quan giữa Quy mô Doanh thu và Đa dạng hóa', fontsize=16, fontweight='bold', pad=15)
    ax2.set_xlabel('Tổng Thu nhập hoạt động trung bình (Tỷ VNĐ)', fontsize=13)
    ax2.set_ylabel('Tỉ lệ Thu nhập ngoài lãi - Fee Ratio (%)', fontsize=13)
    ax2.legend(title='Phân Nhóm', fontsize=11, title_fontsize=12)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9) # Tạo khoảng trống cho suptitle
    
    # Lưu file
    os.makedirs(FIGURES_S, exist_ok=True)
    out_file = os.path.join(FIGURES_S, "Revenue_Diversification_Clusters.png")
    plt.savefig(out_file, dpi=200, bbox_inches='tight')
    print(f"Saved: {out_file}")
    
    # In ra báo cáo text
    print("=== KẾT QUẢ PHÂN NHÓM ĐA DẠNG HÓA DOANH THU ===")
    for cluster_id in range(2, -1, -1): # In từ cao xuống thấp
        banks = df_bank[df_bank['Cluster'] == cluster_id]['Công ty'].tolist()
        avg_ratio = df_bank[df_bank['Cluster'] == cluster_id]['Fee_Ratio'].mean()
        print(f"\nNhóm: {labels_map[cluster_id]}")
        print(f"- Tỉ lệ trung bình nhóm: {avg_ratio:.2f}%")
        print(f"- Các ngân hàng: {', '.join(banks)}")

if __name__ == "__main__":
    main()

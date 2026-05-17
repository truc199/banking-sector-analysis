# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "scikit-learn",
#     "matplotlib",
# ]
# ///

import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== BẮT ĐẦU PHÂN TÍCH DỮ LIỆU NỢ XẤU ===\n")
    
    file_path = "[G'Contest 2026] Đề Vòng 2_3. Note.csv"
    if not os.path.exists(file_path):
        print("Không tìm thấy file dữ liệu.")
        return

    df = pd.read_csv(file_path)
    
    # Các cột nợ
    # C33: Đủ tiêu chuẩn, C34: Cần chú ý, C35: Dưới tiêu chuẩn, C36: Nghi ngờ, C37: Mất vốn
    cols = ['C33', 'C34', 'C35', 'C36', 'C37']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    # Tính Tổng dư nợ và Nợ xấu (NPL - Non-Performing Loan: Nhóm 3, 4, 5)
    df['Total_Loans'] = df[cols].sum(axis=1)
    df['NPL_Amount'] = df['C35'] + df['C36'] + df['C37']
    df['NPL_Ratio'] = np.where(df['Total_Loans'] > 0, df['NPL_Amount'] / df['Total_Loans'] * 100, 0)
    df['C34_Ratio'] = np.where(df['Total_Loans'] > 0, df['C34'] / df['Total_Loans'] * 100, 0) # Tỷ lệ nợ cần chú ý
    
    # Lọc bỏ các dòng không có dư nợ để tránh nhiễu
    df_clean = df[df['Total_Loans'] > 0].copy()

    # ---------------------------------------------------------
    # 1. THỐNG KÊ MÔ TẢ (DESCRIPTIVE STATISTICS)
    # ---------------------------------------------------------
    print("1. THỐNG KÊ TỔNG QUAN HÀNG NĂM (SYSTEM TREND):")
    yearly_trend = df_clean.groupby('Năm').agg({
        'NPL_Ratio': 'mean',
        'Total_Loans': 'sum'
    }).reset_index()
    print(yearly_trend.to_string(index=False, float_format="%.2f"))
    print("\n=> Insight: Nhìn vào xu hướng trung bình Tỷ lệ Nợ Xấu (NPL_Ratio) qua các năm để thấy sức khỏe chung của hệ thống ngân hàng.\n")

    print("2. TOP NGÂN HÀNG RỦI RO CAO NHẤT VÀ THẤP NHẤT (Dựa trên NPL trung bình):")
    bank_npl = df_clean.groupby('Công ty')['NPL_Ratio'].mean().sort_values(ascending=False)
    print(f"- Top 3 Ngân hàng có NPL cao nhất:\n{bank_npl.head(3).to_string(float_format='%.2f')}")
    print(f"- Top 3 Ngân hàng có NPL thấp nhất:\n{bank_npl.tail(3).to_string(float_format='%.2f')}\n")

    # ---------------------------------------------------------
    # 2. PHÂN CỤM NGÂN HÀNG (CLUSTERING) VỚI K-MEANS
    # ---------------------------------------------------------
    print("3. PHÂN CỤM NGÂN HÀNG THEO RỦI RO (K-Means Clustering):")
    # Feature engineering cho phân cụm: lấy trung bình NPL_Ratio và C34_Ratio của mỗi ngân hàng qua các năm
    bank_features = df_clean.groupby('Công ty').agg({
        'NPL_Ratio': 'mean',
        'C34_Ratio': 'mean' # Nợ nhóm 2 (Nợ cần chú ý) - chỉ báo sớm của nợ xấu
    }).dropna()

    if len(bank_features) >= 3:
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        bank_features['Cluster'] = kmeans.fit_predict(bank_features)
        
        # Sắp xếp lại cluster label sao cho cluster 0 là thấp, 2 là cao
        cluster_centers = bank_features.groupby('Cluster')['NPL_Ratio'].mean().sort_values()
        mapping = {old_label: new_label for new_label, old_label in enumerate(cluster_centers.index)}
        bank_features['Cluster'] = bank_features['Cluster'].map(mapping)
        
        cluster_names = {0: "An toàn / Ít rủi ro", 1: "Trung bình / Cần theo dõi", 2: "Rủi ro cao"}
        bank_features['Risk_Profile'] = bank_features['Cluster'].map(cluster_names)
        
        for cluster_id in range(3):
            banks_in_cluster = bank_features[bank_features['Cluster'] == cluster_id].index.tolist()
            print(f"- Nhóm {cluster_names[cluster_id]}: {banks_in_cluster}")
        print("\n=> Insight: Các ngân hàng trong 'Nhóm rủi ro cao' thường có cả tỷ lệ nợ nhóm 2 và nợ nhóm 3-5 cao hơn mặt bằng chung.\n")
        
        # Vẽ biểu đồ phân cụm
        os.makedirs('pictures', exist_ok=True)
        plt.figure(figsize=(10, 6))
        colors = ['green', 'orange', 'red']
        for cluster_id in range(3):
            cluster_data = bank_features[bank_features['Cluster'] == cluster_id]
            plt.scatter(cluster_data['C34_Ratio'], cluster_data['NPL_Ratio'], 
                        c=colors[cluster_id], label=cluster_names[cluster_id], s=100, alpha=0.7)
            for bank_id in cluster_data.index:
                plt.annotate(bank_id, (cluster_data.loc[bank_id, 'C34_Ratio'], cluster_data.loc[bank_id, 'NPL_Ratio']))
                
        plt.title('Phân cụm Ngân hàng theo Rủi ro Tín dụng')
        plt.xlabel('Tỷ lệ Nợ cần chú ý (Nhóm 2) trung bình %')
        plt.ylabel('Tỷ lệ Nợ xấu (Nhóm 3-5) trung bình %')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('pictures/Cluster_Risk_Profile.png', dpi=150)
        print("Đã lưu biểu đồ phân cụm rủi ro tại pictures/Cluster_Risk_Profile.png")

    # ---------------------------------------------------------
    # 3. PHÁT HIỆN BẤT THƯỜNG (ANOMALY DETECTION) VỚI ISOLATION FOREST
    # ---------------------------------------------------------
    print("\n4. PHÁT HIỆN ĐIỂM BẤT THƯỜNG (Isolation Forest):")
    print("Mục đích: Tìm ra những năm mà một ngân hàng cụ thể có sự biến động nợ xấu đột biến so với bình thường.")
    
    features = ['NPL_Ratio', 'C34_Ratio']
    iso_forest = IsolationForest(contamination=0.05, random_state=42) # Giả sử 5% dữ liệu là bất thường
    df_clean['Anomaly'] = iso_forest.fit_predict(df_clean[features])
    
    anomalies = df_clean[df_clean['Anomaly'] == -1]
    
    if not anomalies.empty:
        result_anomalies = anomalies[['Công ty', 'Năm', 'NPL_Ratio', 'C34_Ratio']].sort_values(by='NPL_Ratio', ascending=False)
        print("Các quan sát bất thường (NPL hoặc C34 quá cao/biến động mạnh):")
        print(result_anomalies.head(10).to_string(index=False, float_format="%.2f"))
        print("\n=> Insight: Các thời điểm bất thường này có thể do ngân hàng gặp khủng hoảng riêng, hoặc thay đổi quy định phân loại nợ.")
    else:
        print("Không phát hiện điểm bất thường đáng kể nào.")

    print("\n=== HOÀN TẤT PHÂN TÍCH ===")

if __name__ == "__main__":
    main()

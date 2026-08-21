import os
import sys
import glob
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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

def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== TÍNH TOÁN K-MEANS CLUSTERING CHÍNH XÁC CHO 27 NGÂN HÀNG ===")
    
    # Load files
    BS_FILE   = glob.glob(str(DATA / "*Balance*"))[0]
    IS_FILE   = glob.glob(str(DATA / "*Income*"))[0]
    NOTE_FILE = glob.glob(str(DATA / "*Note*"))[0]
    
    bs = pd.read_csv(BS_FILE)
    ic = pd.read_csv(IS_FILE)
    note = pd.read_csv(NOTE_FILE)
    
    # Merge BS, IS, Note
    df = bs.merge(ic, on=['Công ty', 'Năm'], how='outer')
    df = df.merge(note, on=['Công ty', 'Năm'], how='outer')
    
    # Convert numeric
    for c in df.columns:
        if c not in ['Công ty', 'Năm']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
            
    # Compute the 6 variables
    df['ROA'] = safe_div(df['B22'], df['A1'])
    npl_sum = df[['C35','C36','C37']].sum(axis=1)
    df['NPL'] = safe_div(npl_sum, df['A13'])
    df['CASA'] = safe_div(df['C68'], df['A55'])
    df['CIR'] = safe_div(df['B15'], df['B14'])
    df['NIM'] = safe_div(df['B3'], df['A1'])
    df['LDR'] = safe_div(df['A13'], df['A55'])
    
    features = ['ROA', 'NPL', 'CASA', 'CIR', 'NIM', 'LDR']
    
    periods = {
        'Phase 1 (2020-2021)': [2020, 2021],
        'Phase 2 (2022-2023)': [2022, 2023],
        'Phase 3 (2024)': [2024]
    }
    
    results = {}
    
    for name, years in periods.items():
        print(f"\n--- {name} ---")
        p_df = df[df['Năm'].isin(years)].groupby('Công ty')[features].mean().reset_index()
        
        # Check and fillna
        p_df[features] = p_df[features].fillna(p_df[features].mean())
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(p_df[features])
        
        # KMeans clustering (K=4)
        # We set random_state=42 for reproducibility
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        p_df['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # PCA projection to 2D
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        p_df['PC1'] = X_pca[:, 0]
        p_df['PC2'] = X_pca[:, 1]
        
        # Map cluster profiles to human readable labels (🟢 Ngôi sao, 🔵 Ổn định, 🟡 Chuyển đổi, 🔴 Cần giám sát)
        # Cluster categorization based on ROA and NPL:
        # We can analyze the cluster centroids to assign names
        centroids = p_df.groupby('Cluster')[['ROA', 'NPL', 'CASA', 'CIR']].mean()
        print("Centroids of clusters:")
        print(centroids.to_string())
        
        # Map cluster IDs to labels based on rank of ROA (descending) and NPL (ascending)
        # Top ROA = Star, Second ROA = Stable, Third ROA/High NPL = Transition/Monitor
        sorted_by_roa = centroids.sort_values(by='ROA', ascending=False).index.tolist()
        
        cluster_labels = {}
        cluster_labels[sorted_by_roa[0]] = '🟢 Star (Ngôi sao)'
        cluster_labels[sorted_by_roa[1]] = '🔵 Stable (Ổn định)'
        
        # Of the remaining two, the one with higher NPL is Monitor, other is Transition
        rem_0, rem_1 = sorted_by_roa[2], sorted_by_roa[3]
        if centroids.loc[rem_0, 'NPL'] > centroids.loc[rem_1, 'NPL']:
            cluster_labels[rem_0] = '🔴 Monitor (Cần giám sát)'
            cluster_labels[rem_1] = '🟡 Transition (Chuyển đổi)'
        else:
            cluster_labels[rem_0] = '🟡 Transition (Chuyển đổi)'
            cluster_labels[rem_1] = '🔴 Monitor (Cần giám sát)'
            
        p_df['Cluster_Name'] = p_df['Cluster'].map(cluster_labels)
        
        print("\nBank Assignments:")
        for name_label in ['🟢 Star (Ngôi sao)', '🔵 Stable (Ổn định)', '🟡 Transition (Chuyển đổi)', '🔴 Monitor (Cần giám sát)']:
            banks = p_df[p_df['Cluster_Name'] == name_label]['Công ty'].tolist()
            print(f"  {name_label}: NH {', NH '.join(map(str, sorted(banks)))}")
            
        results[name] = p_df
        
if __name__ == '__main__':
    main()

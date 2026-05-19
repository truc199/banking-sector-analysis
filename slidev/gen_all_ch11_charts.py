import os
import sys
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=== DỰNG BIỂU ĐỒ RADAR TÁCH 4 CỤM RIÊNG BIỆT NĂM 2024 ===")
    
    # 1. Load data
    BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
    IS_FILE   = glob.glob(r'd:\uni\gcontest\*Income*')[0]
    NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
    
    bs = pd.read_csv(BS_FILE)
    ic = pd.read_csv(IS_FILE)
    note = pd.read_csv(NOTE_FILE)
    
    df = bs.merge(ic, on=['Công ty', 'Năm'], how='outer')
    df = df.merge(note, on=['Công ty', 'Năm'], how='outer')
    
    for c in df.columns:
        if c not in ['Công ty', 'Năm']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
            
    # Compute the 6 variables
    df['ROA'] = safe_div(df['B22'], df['A1'])
    npl_sum = df[['C35','C36','C37']].sum(axis=1)
    df['NPL'] = safe_div(npl_sum, df['A13'])
    df['CASA'] = safe_div(df['C68'], df['A55'])
    # Convert CIR to positive
    df['CIR'] = np.abs(safe_div(df['B15'], df['B14']))
    df['NIM'] = safe_div(df['B3'], df['A1'])
    df['LDR'] = safe_div(df['A13'], df['A55'])
    
    features = ['ROA', 'NPL', 'CASA', 'CIR', 'NIM', 'LDR']
    
    # Filter 2024
    df_2024 = df[df['Năm'] == 2024].groupby('Công ty')[features].mean().reset_index()
    
    # Fill NAs
    df_2024[features] = df_2024[features].fillna(df_2024[features].mean())
    
    # Standardize for KMeans clustering
    from sklearn.preprocessing import StandardScaler
    scaler_std = StandardScaler()
    X_scaled_std = scaler_std.fit_transform(df_2024[features])
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df_2024['Cluster'] = kmeans.fit_predict(X_scaled_std)
    
    # Map cluster names
    centroids = df_2024.groupby('Cluster')[features].mean()
    sorted_by_roa = centroids.sort_values(by='ROA', ascending=False).index.tolist()
    
    cluster_labels = {}
    cluster_labels[sorted_by_roa[0]] = 'Ngôi sao (Star)'
    cluster_labels[sorted_by_roa[1]] = 'Ổn định (Stable)'
    
    rem_0, rem_1 = sorted_by_roa[2], sorted_by_roa[3]
    if centroids.loc[rem_0, 'NPL'] > centroids.loc[rem_1, 'NPL']:
        cluster_labels[rem_0] = 'Cần giám sát (Monitor)'
        cluster_labels[rem_1] = 'Chuyển đổi (Transition)'
    else:
        cluster_labels[rem_0] = 'Chuyển đổi (Transition)'
        cluster_labels[rem_1] = 'Cần giám sát (Monitor)'
        
    df_2024['Cluster_Name'] = df_2024['Cluster'].map(cluster_labels)
    
    # 2. Min-Max Normalization
    scaler_mm = MinMaxScaler()
    df_2024_norm = df_2024.copy()
    df_2024_norm[features] = scaler_mm.fit_transform(df_2024[features])
    
    # Calculate normalized centroids for each cluster
    norm_centroids = df_2024_norm.groupby('Cluster_Name')[features].mean()
    
    # Set up matplotlib style matching premium theme
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.6
    
    labels = ['ROA', 'NPL', 'CASA', 'CIR', 'NIM', 'LDR']
    num_vars = len(labels)
    
    # Angles for radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Close the loop
    
    # Create 2x2 grid of polar subplots
    fig, axs = plt.subplots(2, 2, figsize=(4.8, 4.8), subplot_kw=dict(projection='polar'), dpi=300)
    
    # Cluster configuration (removed emojis to avoid broken characters)
    cluster_configs = [
        ('Ngôi sao (Star)', axs[0, 0], '#10B981', 'Cụm 1: Ngôi sao (Star)'),
        ('Ổn định (Stable)', axs[0, 1], '#003366', 'Cụm 2: Ổn định (Stable)'),
        ('Chuyển đổi (Transition)', axs[1, 0], '#E67E22', 'Cụm 3: Chuyển đổi (Transition)'),
        ('Cần giám sát (Monitor)', axs[1, 1], '#C0392B', 'Cụm 4: Cần giám sát (Monitor)')
    ]
    
    for cluster_name, ax, color, title in cluster_configs:
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Grid variables and labels with very clean tiny font size
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color='#475569', fontweight='bold', fontsize=5.8)
        
        # Grid customization
        ax.grid(True, color='#E2E8F0', linestyle='--', linewidth=0.5)
        
        # Common radial limits (scaled from 0 to 1.1)
        ax.set_ylim(0, 1.1)
        # Hide standard polar radial values to avoid clutter
        ax.set_yticklabels([])
        
        # Retrieve values and plot
        if cluster_name in norm_centroids.index:
            values = norm_centroids.loc[cluster_name].values.tolist()
            values += values[:1]  # Close loop
            
            # Plot solid outline
            ax.plot(angles, values, color=color, linewidth=1.2, linestyle='-', zorder=4)
            # Fill region with low opacity
            ax.fill(angles, values, color=color, alpha=0.15, zorder=3)
            # Plot individual vertices
            ax.scatter(angles[:-1], values[:-1], color=color, s=10, edgecolor='w', linewidths=0.3, zorder=5)
            
        # Clean compact title for each subplot
        ax.set_title(title, fontweight='bold', fontsize=7.5, color='#1E293B', pad=10)
        
    plt.suptitle('A. Radar Profiles: Phân tích Riêng Biệt 4 Cụm Ngân Hàng (2024)\n(Chỉ số đã chuẩn hóa Min-Max trên cùng hệ trục so sánh)', 
                 fontweight='bold', fontsize=8.5, color='#1E293B', y=0.98)
    
    plt.tight_layout()
    
    public_dir = r'd:\uni\gcontest\slidev\public'
    os.makedirs(public_dir, exist_ok=True)
    path = os.path.join(public_dir, 'slide_13_radar_profile.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path} successfully!")

if __name__ == '__main__':
    main()

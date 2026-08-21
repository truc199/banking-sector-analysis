import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

# --- Đường dẫn tương đối theo vị trí file (không phụ thuộc máy) ---
import sys as _sys
_sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
PUBLIC = ROOT / "slidev" / "public"
FONTS = ROOT / "slidev" / "fonts"
# ------------------------------------------------------------------

# Setup fonts
for font_file in glob.glob(str(FONTS / "*.ttf")):
    try:
        fm.fontManager.addfont(font_file)
    except Exception:
        pass

plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

public_dir = str(PUBLIC)
os.makedirs(public_dir, exist_ok=True)

# Helper function
def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

# Load data
bs_df = pd.read_csv(glob.glob(str(DATA / "*Balance*"))[0])
inc_df = pd.read_csv(glob.glob(str(DATA / "*Income*"))[0])
note_df = pd.read_csv(glob.glob(str(DATA / "*Note*"))[0])

for df in [bs_df, inc_df, note_df]:
    for col in df.columns:
        if col not in ['Công ty', 'Năm']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

m_df = bs_df.merge(inc_df, on=['Công ty', 'Năm']).merge(note_df, on=['Công ty', 'Năm'])

# Compute the 6 variables
m_df['ROA'] = safe_div(m_df['B22'], m_df['A1'])
npl_sum = m_df[['C35','C36','C37']].sum(axis=1)
m_df['NPL'] = safe_div(npl_sum, m_df['A13'])
m_df['CASA'] = safe_div(m_df['C68'], m_df['A55'])
m_df['CIR'] = safe_div(m_df['B15'], m_df['B14'])
m_df['NIM'] = safe_div(m_df['B3'], m_df['A1'])
m_df['LDR'] = safe_div(m_df['A13'], m_df['A55'])

features = ['ROA', 'NPL', 'CASA', 'CIR', 'NIM', 'LDR']

periods = [
    {
        'years': [2020, 2021],
        'title': 'GĐ1 (2020-2021): COVID-19 & CASA thống trị',
        'color_key': 'phase1'
    },
    {
        'years': [2022, 2023],
        'title': 'GĐ2 (2022-2023): Chuyển giao & Thắt chặt tiền tệ',
        'color_key': 'phase2'
    },
    {
        'years': [2024],
        'title': 'GĐ3 (2024): Tái cân bằng & Phân hóa nợ xấu',
        'color_key': 'phase3'
    }
]

# Set up 3 horizontal subplots (full-width layout)
fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.2), dpi=350)
plt.subplots_adjust(wspace=0.20, bottom=0.24)

from adjustText import adjust_text

for idx, p_info in enumerate(periods):
    ax = axes[idx]
    years = p_info['years']
    
    # Filter and group
    p_df = m_df[m_df['Năm'].isin(years)].groupby('Công ty')[features].mean().reset_index()
    p_df[features] = p_df[features].fillna(p_df[features].mean())
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(p_df[features])
    
    # KMeans (K=4)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    p_df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # PCA to 2D
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    p_df['PC1'] = X_pca[:, 0]
    p_df['PC2'] = X_pca[:, 1]
    
    # Explained variance
    dim1_pct = pca.explained_variance_ratio_[0] * 100
    dim2_pct = pca.explained_variance_ratio_[1] * 100
    
    # Map cluster centroids to names to maintain consistent coloring
    centroids = p_df.groupby('Cluster')[['ROA', 'NPL', 'CASA', 'CIR']].mean()
    sorted_by_roa = centroids.sort_values(by='ROA', ascending=False).index.tolist()
    
    cluster_props = {}
    # Top ROA = Star
    cluster_props[sorted_by_roa[0]] = {'color': '#10B981', 'marker': 'o', 'label': 'Cụm 1 (Ngôi sao - Star)'}
    # Second ROA = Stable
    cluster_props[sorted_by_roa[1]] = {'color': '#003366', 'marker': '^', 'label': 'Cụm 2 (Ổn định - Stable)'}
    
    rem_0, rem_1 = sorted_by_roa[2], sorted_by_roa[3]
    if centroids.loc[rem_0, 'NPL'] > centroids.loc[rem_1, 'NPL']:
        cluster_props[rem_0] = {'color': '#C0392B', 'marker': 'd', 'label': 'Cụm 4 (Cần giám sát - Monitor)'}
        cluster_props[rem_1] = {'color': '#E67E22', 'marker': 's', 'label': 'Cụm 3 (Chuyển đổi - Transition)'}
    else:
        cluster_props[rem_0] = {'color': '#E67E22', 'marker': 's', 'label': 'Cụm 3 (Chuyển đổi - Transition)'}
        cluster_props[rem_1] = {'color': '#C0392B', 'marker': 'd', 'label': 'Cụm 4 (Cần giám sát - Monitor)'}
        
    ax.set_facecolor('#f8fafc')
    ax.grid(True, color='white', linestyle='-', linewidth=1.0, zorder=0)
    ax.grid(True, color='#e2e8f0', linestyle='--', linewidth=0.5, zorder=1)
    
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    ax.set_title(p_info['title'], fontweight='bold', fontsize=9.0, color='#0f172a', pad=8)
    ax.set_xlabel(f"Thành phần chính 1 (PC1: {dim1_pct:.1f}%)", fontsize=7.5, color='#475569')
    ax.set_ylabel(f"Thành phần chính 2 (PC2: {dim2_pct:.1f}%)", fontsize=7.5, color='#475569')
    ax.tick_params(colors='#64748b', labelsize=7)
    
    texts = []
    
    # Plot convex hulls and points
    for cluster_id, props in cluster_props.items():
        c_df = p_df[p_df['Cluster'] == cluster_id]
        if len(c_df) == 0:
            continue
            
        color = props['color']
        marker = props['marker']
        points = c_df[['PC1', 'PC2']].values
        
        # Convex Hull Polygon
        if len(points) >= 3:
            try:
                hull = ConvexHull(points)
                hull_points = points[hull.vertices]
                polygon = Polygon(hull_points, closed=True, facecolor=color, edgecolor=color, alpha=0.10, linewidth=0.8, zorder=2)
                ax.add_patch(polygon)
                ax.plot(np.append(hull_points[:, 0], hull_points[0, 0]), 
                        np.append(hull_points[:, 1], hull_points[0, 1]), 
                        color=color, linewidth=0.6, alpha=0.4, zorder=3)
            except Exception:
                pass
        elif len(points) == 2:
            ax.plot(points[:, 0], points[:, 1], color=color, linewidth=0.6, alpha=0.3, zorder=3)
            
        # Plot points
        ax.scatter(c_df['PC1'], c_df['PC2'], color=color, marker=marker, s=35, edgecolor='w', linewidths=0.5, zorder=4)
        
        # Collect labels for adjustText
        for _, row in c_df.iterrows():
            bank_id = str(int(row['Công ty']))
            t = ax.text(row['PC1'], row['PC2'], bank_id, fontsize=6.2, fontweight='bold', color=color, ha='center', va='center', zorder=5)
            texts.append(t)
            
    # Adjust all label positions for this subplot
    adjust_text(texts, ax=ax, force_points=0.2, force_text=0.2, expand_points=(1.2, 1.2), expand_text=(1.2, 1.2),
                arrowprops=dict(arrowstyle="-", color='#94a3b8', lw=0.4, alpha=0.5))

# Common shared legend at the bottom of the figure with detailed metrics definitions
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#10B981', markersize=7, 
           label='Cụm 1 (Ngôi sao - Star): ROA ~1.62%, NPL ~1.50%, CASA ~27.51%, NIM ~3.02%, LDR ~107.73%'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#003366', markersize=7, 
           label='Cụm 2 (Ổn định - Stable): ROA ~1.60%, NPL ~2.71%, CASA ~13.73%, NIM ~3.71%, LDR ~120.41%'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#E67E22', markersize=7, 
           label='Cụm 3 (Chuyển đổi - Transition): ROA ~0.83%, NPL ~2.48%, CASA ~9.38%, NIM ~2.53%, LDR ~97.76%'),
    Line2D([0], [0], marker='d', color='w', markerfacecolor='#C0392B', markersize=7, 
           label='Cụm 4 (Cần giám sát - Monitor): ROA < 0% (~ -4.33%), NPL ~19.54%, CASA ~9.45%, NIM ~ -1.50%, LDR ~74.05%')
]

# Adjust layout to make room for legend
plt.tight_layout(rect=[0, 0.16, 1, 0.98])
fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=2, frameon=False, fontsize=7.2)

path = os.path.join(public_dir, 'new_slide_9_1_horizontal_pca.png')
plt.savefig(path, dpi=350, bbox_inches='tight', transparent=True)
plt.close()
print("Saved Slide 9.1 Horizontal PCA K-Means space map successfully!")

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

# Set font style and parameters for high-end professional reports
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#E2E8F0'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

public_dir = r'd:\uni\gcontest\slidev\public'
os.makedirs(public_dir, exist_ok=True)

# Branding Color Palette
PRIMARY_NAVY = '#003366'
DARK_BLUE = '#004C99'
DODGER_BLUE = '#3399FF'
LIGHT_BLUE = '#66B2FF'
BABY_BLUE = '#99CCFF'

CLUSTER_STAR = '#10B981'     # Emerald Green
CLUSTER_STABLE = '#003366'   # Navy Blue
CLUSTER_TRANS = '#E67E22'    # Orange
CLUSTER_MONITOR = '#C0392B'  # Brick Red

# ----------------------------------------------------
# CHART 9.1: 3 Separate PCA K-Means Convex Hull Maps for 3 Phases (EXACT MATHEMATICAL)
# ----------------------------------------------------
def gen_chart_9_1():
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from scipy.spatial import ConvexHull
    from matplotlib.patches import Polygon
    from matplotlib.lines import Line2D
    
    # Load files
    BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
    IS_FILE   = glob.glob(r'd:\uni\gcontest\*Income*')[0]
    NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
    
    bs = pd.read_csv(BS_FILE)
    ic = pd.read_csv(IS_FILE)
    note = pd.read_csv(NOTE_FILE)
    
    df = bs.merge(ic, on=['Công ty', 'Năm'], how='outer')
    df = df.merge(note, on=['Công ty', 'Năm'], how='outer')
    
    # Convert numeric
    for c in df.columns:
        if c not in ['Công ty', 'Năm']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
            
    # Compute 6 variables
    df['ROA'] = safe_div(df['B22'], df['A1'])
    npl_sum = df[['C35','C36','C37']].sum(axis=1)
    df['NPL'] = safe_div(npl_sum, df['A13'])
    df['CASA'] = safe_div(df['C68'], df['A55'])
    df['CIR'] = safe_div(df['B15'], df['B14'])
    df['NIM'] = safe_div(df['B3'], df['A1'])
    df['LDR'] = safe_div(df['A13'], df['A55'])
    
    features = ['ROA', 'NPL', 'CASA', 'CIR', 'NIM', 'LDR']
    
    periods = {
        'phase1': {
            'years': [2020, 2021],
            'title': 'Phân cụm vị thế: Giai đoạn 1 (2020-2021) - Khủng hoảng COVID-19',
            'filename': 'slide_9_1a_phase1_map.png'
        },
        'phase2': {
            'years': [2022, 2023],
            'title': 'Phân cụm vị thế: Giai đoạn 2 (2022-2023) - Phục hồi & Thắt chặt',
            'filename': 'slide_9_1b_phase2_map.png'
        },
        'phase3': {
            'years': [2024],
            'title': 'Phân cụm vị thế: Giai đoạn 3 (2024) - Tái cân bằng & Phân hóa',
            'filename': 'slide_9_1c_phase3_map.png'
        }
    }
    
    for phase_key, info in periods.items():
        years = info['years']
        p_df = df[df['Năm'].isin(years)].groupby('Công ty')[features].mean().reset_index()
        p_df[features] = p_df[features].fillna(p_df[features].mean())
        
        # Scale
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(p_df[features])
        
        # K-Means K=4
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        p_df['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        p_df['PC1'] = X_pca[:, 0]
        p_df['PC2'] = X_pca[:, 1]
        
        # Calculate explained variance percentages
        dim1_pct = pca.explained_variance_ratio_[0] * 100
        dim2_pct = pca.explained_variance_ratio_[1] * 100
        
        # Identify clusters based on ROA and NPL to keep coloring consistent
        centroids = p_df.groupby('Cluster')[['ROA', 'NPL', 'CASA', 'CIR']].mean()
        sorted_by_roa = centroids.sort_values(by='ROA', ascending=False).index.tolist()
        
        cluster_props = {}
        # Star (Red): top ROA
        cluster_props[sorted_by_roa[0]] = {'color': '#F8766D', 'marker': 'o', 'name': 'Cụm 1 (Ngôi sao - Star)'}
        # Stable (Olive Green): second ROA
        cluster_props[sorted_by_roa[1]] = {'color': '#7CAE00', 'marker': '^', 'name': 'Cụm 2 (Ổn định - Stable)'}
        
        # Of remaining, higher NPL is Monitor (Purple), lower is Transition (Cyan/Teal)
        rem_0, rem_1 = sorted_by_roa[2], sorted_by_roa[3]
        if centroids.loc[rem_0, 'NPL'] > centroids.loc[rem_1, 'NPL']:
            cluster_props[rem_0] = {'color': '#C77CFF', 'marker': 'd', 'name': 'Cụm 4 (Cần giám sát - Monitor)'}
            cluster_props[rem_1] = {'color': '#00BFC4', 'marker': 's', 'name': 'Cụm 3 (Chuyển đổi - Transition)'}
        else:
            cluster_props[rem_0] = {'color': '#00BFC4', 'marker': 's', 'name': 'Cụm 3 (Chuyển đổi - Transition)'}
            cluster_props[rem_1] = {'color': '#C77CFF', 'marker': 'd', 'name': 'Cụm 4 (Cần giám sát - Monitor)'}
            
        p_df['Color'] = p_df['Cluster'].map({k: v['color'] for k, v in cluster_props.items()})
        
        # Create single large plot
        fig, ax = plt.subplots(figsize=(6.5, 4.4), dpi=300)
        
        # ggplot2 background style
        ax.set_facecolor('#EBEBEB')
        ax.grid(True, color='white', linestyle='-', linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(colors='#475569', labelsize=7)
        
        ax.set_title(info['title'], fontweight='bold', fontsize=9.5, color='#1E293B', pad=10)
        ax.set_xlabel(f"Dim1 ({dim1_pct:.1f}%)", fontsize=8, color='#475569', fontweight='semibold')
        ax.set_ylabel(f"Dim2 ({dim2_pct:.1f}%)", fontsize=8, color='#475569', fontweight='semibold')
        
        # Dynamic limits based on coordinates to fit nicely
        ax.set_xlim(p_df['PC1'].min() - 0.6, p_df['PC1'].max() + 0.6)
        ax.set_ylim(p_df['PC2'].min() - 0.6, p_df['PC2'].max() + 0.6)
        
        # Plot points and draw convex hulls
        for cluster_id, props in cluster_props.items():
            c_df = p_df[p_df['Cluster'] == cluster_id]
            if len(c_df) == 0:
                continue
            
            cluster_color = props['color']
            cluster_marker = props['marker']
            points = c_df[['PC1', 'PC2']].values
            
            # Convex Hull Polygon
            if len(points) >= 3:
                try:
                    hull = ConvexHull(points)
                    hull_points = points[hull.vertices]
                    polygon = Polygon(hull_points, closed=True, facecolor=cluster_color, edgecolor=cluster_color, alpha=0.12, linewidth=1.0, zorder=1)
                    ax.add_patch(polygon)
                    
                    # Boundary line
                    ax.plot(np.append(hull_points[:, 0], hull_points[0, 0]), 
                            np.append(hull_points[:, 1], hull_points[0, 1]), 
                            color=cluster_color, linewidth=0.8, alpha=0.5, zorder=2)
                except Exception as e:
                    print(f"Hull error: {e}")
            elif len(points) == 2:
                # Draw a line between the two points
                ax.plot(points[:, 0], points[:, 1], color=cluster_color, linewidth=0.8, alpha=0.4, zorder=2)
                
            # Plot individual points
            ax.scatter(c_df['PC1'], c_df['PC2'], color=cluster_color, marker=cluster_marker, s=40, edgecolor='w', linewidths=0.5, zorder=4)
            
            # Plot Centroid
            centroid_x = points[:, 0].mean()
            centroid_y = points[:, 1].mean()
            ax.scatter(centroid_x, centroid_y, color=cluster_color, marker=cluster_marker, s=120, edgecolor='black', linewidths=0.7, alpha=0.9, zorder=5)
            
            # Annotate with just bank number (integer)
            for _, row in c_df.iterrows():
                bank_id = str(int(row['Công ty']))
                # Use a small offset so text doesn't touch the dot
                ax.text(row['PC1'], row['PC2'] + 0.05, bank_id, fontsize=6.8, fontweight='bold', color=cluster_color, ha='center', va='bottom', zorder=6)
                
        # Custom legends for clusters matching fviz_cluster style
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#F8766D', markersize=8, label='Cụm 1 (Ngôi sao - Star)'),
            Line2D([0], [0], marker='^', color='w', markerfacecolor='#7CAE00', markersize=8, label='Cụm 2 (Ổn định - Stable)'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='#00BFC4', markersize=8, label='Cụm 3 (Chuyển đổi - Transition)'),
            Line2D([0], [0], marker='d', color='w', markerfacecolor='#C77CFF', markersize=8, label='Cụm 4 (Cần giám sát - Monitor)')
        ]
        ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.18), frameon=False, fontsize=7.5, ncol=4)
        
        path = os.path.join(public_dir, info['filename'])
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        print(f"Saved {path}")

# ----------------------------------------------------
# CHART 9.2: Quadrant Scatter Plot (Equity Ratio vs LLR Coverage)
# ----------------------------------------------------
def gen_chart_9_2():
    import glob
    import pandas as pd
    
    BS_FILE   = glob.glob(r'd:\uni\gcontest\*Balance*')[0]
    NOTE_FILE = glob.glob(r'd:\uni\gcontest\*Note*')[0]
    
    bs = pd.read_csv(BS_FILE)
    note = pd.read_csv(NOTE_FILE)
    
    # Filter 2024 data
    bs_24 = bs[bs['Năm'] == 2024].copy()
    note_24 = note[note['Năm'] == 2024].copy()
    
    # Merge BS and Note
    m = bs_24.merge(note_24, on=['Công ty','Năm'])
    
    # Equity Ratio = VCSH (A64) / TTS (A1) * 100
    m['equity_ratio'] = m['A64'] / m['A1'] * 100
    
    # LLR Coverage = Dự phòng cụ thể (A14) / NPL (C35 + C36 + C37) * 100
    npl_cols = ['C35', 'C36', 'C37']
    m['npl_amt'] = m[npl_cols].sum(axis=1)
    m['llr_coverage'] = m['A14'].abs() / m['npl_amt'] * 100
    
    data = m[['Công ty', 'equity_ratio', 'llr_coverage']].dropna().reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')
    
    # Draw limits
    ax.axvline(8.0, color='#64748B', linestyle='--', linewidth=1.0, zorder=2) # 8% Capital adequacy limit
    ax.axhline(100.0, color='#64748B', linestyle='--', linewidth=1.0, zorder=2) # 100% LLR coverage limit
    
    # Plot points
    ax.scatter(data['equity_ratio'], data['llr_coverage'], color=DODGER_BLUE, alpha=0.75, s=60, edgecolor='w', zorder=3, label='Ngân hàng (n=27)')
    
    # Highlight specific banks
    # Consistent Leaders
    # Find NH 4 and NH 2
    nh4_row = data[data['Công ty'] == 4]
    nh2_row = data[data['Công ty'] == 2]
    
    if not nh4_row.empty:
        ax.scatter(nh4_row['equity_ratio'].values[0], nh4_row['llr_coverage'].values[0], color=CLUSTER_STAR, s=100, edgecolor='w', zorder=5)
        ax.text(nh4_row['equity_ratio'].values[0] + 0.15, nh4_row['llr_coverage'].values[0] + 5, 'NH 4\n(Golden Zone)', fontsize=7.5, fontweight='bold', color=CLUSTER_STAR)
        
    if not nh2_row.empty:
        ax.scatter(nh2_row['equity_ratio'].values[0], nh2_row['llr_coverage'].values[0], color=CLUSTER_STAR, s=100, edgecolor='w', zorder=5)
        ax.text(nh2_row['equity_ratio'].values[0] + 0.15, nh2_row['llr_coverage'].values[0] - 15, 'NH 2\n(Golden Zone)', fontsize=7.5, fontweight='bold', color=CLUSTER_STAR)
        
    # Bottom left: Danger Zone
    danger_zone = data[(data['equity_ratio'] < 8.0) & (data['llr_coverage'] < 100.0)]
    for _, row in danger_zone.iterrows():
        ax.scatter(row['equity_ratio'], row['llr_coverage'], color=CLUSTER_MONITOR, s=80, edgecolor='w', zorder=4)
        ax.text(row['equity_ratio'] + 0.15, row['llr_coverage'] + 3, f"NH {int(row['Công ty'])}", fontsize=6.8, color=CLUSTER_MONITOR, fontweight='bold')
        
    # Text annotations for zones
    ax.text(12.5, 230, 'VÙNG AN TOÀN VÀNG (GOLDEN ZONE)\nĐệm vốn dày & Dự phòng bao phủ >100%', color=CLUSTER_STAR, fontweight='bold', fontsize=7.5, ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="#E6F4EA", ec=CLUSTER_STAR, lw=0.5))
    ax.text(4.5, 30, 'VÙNG NGUY HIỂM\nĐệm vốn <8% & Dự phòng <100%', color=CLUSTER_MONITOR, fontweight='bold', fontsize=7.5, ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="#FCE8E6", ec=CLUSTER_MONITOR, lw=0.5))
    
    ax.set_xlabel('Tỷ lệ an toàn vốn tự có Equity Ratio (VCSH/TTS) (%)', fontweight='bold', fontsize=8.2)
    ax.set_ylabel('Tỷ lệ bao phủ nợ xấu LLR Coverage (%)', fontweight='bold', fontsize=8.2)
    ax.set_xlim(3.0, 16.0)
    ax.set_ylim(0, 260)
    ax.set_title('Bản đồ Kỷ luật Phòng vệ: Equity Ratio vs LLR Coverage (2024)', fontweight='bold', fontsize=9.5, pad=12, color='#1E293B')
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_9_2_discipline_quadrant.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# ----------------------------------------------------
# CHART 9.3: Summary Pearson Correlation Comparison
# ----------------------------------------------------
def gen_chart_9_3():
    factors = [
        'Thu ngoài lãi\n(Fee Income/TOI)',
        'Đệm vốn tự có\n(Equity/Assets)',
        'Tiền gửi rẻ\n(CASA Ratio)',
        'Tối ưu vận hành\n(-CIR)'
    ]
    correlations = [0.672, 0.456, 0.395, -0.320]
    colors = [CLUSTER_STAR, DODGER_BLUE, LIGHT_BLUE, CLUSTER_MONITOR]
    
    fig, ax = plt.subplots(figsize=(5.0, 4.2), dpi=300)
    ax.grid(True, linestyle='--', alpha=0.3, color='#94A3B8', axis='y', zorder=0)
    
    x = np.arange(len(factors))
    bars = ax.bar(x, correlations, color=colors, alpha=0.85, width=0.5, zorder=3)
    
    # Draw reference line at 0
    ax.axhline(0, color='#64748B', linewidth=1, zorder=2)
    
    # Add values labels on top/bottom of bars
    for i, bar in enumerate(bars):
        val = correlations[i]
        x_pos = bar.get_x() + bar.get_width()/2
        
        y_pos = val + 0.03 if val >= 0 else val - 0.06
        va_align = 'bottom' if val >= 0 else 'top'
        
        ax.text(x_pos, y_pos, f"r = {val:+.3f}",
                ha='center', va=va_align, fontsize=7.5, fontweight='bold', color='#1E293B')
                
    ax.set_xticks(x)
    ax.set_xticklabels(factors, fontweight='bold', fontsize=7.5)
    ax.set_ylabel('Hệ số tương quan Pearson với ROA (r)', fontweight='bold', fontsize=8.2)
    ax.set_ylim(-0.50, 0.85)
    ax.set_title('Tương quan các chỉ số đệm lực với hiệu suất sinh lời ROA (2024)', fontweight='bold', fontsize=9, pad=10, color='#1E293B')
    
    plt.tight_layout()
    path = os.path.join(public_dir, 'slide_9_3_takeaway_summary.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"Saved {path}")

# Run all
if __name__ == '__main__':
    gen_chart_9_1()
    gen_chart_9_2()
    gen_chart_9_3()
    print("All Chapter 9 premium charts generated successfully!")

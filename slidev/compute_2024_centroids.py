import sys
import glob
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
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
            
    df['ROA'] = safe_div(df['B22'], df['A1'])
    npl_sum = df[['C35','C36','C37']].sum(axis=1)
    df['NPL'] = safe_div(npl_sum, df['A13'])
    df['CASA'] = safe_div(df['C68'], df['A55'])
    df['CIR'] = safe_div(df['B15'], df['B14'])
    df['NIM'] = safe_div(df['B3'], df['A1'])
    df['LDR'] = safe_div(df['A13'], df['A55'])
    
    features = ['ROA', 'NPL', 'CASA', 'CIR', 'NIM', 'LDR']
    
    p_df = df[df['Năm'] == 2024].groupby('Công ty')[features].mean().reset_index()
    p_df[features] = p_df[features].fillna(p_df[features].mean())
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(p_df[features])
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    p_df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Identify cluster names
    centroids = p_df.groupby('Cluster')[features].mean()
    sorted_by_roa = centroids.sort_values(by='ROA', ascending=False).index.tolist()
    
    cluster_labels = {}
    cluster_labels[sorted_by_roa[0]] = 'Star'
    cluster_labels[sorted_by_roa[1]] = 'Stable'
    
    rem_0, rem_1 = sorted_by_roa[2], sorted_by_roa[3]
    if centroids.loc[rem_0, 'NPL'] > centroids.loc[rem_1, 'NPL']:
        cluster_labels[rem_0] = 'Monitor'
        cluster_labels[rem_1] = 'Transition'
    else:
        cluster_labels[rem_0] = 'Transition'
        cluster_labels[rem_1] = 'Monitor'
        
    p_df['Cluster_Name'] = p_df['Cluster'].map(cluster_labels)
    centroids = p_df.groupby('Cluster_Name')[features].mean()
    
    print("=== CENTROIDS FOR 2024 ===")
    print(centroids.to_string())
    
    print("\n=== BANK ASSIGNMENTS FOR 2024 ===")
    for label in ['Star', 'Stable', 'Transition', 'Monitor']:
        banks = p_df[p_df['Cluster_Name'] == label]['Công ty'].tolist()
        print(f"{label}: {[int(b) for b in sorted(banks)]}")

if __name__ == '__main__':
    main()

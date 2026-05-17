import pandas as pd
import numpy as np

files = [
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_GDP.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_FDI.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Monetary.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Tỷ giá.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_Tổng mức bán lẻ.csv',
    'd:/uni/gcontest/[G\'Contest 2026] Đề Vòng 2_PMI.csv'
]

out = []
for f in files:
    try:
        # First row is typically header
        df = pd.read_csv(f, encoding='utf-8', header=1)
        name = f.split('_')[-1]
        out.append(f'--- File: {name} ---')
        
        # Determine frequency based on Date
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            df_recent = df[df['Year'] >= 2020]
            
            # Simple summarization logic
            cols_to_summarize = [c for c in df.columns if c not in ['Date', 'Year'] and 'Unnamed' not in str(c) and df[c].dtype in [np.float64, np.int64]]
            if len(cols_to_summarize) > 0:
                summary = df_recent.groupby('Year')[cols_to_summarize].mean().round(2)
                out.append(summary.to_string())
            else:
                out.append('No numeric columns found for summarization.')
        else:
            out.append('No Date column')
    except Exception as e:
        out.append(f'Error reading {f.split("_")[-1]}: {e}')

with open('d:/uni/gcontest/macro_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print("Done")

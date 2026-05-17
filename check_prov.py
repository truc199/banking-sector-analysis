# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
# ]
# ///

import pandas as pd

def check_prov():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    is_file = "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv"
    df = pd.read_csv(is_file)
    cols = ['B14', 'B17', 'B15']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        
    sys = df.groupby('Năm')[['B14', 'B17', 'B15']].sum().reset_index()
    sys['System_Prov_Burden'] = sys['B17'] / sys['B14'] * 100
    sys['System_CIR'] = sys['B15'] / sys['B14'] * 100
    
    print(sys[sys['Năm'] >= 2015].to_string(index=False, float_format="%.2f"))

if __name__ == "__main__":
    check_prov()

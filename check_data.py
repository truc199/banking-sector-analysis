# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
# ]
# ///

import pandas as pd

def check_data():
    df = pd.read_csv("[G'Contest 2026] Đề Vòng 2_3. Note.csv", skiprows=1)
    print("Columns:", df.columns[:10])
    print("Number of companies:", df['Công ty'].nunique())
    print("Companies:", df['Công ty'].unique())
    print("Years:", df['Năm'].unique())
    
    # Check if C33 to C37 exist and are numeric
    cols = ['C33', 'C34', 'C35', 'C36', 'C37']
    print(df[['Công ty', 'Năm'] + cols].head())

if __name__ == "__main__":
    check_data()

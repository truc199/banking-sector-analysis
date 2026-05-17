# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "openpyxl",
# ]
# ///

import pandas as pd
import os

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    file_path = "[G'Contest 2026] Đề Vòng 2.xlsx"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Reading {file_path}...")
    try:
        # Read all sheets
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Construct output file name
            base_name = os.path.splitext(file_path)[0]
            out_file = f"{base_name}_{sheet_name}.csv"
            
            # Replace some potentially invalid characters for filenames
            out_file = out_file.replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_')
            
            df.to_csv(out_file, index=False, encoding='utf-8-sig')
            print(f"Saved: {out_file}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

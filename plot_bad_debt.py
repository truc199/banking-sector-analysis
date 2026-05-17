# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
# ]
# ///

import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    # Read data
    file_path = "[G'Contest 2026] Đề Vòng 2_3. Note.csv"
    df = pd.read_csv(file_path)
    
    # Fields for Loan quality classification
    cols = ['C33', 'C34', 'C35', 'C36', 'C37']
    labels = {
        'C33': 'Nợ đủ tiêu chuẩn',
        'C34': 'Nợ cần chú ý',
        'C35': 'Nợ dưới tiêu chuẩn',
        'C36': 'Nợ nghi ngờ',
        'C37': 'Nợ xấu có khả năng mất vốn'
    }
    
    # Clean the data and convert to numeric
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    # Calculate Total Loans for the classification
    df['Total_Loans'] = df[cols].sum(axis=1)
    
    # Calculate ratios
    for col in cols:
        # Avoid division by zero
        df[f'{col}_ratio'] = df.apply(
            lambda row: (row[col] / row['Total_Loans'] * 100) if row['Total_Loans'] > 0 else 0,
            axis=1
        )
        
    # Create directory for pictures
    os.makedirs('pictures', exist_ok=True)
    
    # Get list of banks
    banks = df['Công ty'].unique()
    
    # Plot one chart for each category
    for col in cols:
        plt.figure(figsize=(14, 8))
        
        # Plot each bank
        for bank in banks:
            bank_data = df[df['Công ty'] == bank].sort_values(by='Năm')
            # Only plot if we have data
            if not bank_data.empty:
                plt.plot(bank_data['Năm'].astype(str), bank_data[f'{col}_ratio'], marker='o', label=f'NH {bank}')
            
        plt.title(f'Tỉ lệ {labels[col]} của các ngân hàng theo thời gian', fontsize=16)
        plt.xlabel('Năm', fontsize=12)
        plt.ylabel('Tỉ lệ (%)', fontsize=12)
        
        # Format the legend to handle many banks
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=9, ncol=2)
        
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        # Save figure
        # Handle filename potential issues with spaces/unicode
        safe_name = labels[col].replace(' ', '_')
        out_file = os.path.join('pictures', f'{safe_name}.png')
        plt.savefig(out_file, dpi=150)
        plt.close()
        print(f"Saved {out_file}")

if __name__ == "__main__":
    main()

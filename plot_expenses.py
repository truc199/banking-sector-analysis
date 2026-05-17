# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "numpy",
# ]
# ///

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Ensure UTF-8 output on Windows terminal
    if sys.platform.startswith('win'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    print("=== STARTING EXPENSE ANALYSIS AND PLOTTING PIPELINE ===\n")

    # Define paths
    mapping_file = "[G'Contest 2026] Đề Vòng 2_4. Mapping.csv"
    is_file = "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv"
    note_file = "[G'Contest 2026] Đề Vòng 2_3. Note.csv"
    pictures_dir = "pictures"

    # Create pictures directory if it doesn't exist
    os.makedirs(pictures_dir, exist_ok=True)

    # 1. Parse Mapping file to get expense categories
    print("Reading mapping file...")
    df_map = pd.read_csv(mapping_file)
    
    # Clean code and description columns
    df_map['Trường dữ liệu'] = df_map['Trường dữ liệu'].astype(str).str.strip()
    df_map['Mô tả'] = df_map['Mô tả'].astype(str).str.strip()
    
    mapping_dict = dict(zip(df_map['Trường dữ liệu'], df_map['Mô tả']))

    # 2. Read datasets
    print("Reading Income Statement and Note datasets...")
    df_is = pd.read_csv(is_file)
    df_note = pd.read_csv(note_file)

    # Clean company names and years
    for df in [df_is, df_note]:
        df['Công ty'] = df['Công ty'].astype(str).str.strip()
        df['Năm'] = pd.to_numeric(df['Năm'], errors='coerce')

    # Merge the datasets to ensure consistency across years and companies
    df_merged = df_is.merge(df_note, on=['Công ty', 'Năm'], how='inner')
    print(f"Data merged successfully. Total records: {df_merged.shape[0]} across {df_merged['Công ty'].nunique()} companies.")
    print(f"Years covered: {sorted(df_merged['Năm'].dropna().unique())}\n")

    # 3. Define the groups of expenses to plot
    expense_groups = {
        "1_High_Level_IS": {
            "title": "High-Level Income Statement Expenses (B-Series)",
            "subtitle": "System-wide high-level expenses from the Income Statement (in absolute values)",
            "codes": ['B2', 'B5', 'B11', 'B15', 'B17', 'B21'],
            "is_is_statement": True, # Income statement values are negative, we will take absolute values
            "filename": "expense_high_level_is.png"
        },
        "2_Interest_Breakdown": {
            "title": "Breakdown of Interest Expenses (C87-C91)",
            "subtitle": "Detailed interest and financing costs from Notes",
            "codes": ['C88', 'C89', 'C90', 'C91'],
            "is_is_statement": False,
            "filename": "expense_interest_breakdown.png"
        },
        "3_Service_Breakdown": {
            "title": "Breakdown of Service & Fee Expenses (C100-C106)",
            "subtitle": "Detailed service/commission expenses from Notes",
            "codes": ['C100', 'C101', 'C102', 'C103', 'C104', 'C105', 'C106'],
            "is_is_statement": False,
            "filename": "expense_service_breakdown.png"
        },
        "4_Operating_Breakdown": {
            "title": "Breakdown of Operating Expenses (C140-C155)",
            "subtitle": "High-level operational cost breakdowns from Notes",
            "codes": ['C141', 'C142', 'C148', 'C151', 'C152', 'C153', 'C154', 'C155'],
            "is_is_statement": False,
            "filename": "expense_operating_breakdown.png"
        },
        "5_Staff_Breakdown": {
            "title": "Breakdown of Staff Expenses (C142-C147)",
            "subtitle": "Detailed human resources and salary costs from Notes",
            "codes": ['C143', 'C144', 'C145', 'C146', 'C147'],
            "is_is_statement": False,
            "filename": "expense_staff_breakdown.png"
        },
        "6_Asset_Breakdown": {
            "title": "Breakdown of Asset Expenses (C148-C150)",
            "subtitle": "Property, equipment, depreciation, and asset management costs from Notes",
            "codes": ['C149', 'C150'],
            "is_is_statement": False,
            "filename": "expense_asset_breakdown.png"
        },
        "7_FX_Securities_Other": {
            "title": "Breakdown of FX, Securities & Other Expenses",
            "subtitle": "Foreign exchange losses, investment costs, and other non-operating expenses",
            "codes": ['C112', 'C113', 'C114', 'C115', 'C118', 'C123', 'C124', 'C134', 'C135', 'C136', 'C137', 'C138', 'C139'],
            "is_is_statement": False,
            "filename": "expense_fx_securities_other_breakdown.png"
        }
    }

    # Clean the data by converting all codes of interest to numeric values
    all_codes = []
    for grp in expense_groups.values():
        all_codes.extend(grp["codes"])
    all_codes = list(set(all_codes))

    for code in all_codes:
        if code in df_merged.columns:
            df_merged[code] = pd.to_numeric(df_merged[code], errors='coerce').fillna(0)
        else:
            print(f"Warning: {code} not found in merged columns.")
            df_merged[code] = 0.0

    # Aggregate data by Year (sum across all banks)
    df_yearly = df_merged.groupby('Năm')[all_codes].sum().reset_index()
    df_yearly = df_yearly[df_yearly['Năm'] >= 2015].sort_values('Năm')

    # Modern Premium Plotting setup
    plt.style.use('default')
    sns.set_theme(style="whitegrid", rc={
        'axes.facecolor': '#FAFAFA',
        'grid.color': '#E5E8E8',
        'grid.linestyle': '--',
        'figure.facecolor': '#FFFFFF',
        'font.family': 'sans-serif'
    })

    # Custom premium palette
    colors_palette = ['#2C3E50', '#3498DB', '#E74C3C', '#2ECC71', '#F1C40F', '#9B59B6', '#1ABC9C', '#E67E22', '#D35400', '#7F8C8D', '#16A085', '#2980B9', '#8E44AD']

    # 4. Generate and save individual charts
    print("Generating individual category plots...")
    for grp_key, grp_info in expense_groups.items():
        plt.figure(figsize=(14, 7))
        
        # Determine labels and signs
        codes = grp_info["codes"]
        title = grp_info["title"]
        subtitle = grp_info["subtitle"]
        filename = grp_info["filename"]
        is_is = grp_info["is_is_statement"]
        
        for idx, code in enumerate(codes):
            desc = mapping_dict.get(code, f"Undocumented code {code}")
            # Clean up desc if too long or indented
            desc = desc.strip()
            
            y_values = df_yearly[code].copy()
            if is_is:
                # Convert to absolute value for cleaner visualization
                y_values = y_values.abs()
                
            color = colors_palette[idx % len(colors_palette)]
            marker = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h'][idx % 10]
            
            sns.lineplot(
                data=df_yearly, 
                x='Năm', 
                y=y_values, 
                marker=marker, 
                markersize=8, 
                linewidth=2.5, 
                color=color, 
                label=f"{code} - {desc}",
                markeredgecolor='white',
                markeredgewidth=1.5
            )
            
            # Annotate final year value to make the chart extremely premium and readable
            final_year = df_yearly['Năm'].iloc[-1]
            final_val = y_values.iloc[-1]
            plt.annotate(
                f"{final_val:,.0f}", 
                xy=(final_year, final_val),
                xytext=(5, -5 if idx % 2 == 0 else 5), 
                textcoords='offset points', 
                fontsize=9,
                fontweight='semibold',
                color=color
            )

        plt.title(title, fontsize=18, fontweight='bold', color='#1A252C', pad=15)
        plt.suptitle(subtitle, fontsize=11, style='italic', color='#5D6D7E', y=0.92)
        plt.xlabel("Year", fontsize=12, fontweight='semibold', labelpad=10)
        plt.ylabel("System-wide Sum Value (Absolute Value)", fontsize=12, fontweight='semibold', labelpad=10)
        
        # Formatting X-ticks
        plt.xticks(df_yearly['Năm'].unique(), [str(int(y)) for y in df_yearly['Năm'].unique()])
        
        # Legend formatting
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#E5E8E8', shadow=False, fontsize=10)
        
        # Tight layout & Save
        plt.tight_layout()
        save_path = os.path.join(pictures_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved: {save_path}")

    # 5. Generate Master Dashboard (Combined View)
    print("\nGenerating Executive Master Dashboard...")
    fig = plt.figure(figsize=(24, 20))
    fig.suptitle("VIETNAMESE BANKING SYSTEM - EXECUTIVE EXPENSE REPORT (2015-2024)", fontsize=28, fontweight='bold', color='#1A252C', y=0.98)
    
    # 3x2 Grid for the first 6 main groups to fit them beautifully
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.25)
    
    dashboard_groups = [
        ("1_High_Level_IS", gs[0, 0]),
        ("2_Interest_Breakdown", gs[0, 1]),
        ("3_Service_Breakdown", gs[1, 0]),
        ("4_Operating_Breakdown", gs[1, 1]),
        ("5_Staff_Breakdown", gs[2, 0]),
        ("6_Asset_Breakdown", gs[2, 1])
    ]

    for grp_key, grid_pos in dashboard_groups:
        ax = fig.add_subplot(grid_pos)
        grp_info = expense_groups[grp_key]
        codes = grp_info["codes"]
        title = grp_info["title"]
        is_is = grp_info["is_is_statement"]
        
        for idx, code in enumerate(codes):
            desc = mapping_dict.get(code, code).strip()
            # Truncate description for dashboard layout to avoid clutter
            if len(desc) > 35:
                desc = desc[:32] + "..."
                
            y_values = df_yearly[code].copy()
            if is_is:
                y_values = y_values.abs()
                
            color = colors_palette[idx % len(colors_palette)]
            marker = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h'][idx % 10]
            
            sns.lineplot(
                data=df_yearly, 
                x='Năm', 
                y=y_values, 
                marker=marker, 
                markersize=6, 
                linewidth=2.0, 
                color=color, 
                label=f"{code}: {desc}",
                markeredgecolor='white',
                markeredgewidth=1.0,
                ax=ax
            )
            
        ax.set_title(title, fontsize=14, fontweight='bold', color='#1A252C')
        ax.set_xlabel("Year", fontsize=10)
        ax.set_ylabel("Value (Absolute)", fontsize=10)
        ax.set_xticks(df_yearly['Năm'].unique())
        ax.set_xticklabels([str(int(y)) for y in df_yearly['Năm'].unique()], fontsize=9)
        ax.legend(loc='upper left', fontsize=8, frameon=True, facecolor='#FFFFFF', framealpha=0.9)
        ax.tick_params(axis='both', which='major', labelsize=9)

    # Save Dashboard
    master_dashboard_path = os.path.join(pictures_dir, "expense_master_dashboard.png")
    plt.savefig(master_dashboard_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Saved Master Dashboard: {master_dashboard_path}")

    # Create a small summary report to display
    print("\n" + "="*50)
    print("EXPENSE ANALYSIS REPORT COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"All images have been saved to directory: {pictures_dir}/")
    print(f"1. High-Level Income Statement: pictures/expense_high_level_is.png")
    print(f"2. Interest Breakdown:          pictures/expense_interest_breakdown.png")
    print(f"3. Service Breakdown:           pictures/expense_service_breakdown.png")
    print(f"4. Operating Breakdown:         pictures/expense_operating_breakdown.png")
    print(f"5. Staff Breakdown:             pictures/expense_staff_breakdown.png")
    print(f"6. Asset Breakdown:             pictures/expense_asset_breakdown.png")
    print(f"7. FX, Securities & Other:     pictures/expense_fx_securities_other_breakdown.png")
    print(f"8. Master Executive Dashboard:  pictures/expense_master_dashboard.png")
    print("="*50)

if __name__ == '__main__':
    main()

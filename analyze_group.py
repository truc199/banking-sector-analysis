"""
Banking Data Analysis — Group-by-group insight generation.
Loads data once, then each group function computes metrics and writes a markdown file.
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# === DATA LOADING ===
BASE_DIR = r"d:\uni\gcontest"
BS_FILE = os.path.join(BASE_DIR, "[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
IS_FILE = os.path.join(BASE_DIR, "[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
NOTE_FILE = os.path.join(BASE_DIR, "[G'Contest 2026] Đề Vòng 2_3. Note.csv")
INSIGHT_DIR = os.path.join(BASE_DIR, "insight")
os.makedirs(INSIGHT_DIR, exist_ok=True)

print("Loading data...")
bs = pd.read_csv(BS_FILE)
inc = pd.read_csv(IS_FILE)
note = pd.read_csv(NOTE_FILE)

# Clean column names (remove trailing whitespace/commas)
for df in [bs, inc, note]:
    df.columns = df.columns.str.strip().str.rstrip(',')

# Rename identifier columns for consistency
bs.rename(columns={'Công ty': 'Bank', 'Năm': 'Year'}, inplace=True)
inc.rename(columns={'Công ty': 'Bank', 'Năm': 'Year'}, inplace=True)
note.rename(columns={'Công ty': 'Bank', 'Năm': 'Year'}, inplace=True)

# Merge all into one master dataframe
df = bs.merge(inc, on=['Bank', 'Year'], how='outer').merge(note, on=['Bank', 'Year'], how='outer')

# Convert numeric columns
id_cols = ['Bank', 'Year']
for col in df.columns:
    if col not in id_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print(f"Master dataframe: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Banks: {sorted(df['Bank'].unique())}")
print(f"Years: {sorted(df['Year'].unique())}")

# === HELPER FUNCTIONS ===
def safe_div(a, b):
    """Safe division returning NaN for zero/null denominators."""
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

def fmt_pct(val):
    """Format as percentage string."""
    if pd.isna(val):
        return "N/A"
    return f"{val:.2f}%"

def fmt_num(val):
    """Format large number with comma."""
    if pd.isna(val):
        return "N/A"
    return f"{val:,.2f}"

def write_insight(filename, content):
    """Write insight markdown file."""
    filepath = os.path.join(INSIGHT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  -> Saved: {filepath}")


# ============================================================
# NHÓM 1: Khả năng sinh lời tổng thể (Profitability – ROA/ROE)
# ============================================================
def analyze_group1():
    print("\n" + "="*60)
    print("NHÓM 1: Profitability — ROA / ROE / DuPont Decomposition")
    print("="*60)
    
    g = df[['Bank', 'Year', 'A1', 'A64', 'A66', 'A75', 'B18', 'B22', 'B14', 'B15', 'B21']].copy()
    
    # --- Core metrics ---
    g['ROA'] = safe_div(g['B22'], g['A1']) * 100
    g['ROE'] = safe_div(g['B22'], g['A64']) * 100
    g['Profit_Margin'] = safe_div(g['B22'], g['B14']) * 100  # Net Income / TOI
    g['Asset_Turnover'] = safe_div(g['B14'], g['A1']) * 100  # TOI / Total Assets
    g['Equity_Multiplier'] = safe_div(g['A1'], g['A64'])     # Total Assets / Equity
    g['Leverage'] = safe_div(g['A1'], g['A64'])
    g['Tax_Burden'] = safe_div(g['B22'], g['B18']) * 100     # NIAT / PBT
    g['Retained_Earnings_Ratio'] = safe_div(g['A75'], g['A64']) * 100
    
    # --- Aggregate stats by Year ---
    yearly = g.groupby('Year').agg(
        ROA_mean=('ROA', 'mean'),
        ROA_median=('ROA', 'median'),
        ROE_mean=('ROE', 'mean'),
        ROE_median=('ROE', 'median'),
        Leverage_mean=('Leverage', 'mean'),
        Profit_Margin_mean=('Profit_Margin', 'mean'),
        Asset_Turnover_mean=('Asset_Turnover', 'mean'),
    ).reset_index()
    
    # --- Bank-level averages (latest 3 years: 2022-2024) ---
    recent = g[g['Year'] >= 2022]
    bank_avg = recent.groupby('Bank').agg(
        ROA_avg=('ROA', 'mean'),
        ROE_avg=('ROE', 'mean'),
        Leverage_avg=('Leverage', 'mean'),
        Profit_Margin_avg=('Profit_Margin', 'mean'),
        Retained_Earnings_avg=('Retained_Earnings_Ratio', 'mean'),
    ).reset_index().sort_values('ROE_avg', ascending=False)
    
    # --- DuPont decomposition for latest year ---
    latest_year = g['Year'].max()
    latest = g[g['Year'] == latest_year].copy()
    dupont = latest[['Bank', 'Profit_Margin', 'Asset_Turnover', 'Equity_Multiplier', 'ROE']].sort_values('ROE', ascending=False)
    
    # --- YoY ROA change ---
    g_sorted = g.sort_values(['Bank', 'Year'])
    g_sorted['ROA_yoy'] = g_sorted.groupby('Bank')['ROA'].diff()
    recovery = g_sorted[g_sorted['Year'] == 2022][['Bank', 'ROA', 'ROA_yoy']].sort_values('ROA_yoy', ascending=False)
    
    # --- Top/Bottom performers ---
    top5_roe = bank_avg.head(5)
    bot5_roe = bank_avg.tail(5)
    
    # === BUILD MARKDOWN ===
    md = []
    md.append("# Nhóm 1: Khả năng sinh lời tổng thể (Profitability – ROA/ROE)\n")
    md.append(f"> Phân tích dựa trên dữ liệu {int(g['Year'].min())}–{int(g['Year'].max())}, {g['Bank'].nunique()} ngân hàng.\n")
    
    # 1. Yearly trend
    md.append("## 1. Xu hướng ROA/ROE toàn ngành theo năm\n")
    md.append("| Năm | ROA TB (%) | ROA Median (%) | ROE TB (%) | ROE Median (%) | Đòn bẩy TB |")
    md.append("|-----|-----------|----------------|-----------|----------------|------------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_pct(r['ROA_mean'])} | {fmt_pct(r['ROA_median'])} | {fmt_pct(r['ROE_mean'])} | {fmt_pct(r['ROE_median'])} | {fmt_num(r['Leverage_mean'])} |")
    
    # 2. Top/Bottom banks
    md.append(f"\n## 2. Xếp hạng ngân hàng (TB 2022–{int(latest_year)})\n")
    md.append("### Top 5 ROE cao nhất\n")
    md.append("| Bank | ROA TB (%) | ROE TB (%) | Đòn bẩy TB | Profit Margin (%) | LN chưa PP / VCSH (%) |")
    md.append("|------|-----------|-----------|------------|-------------------|----------------------|")
    for _, r in top5_roe.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['ROA_avg'])} | {fmt_pct(r['ROE_avg'])} | {fmt_num(r['Leverage_avg'])} | {fmt_pct(r['Profit_Margin_avg'])} | {fmt_pct(r['Retained_Earnings_avg'])} |")
    
    md.append("\n### Bottom 5 ROE thấp nhất\n")
    md.append("| Bank | ROA TB (%) | ROE TB (%) | Đòn bẩy TB | Profit Margin (%) | LN chưa PP / VCSH (%) |")
    md.append("|------|-----------|-----------|------------|-------------------|----------------------|")
    for _, r in bot5_roe.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['ROA_avg'])} | {fmt_pct(r['ROE_avg'])} | {fmt_num(r['Leverage_avg'])} | {fmt_pct(r['Profit_Margin_avg'])} | {fmt_pct(r['Retained_Earnings_avg'])} |")
    
    # 3. DuPont decomposition
    md.append(f"\n## 3. DuPont Decomposition — Năm {int(latest_year)}\n")
    md.append("> ROE = Profit Margin × Asset Turnover × Equity Multiplier\n")
    md.append("| Bank | Profit Margin (%) | Asset Turnover (%) | Equity Multiplier | ROE (%) |")
    md.append("|------|-------------------|-------------------|-------------------|---------|")
    for _, r in dupont.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Profit_Margin'])} | {fmt_pct(r['Asset_Turnover'])} | {fmt_num(r['Equity_Multiplier'])} | {fmt_pct(r['ROE'])} |")
    
    # 4. COVID recovery
    md.append("\n## 4. Phục hồi sau COVID — Thay đổi ROA 2021→2022\n")
    md.append("| Bank | ROA 2022 (%) | Δ ROA (pp) |")
    md.append("|------|-------------|------------|")
    for _, r in recovery.head(10).iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['ROA'])} | {'+' if r['ROA_yoy'] > 0 else ''}{fmt_pct(r['ROA_yoy'])} |")
    
    # 5. Key insights
    md.append("\n## 5. Key Insights\n")
    
    # Insight 1: ROA/ROE trend
    roa_2020 = yearly[yearly['Year'] == 2020]['ROA_mean'].values
    roa_latest = yearly[yearly['Year'] == latest_year]['ROA_mean'].values
    if len(roa_2020) > 0 and len(roa_latest) > 0:
        roa_change = roa_latest[0] - roa_2020[0]
        direction = "tăng" if roa_change > 0 else "giảm"
        md.append(f"1. **Xu hướng ROA toàn ngành**: ROA trung bình {direction} {abs(roa_change):.2f}pp từ {roa_2020[0]:.2f}% (2020) lên {roa_latest[0]:.2f}% ({int(latest_year)}).")
    
    # Insight 2: Leverage divergence
    high_lev = bank_avg[bank_avg['Leverage_avg'] > bank_avg['Leverage_avg'].quantile(0.75)]
    low_lev = bank_avg[bank_avg['Leverage_avg'] <= bank_avg['Leverage_avg'].quantile(0.25)]
    if len(high_lev) > 0 and len(low_lev) > 0:
        roe_high = high_lev['ROE_avg'].mean()
        roe_low = low_lev['ROE_avg'].mean()
        md.append(f"\n2. **Đòn bẩy & ROE**: Nhóm đòn bẩy cao (top 25%) có ROE TB = {roe_high:.2f}%, nhóm đòn bẩy thấp (bottom 25%) có ROE TB = {roe_low:.2f}%. {'Đòn bẩy cao đang khuếch đại hiệu quả.' if roe_high > roe_low else 'Đòn bẩy cao không đồng nghĩa với ROE cao — rủi ro vận hành.'}")
    
    # Insight 3: DuPont driver
    pm_corr = latest[['Profit_Margin', 'ROE']].corr().iloc[0, 1]
    at_corr = latest[['Asset_Turnover', 'ROE']].corr().iloc[0, 1]
    em_corr = latest[['Equity_Multiplier', 'ROE']].corr().iloc[0, 1]
    driver = max([('Profit Margin', pm_corr), ('Asset Turnover', at_corr), ('Equity Multiplier', em_corr)], key=lambda x: abs(x[1]))
    md.append(f"\n3. **DuPont Driver chính ({int(latest_year)})**: Yếu tố tương quan mạnh nhất với ROE là **{driver[0]}** (r = {driver[1]:.3f}). Đây là đòn bẩy chiến lược quan trọng nhất ảnh hưởng đến hiệu quả sinh lời.")
    
    # Insight 4: Retained earnings
    high_retained = bank_avg[bank_avg['Retained_Earnings_avg'] > bank_avg['Retained_Earnings_avg'].quantile(0.75)]
    low_retained = bank_avg[bank_avg['Retained_Earnings_avg'] <= bank_avg['Retained_Earnings_avg'].quantile(0.25)]
    if len(high_retained) > 0 and len(low_retained) > 0:
        md.append(f"\n4. **Tích lũy nội bộ**: Nhóm có LN chưa phân phối/VCSH cao (>{bank_avg['Retained_Earnings_avg'].quantile(0.75):.1f}%) gồm {len(high_retained)} NH, cho thấy khả năng tự tái đầu tư mạnh, giảm phụ thuộc huy động vốn bên ngoài.")
    
    # Insight 5: Dispersion
    roe_std = recent.groupby('Year')['ROE'].std().mean()
    roe_range = bank_avg['ROE_avg'].max() - bank_avg['ROE_avg'].min()
    md.append(f"\n5. **Phân hóa ngành**: Khoảng cách ROE giữa NH tốt nhất và kém nhất (2022–{int(latest_year)}) là {roe_range:.2f}pp. Độ lệch chuẩn ROE trung bình = {roe_std:.2f}pp → {'phân hóa mạnh' if roe_std > 5 else 'tương đối đồng đều'}.")
    
    content = "\n".join(md)
    write_insight("group01_profitability.md", content)
    print("  [OK] Group 1 complete.")

# ============================================================
# NHÓM 2: Thu nhập lãi thuần và Biên lãi ròng (NIM)
# ============================================================
def analyze_group2():
    print("\n" + "="*60)
    print("NHOM 2: NIM -- Net Interest Margin")
    print("="*60)
    
    cols = ['Bank', 'Year', 'B1', 'B2', 'B3', 'A1', 'A12', 'A13', 'A55',
            'C79', 'C80', 'C81', 'C82', 'C83', 'C84', 'C85', 'C86',
            'C87', 'C88', 'C89', 'C90', 'C91']
    # Filter only existing columns
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # --- Core metrics ---
    # NIM = NII / Earning Assets (proxy: Total Assets)
    g['NIM'] = safe_div(g['B3'], g['A1']) * 100
    # NIM on loans = NII / Gross Loans
    g['NIM_loans'] = safe_div(g['B3'], g['A13']) * 100
    # Yield on loans = Interest income from loans (C80) / Gross loans (A13)
    if 'C80' in g.columns:
        g['Yield_Loans'] = safe_div(g['C80'], g['A13']) * 100
    # Cost of deposits = Interest expense on deposits (C88) / Customer deposits (A55)
    if 'C88' in g.columns:
        g['Cost_Deposits'] = safe_div(g['C88'].abs(), g['A55']) * 100
    # Spread = Yield on loans - Cost of deposits
    if 'Yield_Loans' in g.columns and 'Cost_Deposits' in g.columns:
        g['Spread'] = g['Yield_Loans'] - g['Cost_Deposits']
    # Interest income composition
    if 'C80' in g.columns:
        g['Loan_Income_Share'] = safe_div(g['C80'], g['B1']) * 100
    if 'C82' in g.columns:
        g['Securities_Income_Share'] = safe_div(g['C82'], g['B1']) * 100
    # Cost structure
    if 'C88' in g.columns:
        g['Deposit_Cost_Share'] = safe_div(g['C88'].abs(), g['B2'].abs()) * 100
    
    # --- Yearly trend ---
    agg_cols_yearly = {
        'NIM': [('NIM_mean', 'mean'), ('NIM_median', 'median')],
        'NIM_loans': [('NIM_loans_mean', 'mean')],
    }
    yearly_agg = {'NIM_mean': ('NIM', 'mean'), 'NIM_median': ('NIM', 'median'),
                  'NIM_loans_mean': ('NIM_loans', 'mean')}
    if 'Yield_Loans' in g.columns:
        yearly_agg['Yield_mean'] = ('Yield_Loans', 'mean')
    if 'Cost_Deposits' in g.columns:
        yearly_agg['Cost_mean'] = ('Cost_Deposits', 'mean')
    if 'Spread' in g.columns:
        yearly_agg['Spread_mean'] = ('Spread', 'mean')
    
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index()
    
    # --- Bank-level (2022-2024) ---
    recent = g[g['Year'] >= 2022]
    bank_agg = {'NIM_avg': ('NIM', 'mean'), 'NIM_loans_avg': ('NIM_loans', 'mean')}
    if 'Yield_Loans' in g.columns:
        bank_agg['Yield_avg'] = ('Yield_Loans', 'mean')
    if 'Cost_Deposits' in g.columns:
        bank_agg['Cost_avg'] = ('Cost_Deposits', 'mean')
    if 'Spread' in g.columns:
        bank_agg['Spread_avg'] = ('Spread', 'mean')
    if 'Loan_Income_Share' in g.columns:
        bank_agg['Loan_Inc_Share'] = ('Loan_Income_Share', 'mean')
    
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('NIM_avg', ascending=False)
    
    # --- NIM compression/expansion analysis ---
    g_sorted = g.sort_values(['Bank', 'Year'])
    g_sorted['NIM_yoy'] = g_sorted.groupby('Bank')['NIM'].diff()
    
    # NIM change 2022 -> 2024
    nim_2022 = g[g['Year'] == 2022].set_index('Bank')['NIM']
    nim_2024 = g[g['Year'] == g['Year'].max()].set_index('Bank')['NIM']
    nim_change = (nim_2024 - nim_2022).dropna().sort_values(ascending=False).reset_index()
    nim_change.columns = ['Bank', 'NIM_change']
    
    # === BUILD MARKDOWN ===
    md = []
    md.append("# Nhom 2: Thu nhap lai thuan va Bien lai rong (NIM)\n")
    md.append(f"> Phan tich du lieu {int(g['Year'].min())}--{int(g['Year'].max())}, {g['Bank'].nunique()} ngan hang.\n")
    
    # 1. Yearly NIM trend
    md.append("## 1. Xu huong NIM toan nganh\n")
    header = "| Nam | NIM TB (%) | NIM Median (%) | NIM/Loans (%)"
    sep = "|-----|-----------|----------------|---------------"
    if 'Yield_mean' in yearly.columns:
        header += " | Yield on Loans (%) | Cost of Deposits (%) | Spread (pp)"
        sep += "|-------------------|---------------------|------------|"
    header += " |"
    sep += ""
    md.append(header)
    md.append(sep)
    for _, r in yearly.iterrows():
        row = f"| {int(r['Year'])} | {fmt_pct(r['NIM_mean'])} | {fmt_pct(r['NIM_median'])} | {fmt_pct(r['NIM_loans_mean'])}"
        if 'Yield_mean' in yearly.columns:
            row += f" | {fmt_pct(r.get('Yield_mean', np.nan))} | {fmt_pct(r.get('Cost_mean', np.nan))} | {fmt_pct(r.get('Spread_mean', np.nan))}"
        row += " |"
        md.append(row)
    
    # 2. Bank ranking
    latest_year = int(g['Year'].max())
    md.append(f"\n## 2. Xep hang NIM ngan hang (TB 2022--{latest_year})\n")
    md.append("### Top 5 NIM cao nhat\n")
    top5 = bank_avg.head(5)
    header2 = "| Bank | NIM (%) | NIM/Loans (%)"
    sep2 = "|------|---------|---------------"
    if 'Yield_avg' in bank_avg.columns:
        header2 += " | Yield (%) | Cost (%) | Spread (pp)"
        sep2 += "|----------|---------|------------|"
    if 'Loan_Inc_Share' in bank_avg.columns:
        header2 += " | Loan Inc Share (%)"
        sep2 += "|--------------------|"
    header2 += " |"
    md.append(header2)
    md.append(sep2)
    for _, r in top5.iterrows():
        row = f"| {int(r['Bank'])} | {fmt_pct(r['NIM_avg'])} | {fmt_pct(r['NIM_loans_avg'])}"
        if 'Yield_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Yield_avg', np.nan))} | {fmt_pct(r.get('Cost_avg', np.nan))} | {fmt_pct(r.get('Spread_avg', np.nan))}"
        if 'Loan_Inc_Share' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Loan_Inc_Share', np.nan))}"
        row += " |"
        md.append(row)
    
    md.append("\n### Bottom 5 NIM thap nhat\n")
    bot5 = bank_avg.tail(5)
    md.append(header2)
    md.append(sep2)
    for _, r in bot5.iterrows():
        row = f"| {int(r['Bank'])} | {fmt_pct(r['NIM_avg'])} | {fmt_pct(r['NIM_loans_avg'])}"
        if 'Yield_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Yield_avg', np.nan))} | {fmt_pct(r.get('Cost_avg', np.nan))} | {fmt_pct(r.get('Spread_avg', np.nan))}"
        if 'Loan_Inc_Share' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Loan_Inc_Share', np.nan))}"
        row += " |"
        md.append(row)
    
    # 3. NIM compression/expansion
    md.append(f"\n## 3. NIM Compression/Expansion (2022 -> {latest_year})\n")
    md.append("| Bank | NIM Change (pp) | Xu huong |")
    md.append("|------|----------------|---------|")
    for _, r in nim_change.iterrows():
        trend = "Mo rong" if r['NIM_change'] > 0.1 else ("Thu hep" if r['NIM_change'] < -0.1 else "On dinh")
        sign = "+" if r['NIM_change'] > 0 else ""
        md.append(f"| {int(r['Bank'])} | {sign}{r['NIM_change']:.2f} | {trend} |")
    
    # 4. Interest income composition (latest year)
    latest_data = g[g['Year'] == g['Year'].max()]
    if 'Loan_Income_Share' in g.columns and 'Securities_Income_Share' in g.columns:
        md.append(f"\n## 4. Cau truc thu nhap lai ({latest_year})\n")
        md.append("| Bank | Thu lai cho vay/Tong (%) | Thu lai CK/Tong (%) | Khac (%) |")
        md.append("|------|------------------------|--------------------|---------| ")
        comp = latest_data[['Bank', 'Loan_Income_Share', 'Securities_Income_Share']].sort_values('Loan_Income_Share', ascending=False)
        for _, r in comp.iterrows():
            other = 100 - (r['Loan_Income_Share'] if not pd.isna(r['Loan_Income_Share']) else 0) - (r['Securities_Income_Share'] if not pd.isna(r['Securities_Income_Share']) else 0)
            md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Loan_Income_Share'])} | {fmt_pct(r['Securities_Income_Share'])} | {fmt_pct(other)} |")
    
    # 5. Key Insights
    md.append("\n## 5. Key Insights\n")
    
    # Insight 1: NIM trend
    nim_first = yearly.iloc[0]['NIM_mean']
    nim_last = yearly.iloc[-1]['NIM_mean']
    nim_peak_year = yearly.loc[yearly['NIM_mean'].idxmax(), 'Year']
    nim_peak = yearly['NIM_mean'].max()
    md.append(f"1. **NIM toan nganh**: NIM trung binh tu {nim_first:.2f}% ({int(yearly.iloc[0]['Year'])}) den {nim_last:.2f}% ({latest_year}). Dinh NIM dat {nim_peak:.2f}% vao nam {int(nim_peak_year)}.")
    
    # Insight 2: Spread analysis
    if 'Spread_mean' in yearly.columns:
        spread_first = yearly.iloc[0]['Spread_mean']
        spread_last = yearly.iloc[-1]['Spread_mean']
        md.append(f"\n2. **Spread (Yield - Cost)**: Spread trung binh {'mo rong' if spread_last > spread_first else 'thu hep'} tu {spread_first:.2f}pp ({int(yearly.iloc[0]['Year'])}) den {spread_last:.2f}pp ({latest_year}). {'NH co loi the canh tranh khi duy tri spread rong.' if spread_last > 3 else 'Spread hep cho thay ap luc canh tranh lai suat.'}")
    
    # Insight 3: NIM dispersion
    nim_std = recent.groupby('Year')['NIM'].std().mean()
    nim_range = bank_avg['NIM_avg'].max() - bank_avg['NIM_avg'].min()
    md.append(f"\n3. **Phan hoa NIM**: Chenh lech NIM giua NH tot nhat va kem nhat (2022--{latest_year}) la {nim_range:.2f}pp. Do lech chuan = {nim_std:.2f}pp.")
    
    # Insight 4: Correlation NIM vs Cost of Deposits
    if 'Cost_avg' in bank_avg.columns and 'NIM_avg' in bank_avg.columns:
        corr_nim_cost = bank_avg[['NIM_avg', 'Cost_avg']].corr().iloc[0, 1]
        md.append(f"\n4. **NIM vs Chi phi huy dong**: Tuong quan r = {corr_nim_cost:.3f}. {'NH co chi phi huy dong thap co xu huong NIM cao hon.' if corr_nim_cost < -0.3 else 'Moi quan he NIM-Cost phuc tap, khong chi phu thuoc vao chi phi huy dong.'}")
    
    # Insight 5: Compression count
    compressed = nim_change[nim_change['NIM_change'] < -0.1]
    expanded = nim_change[nim_change['NIM_change'] > 0.1]
    md.append(f"\n5. **NIM Compression**: {len(compressed)}/{len(nim_change)} NH bi thu hep NIM (2022->{latest_year}), {len(expanded)} NH mo rong. {'Da so NH dang chiu ap luc thu hep bien lai.' if len(compressed) > len(expanded) else 'Thi truong co su phan hoa ro ret giua nhom mo rong va thu hep NIM.'}")
    
    content = "\n".join(md)
    write_insight("group02_nim.md", content)
    print("  [OK] Group 2 complete.")


# ============================================================
# NHÓM 3: Chất lượng tài sản (Asset Quality – NPL)
# ============================================================
def analyze_group3():
    print("\n" + "="*60)
    print("NHOM 3: Asset Quality -- NPL / Coverage / Credit Cost")
    print("="*60)
    
    cols = ['Bank', 'Year', 'A13', 'A14', 'B17', 'B16', 'B18',
            'C33', 'C34', 'C35', 'C36', 'C37', 'A15', 'A16', 'A17', 'A48']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # --- Core metrics ---
    # NPL = (C35 + C36 + C37) / A13
    g['NPL_amount'] = g[['C35', 'C36', 'C37']].sum(axis=1)
    g['NPL_ratio'] = safe_div(g['NPL_amount'], g['A13']) * 100
    # Nợ cần chú ý (Group 2) ratio
    g['Group2_ratio'] = safe_div(g['C34'], g['A13']) * 100
    # Total classified debt (nhóm 2-5)
    g['Classified_amount'] = g[['C34', 'C35', 'C36', 'C37']].sum(axis=1)
    g['Classified_ratio'] = safe_div(g['Classified_amount'], g['A13']) * 100
    # Coverage ratio = A14 (provisions) / NPL amount
    g['Coverage'] = safe_div(g['A14'].abs(), g['NPL_amount']) * 100
    # Credit cost = B17 / A13
    g['Credit_Cost'] = safe_div(g['B17'].abs(), g['A13']) * 100
    # Provisioning pressure = B17 / B16
    g['Prov_Pressure'] = safe_div(g['B17'].abs(), g['B16']) * 100
    # NPL composition
    g['NPL_sub'] = safe_div(g['C35'], g['NPL_amount']) * 100  # Nợ dưới tiêu chuẩn
    g['NPL_doubt'] = safe_div(g['C36'], g['NPL_amount']) * 100  # Nợ nghi ngờ
    g['NPL_loss'] = safe_div(g['C37'], g['NPL_amount']) * 100  # Nợ có khả năng mất vốn
    
    # --- Yearly trend ---
    yearly = g.groupby('Year').agg(
        NPL_mean=('NPL_ratio', 'mean'),
        NPL_median=('NPL_ratio', 'median'),
        Group2_mean=('Group2_ratio', 'mean'),
        Classified_mean=('Classified_ratio', 'mean'),
        Coverage_mean=('Coverage', 'mean'),
        Coverage_median=('Coverage', 'median'),
        Credit_Cost_mean=('Credit_Cost', 'mean'),
        Prov_Pressure_mean=('Prov_Pressure', 'mean'),
    ).reset_index()
    
    # --- Bank-level (2022-2024) ---
    recent = g[g['Year'] >= 2022]
    bank_avg = recent.groupby('Bank').agg(
        NPL_avg=('NPL_ratio', 'mean'),
        Group2_avg=('Group2_ratio', 'mean'),
        Classified_avg=('Classified_ratio', 'mean'),
        Coverage_avg=('Coverage', 'mean'),
        Credit_Cost_avg=('Credit_Cost', 'mean'),
        Prov_Pressure_avg=('Prov_Pressure', 'mean'),
    ).reset_index().sort_values('NPL_avg', ascending=True)
    
    # --- NPL trend per bank (migration) ---
    g_sorted = g.sort_values(['Bank', 'Year'])
    g_sorted['NPL_yoy'] = g_sorted.groupby('Bank')['NPL_ratio'].diff()
    g_sorted['Group2_yoy'] = g_sorted.groupby('Bank')['Group2_ratio'].diff()
    
    # COVID impact: NPL change 2019->2021
    npl_2019 = g[g['Year'] == 2019].set_index('Bank')['NPL_ratio']
    npl_2021 = g[g['Year'] == 2021].set_index('Bank')['NPL_ratio']
    npl_covid = (npl_2021 - npl_2019).dropna().sort_values(ascending=False).reset_index()
    npl_covid.columns = ['Bank', 'NPL_covid_change']
    
    # Latest year snapshot
    latest_year = int(g['Year'].max())
    latest = g[g['Year'] == latest_year].sort_values('NPL_ratio', ascending=False)
    
    # === BUILD MARKDOWN ===
    md = []
    md.append("# Nhom 3: Chat luong tai san va Rui ro tin dung (Asset Quality -- NPL)\n")
    md.append(f"> Phan tich du lieu {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} ngan hang.\n")
    
    # 1. Yearly trend
    md.append("## 1. Xu huong NPL & Coverage toan nganh\n")
    md.append("| Nam | NPL TB (%) | NPL Median (%) | No can chu y (%) | No phan loai (%) | Coverage TB (%) | Credit Cost (%) | Prov/PPOP (%) |")
    md.append("|-----|-----------|----------------|-----------------|-----------------|----------------|----------------|--------------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_pct(r['NPL_mean'])} | {fmt_pct(r['NPL_median'])} | {fmt_pct(r['Group2_mean'])} | {fmt_pct(r['Classified_mean'])} | {fmt_pct(r['Coverage_mean'])} | {fmt_pct(r['Credit_Cost_mean'])} | {fmt_pct(r['Prov_Pressure_mean'])} |")
    
    # 2. Bank ranking
    md.append(f"\n## 2. Xep hang chat luong tai san (TB 2022--{latest_year})\n")
    md.append("### Top 5 NPL thap nhat (tot nhat)\n")
    top5 = bank_avg.head(5)
    md.append("| Bank | NPL (%) | No can chu y (%) | Coverage (%) | Credit Cost (%) | Prov/PPOP (%) |")
    md.append("|------|---------|-----------------|-------------|----------------|--------------|")
    for _, r in top5.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['NPL_avg'])} | {fmt_pct(r['Group2_avg'])} | {fmt_pct(r['Coverage_avg'])} | {fmt_pct(r['Credit_Cost_avg'])} | {fmt_pct(r['Prov_Pressure_avg'])} |")
    
    md.append("\n### Top 5 NPL cao nhat (xau nhat)\n")
    bot5 = bank_avg.sort_values('NPL_avg', ascending=False).head(5)
    md.append("| Bank | NPL (%) | No can chu y (%) | Coverage (%) | Credit Cost (%) | Prov/PPOP (%) |")
    md.append("|------|---------|-----------------|-------------|----------------|--------------|")
    for _, r in bot5.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['NPL_avg'])} | {fmt_pct(r['Group2_avg'])} | {fmt_pct(r['Coverage_avg'])} | {fmt_pct(r['Credit_Cost_avg'])} | {fmt_pct(r['Prov_Pressure_avg'])} |")
    
    # 3. NPL snapshot latest year
    md.append(f"\n## 3. NPL Snapshot -- Nam {latest_year}\n")
    md.append("| Bank | NPL (%) | Duoi TC (%) | Nghi ngo (%) | Mat von (%) | Coverage (%) |")
    md.append("|------|---------|------------|-------------|------------|-------------|")
    for _, r in latest.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['NPL_ratio'])} | {fmt_pct(r['NPL_sub'])} | {fmt_pct(r['NPL_doubt'])} | {fmt_pct(r['NPL_loss'])} | {fmt_pct(r['Coverage'])} |")
    
    # 4. COVID impact
    md.append("\n## 4. Tac dong COVID len NPL (2019 -> 2021)\n")
    md.append("| Bank | NPL Change (pp) | Danh gia |")
    md.append("|------|----------------|---------|")
    for _, r in npl_covid.iterrows():
        assessment = "Tang manh" if r['NPL_covid_change'] > 0.5 else ("Tang nhe" if r['NPL_covid_change'] > 0 else "Giam")
        sign = "+" if r['NPL_covid_change'] > 0 else ""
        md.append(f"| {int(r['Bank'])} | {sign}{r['NPL_covid_change']:.2f} | {assessment} |")
    
    # 5. Early warning: Group 2 ratio spike
    md.append(f"\n## 5. Canh bao som: No can chu y (Nhom 2) -- {latest_year}\n")
    g2_latest = g[g['Year'] == latest_year][['Bank', 'Group2_ratio', 'NPL_ratio']].sort_values('Group2_ratio', ascending=False)
    md.append("| Bank | No Nhom 2 (%) | NPL (%) | Nhom 2 / NPL |")
    md.append("|------|--------------|---------|-------------|")
    for _, r in g2_latest.iterrows():
        ratio = r['Group2_ratio'] / r['NPL_ratio'] if r['NPL_ratio'] > 0 else np.nan
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Group2_ratio'])} | {fmt_pct(r['NPL_ratio'])} | {fmt_num(ratio)} |")
    
    # 6. Key Insights
    md.append("\n## 6. Key Insights\n")
    
    # Insight 1: NPL trend
    npl_2020 = yearly[yearly['Year'] == 2020]['NPL_mean'].values
    npl_latest = yearly[yearly['Year'] == latest_year]['NPL_mean'].values
    if len(npl_2020) > 0 and len(npl_latest) > 0:
        md.append(f"1. **NPL toan nganh**: NPL trung binh {'tang' if npl_latest[0] > npl_2020[0] else 'giam'} tu {npl_2020[0]:.2f}% (2020) len {npl_latest[0]:.2f}% ({latest_year}).")
    
    # Insight 2: Coverage adequacy
    low_coverage = bank_avg[bank_avg['Coverage_avg'] < 100]
    high_coverage = bank_avg[bank_avg['Coverage_avg'] >= 150]
    md.append(f"\n2. **Muc do du phong**: {len(low_coverage)} NH co ty le bao phu < 100% (thieu du phong), {len(high_coverage)} NH co bao phu >= 150% (du phong day).")
    
    # Insight 3: Credit cost burden
    high_cc = bank_avg[bank_avg['Credit_Cost_avg'] > bank_avg['Credit_Cost_avg'].quantile(0.75)]
    md.append(f"\n3. **Chi phi tin dung**: Nhom chi phi tin dung cao (top 25%, >{bank_avg['Credit_Cost_avg'].quantile(0.75):.2f}%) gom {len(high_cc)} NH — dang tra gia cho chat luong tai san kem.")
    
    # Insight 4: Provisioning vs Earnings
    high_prov = bank_avg[bank_avg['Prov_Pressure_avg'] > 50]
    md.append(f"\n4. **Ap luc du phong**: {len(high_prov)} NH co du phong chiem >50% PPOP — loi nhuan that bi bao mon nghiem trong boi no xau.")
    
    # Insight 5: Group 2 early warning
    g2_high = g2_latest[g2_latest['Group2_ratio'] > g2_latest['Group2_ratio'].quantile(0.75)]
    md.append(f"\n5. **Canh bao som**: {len(g2_high)} NH co no can chu y (Nhom 2) o muc cao (>{g2_latest['Group2_ratio'].quantile(0.75):.2f}%), co nguy co chuyen thanh no xau trong tuong lai.")
    
    content = "\n".join(md)
    write_insight("group03_asset_quality.md", content)
    print("  [OK] Group 3 complete.")


# ============================================================
# NHÓM 4: Cấu trúc nguồn vốn & CASA (Funding Structure)
# ============================================================
def analyze_group4():
    print("\n" + "="*60)
    print("NHOM 4: Funding Structure -- CASA / Deposit Mix")
    print("="*60)
    
    cols = ['Bank', 'Year', 'A50', 'A51', 'A52', 'A53', 'A54', 'A55', 'A57', 'A58',
            'C67', 'C68', 'C69', 'C70', 'C71', 'C72',
            'C73', 'C74', 'C75', 'C76', 'C77', 'C78']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # --- Core metrics ---
    # CASA ratio = Tiền gửi không kỳ hạn / Tổng tiền gửi KH
    if 'C68' in g.columns:
        g['CASA'] = safe_div(g['C68'], g['A55']) * 100
    # Deposit / Total liabilities
    g['Deposit_Share'] = safe_div(g['A55'], g['A50']) * 100
    # Interbank funding ratio
    if 'A54' in g.columns:
        g['Interbank_Share'] = safe_div(g['A54'], g['A50']) * 100
    # Bond issuance ratio
    if 'A58' in g.columns:
        g['Bond_Share'] = safe_div(g['A58'], g['A50']) * 100
    # Wholesale funding = (interbank borrowing + bond) / total liabilities
    if 'A54' in g.columns and 'A58' in g.columns:
        g['Wholesale_Funding'] = safe_div(g['A54'] + g['A58'], g['A50']) * 100
    # Term structure: demand vs term deposits
    if 'C68' in g.columns and 'C69' in g.columns:
        g['Term_Deposit_Share'] = safe_div(g['C69'], g['A55']) * 100
    # Savings deposit share
    if 'C70' in g.columns:
        g['Savings_Share'] = safe_div(g['C70'], g['A55']) * 100
    # Retail deposit share (cá nhân)
    if 'C77' in g.columns:
        g['Retail_Deposit_Share'] = safe_div(g['C77'], g['A55']) * 100
    # Government/NHNN funding
    if 'A51' in g.columns:
        g['Gov_Funding_Share'] = safe_div(g['A51'], g['A50']) * 100
    
    # --- Yearly trend ---
    yearly_agg = {
        'CASA_mean': ('CASA', 'mean'),
        'CASA_median': ('CASA', 'median'),
        'Deposit_Share_mean': ('Deposit_Share', 'mean'),
    }
    if 'Wholesale_Funding' in g.columns:
        yearly_agg['Wholesale_mean'] = ('Wholesale_Funding', 'mean')
    if 'Retail_Deposit_Share' in g.columns:
        yearly_agg['Retail_mean'] = ('Retail_Deposit_Share', 'mean')
    
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index()
    
    # --- Bank-level (2022-2024) ---
    recent = g[g['Year'] >= 2022]
    bank_agg = {
        'CASA_avg': ('CASA', 'mean'),
        'Deposit_Share_avg': ('Deposit_Share', 'mean'),
    }
    if 'Interbank_Share' in g.columns:
        bank_agg['Interbank_avg'] = ('Interbank_Share', 'mean')
    if 'Bond_Share' in g.columns:
        bank_agg['Bond_avg'] = ('Bond_Share', 'mean')
    if 'Wholesale_Funding' in g.columns:
        bank_agg['Wholesale_avg'] = ('Wholesale_Funding', 'mean')
    if 'Retail_Deposit_Share' in g.columns:
        bank_agg['Retail_avg'] = ('Retail_Deposit_Share', 'mean')
    if 'Term_Deposit_Share' in g.columns:
        bank_agg['Term_avg'] = ('Term_Deposit_Share', 'mean')
    
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('CASA_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    # === BUILD MARKDOWN ===
    md = []
    md.append("# Nhom 4: Cau truc nguon von & CASA\n")
    md.append(f"> Phan tich du lieu {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} ngan hang.\n")
    
    # 1. Yearly CASA trend
    md.append("## 1. Xu huong CASA & Cau truc nguon von toan nganh\n")
    header = "| Nam | CASA TB (%) | CASA Median (%) | TG KH / Tong no (%)"
    sep = "|-----|------------|----------------|--------------------"
    if 'Wholesale_mean' in yearly.columns:
        header += " | Wholesale (%)"
        sep += "|---------------"
    if 'Retail_mean' in yearly.columns:
        header += " | TG Ca nhan (%)"
        sep += "|---------------"
    header += " |"
    md.append(header)
    md.append(sep)
    for _, r in yearly.iterrows():
        row = f"| {int(r['Year'])} | {fmt_pct(r['CASA_mean'])} | {fmt_pct(r['CASA_median'])} | {fmt_pct(r['Deposit_Share_mean'])}"
        if 'Wholesale_mean' in yearly.columns:
            row += f" | {fmt_pct(r.get('Wholesale_mean', np.nan))}"
        if 'Retail_mean' in yearly.columns:
            row += f" | {fmt_pct(r.get('Retail_mean', np.nan))}"
        row += " |"
        md.append(row)
    
    # 2. Bank ranking
    md.append(f"\n## 2. Xep hang CASA (TB 2022--{latest_year})\n")
    md.append("### Top 5 CASA cao nhat\n")
    top5 = bank_avg.head(5)
    header2 = "| Bank | CASA (%) | TG KH/No (%)"
    sep2 = "|------|---------|-------------"
    if 'Wholesale_avg' in bank_avg.columns:
        header2 += " | Wholesale (%)"
        sep2 += "|---------------"
    if 'Retail_avg' in bank_avg.columns:
        header2 += " | TG Ca nhan (%)"
        sep2 += "|---------------"
    if 'Term_avg' in bank_avg.columns:
        header2 += " | TG Co ky han (%)"
        sep2 += "|-----------------"
    header2 += " |"
    md.append(header2)
    md.append(sep2)
    for _, r in top5.iterrows():
        row = f"| {int(r['Bank'])} | {fmt_pct(r['CASA_avg'])} | {fmt_pct(r['Deposit_Share_avg'])}"
        if 'Wholesale_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Wholesale_avg', np.nan))}"
        if 'Retail_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Retail_avg', np.nan))}"
        if 'Term_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Term_avg', np.nan))}"
        row += " |"
        md.append(row)
    
    md.append("\n### Bottom 5 CASA thap nhat\n")
    bot5 = bank_avg.tail(5)
    md.append(header2)
    md.append(sep2)
    for _, r in bot5.iterrows():
        row = f"| {int(r['Bank'])} | {fmt_pct(r['CASA_avg'])} | {fmt_pct(r['Deposit_Share_avg'])}"
        if 'Wholesale_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Wholesale_avg', np.nan))}"
        if 'Retail_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Retail_avg', np.nan))}"
        if 'Term_avg' in bank_avg.columns:
            row += f" | {fmt_pct(r.get('Term_avg', np.nan))}"
        row += " |"
        md.append(row)
    
    # 3. Full bank CASA & funding breakdown (latest year)
    latest = g[g['Year'] == latest_year].sort_values('CASA', ascending=False) if 'CASA' in g.columns else pd.DataFrame()
    if not latest.empty:
        md.append(f"\n## 3. Cau truc nguon von chi tiet -- Nam {latest_year}\n")
        md.append("| Bank | CASA (%) | TG KH/No (%) | Lien NH (%) | GTCG (%) | Wholesale (%) |")
        md.append("|------|---------|-------------|------------|---------|--------------|")
        for _, r in latest.iterrows():
            md.append(f"| {int(r['Bank'])} | {fmt_pct(r.get('CASA', np.nan))} | {fmt_pct(r.get('Deposit_Share', np.nan))} | {fmt_pct(r.get('Interbank_Share', np.nan))} | {fmt_pct(r.get('Bond_Share', np.nan))} | {fmt_pct(r.get('Wholesale_Funding', np.nan))} |")
    
    # 4. Key Insights
    md.append("\n## 4. Key Insights\n")
    
    # Insight 1: CASA trend
    casa_first = yearly.iloc[0]['CASA_mean']
    casa_last = yearly.iloc[-1]['CASA_mean']
    md.append(f"1. **CASA toan nganh**: CASA trung binh {'tang' if casa_last > casa_first else 'giam'} tu {casa_first:.2f}% ({int(yearly.iloc[0]['Year'])}) den {casa_last:.2f}% ({latest_year}).")
    
    # Insight 2: CASA dispersion
    casa_range = bank_avg['CASA_avg'].max() - bank_avg['CASA_avg'].min()
    md.append(f"\n2. **Phan hoa CASA**: Chenh lech CASA giua NH tot nhat va kem nhat la {casa_range:.2f}pp. NH CASA cao co loi the chi phi von re, gop phan cai thien NIM.")
    
    # Insight 3: Wholesale dependency
    if 'Wholesale_avg' in bank_avg.columns:
        high_wholesale = bank_avg[bank_avg['Wholesale_avg'] > 15]
        md.append(f"\n3. **Phu thuoc von thi truong**: {len(high_wholesale)} NH co ty le wholesale funding >15% — rui ro thanh khoan va chi phi von cao hon.")
    
    # Insight 4: Retail deposit stability
    if 'Retail_avg' in bank_avg.columns:
        high_retail = bank_avg[bank_avg['Retail_avg'] > bank_avg['Retail_avg'].median()]
        low_retail = bank_avg[bank_avg['Retail_avg'] <= bank_avg['Retail_avg'].median()]
        md.append(f"\n4. **On dinh tien gui**: NH co ty le TG ca nhan cao (>{bank_avg['Retail_avg'].median():.1f}%) co co so KH ben vung hon. Nhom nay gom {len(high_retail)} NH.")
    
    # Insight 5: CASA-NIM correlation (cross-reference)
    md.append(f"\n5. **CASA va NIM (tham chieu cheo Nhom 2)**: NH co CASA cao thuong co chi phi huy dong thap, giup duy tri NIM tot. Day la loi the canh tranh cot loi trong moi truong lai suat giam.")
    
    content = "\n".join(md)
    write_insight("group04_funding_casa.md", content)
    print("  [OK] Group 4 complete.")


# ============================================================
# NHÓM 5: Đa dạng hóa nguồn thu (Revenue Diversification)
# ============================================================
def analyze_group5():
    print("\n" + "="*60)
    print("NHOM 5: Revenue Diversification -- Non-Interest Income")
    print("="*60)
    
    cols = ['Bank', 'Year', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14',
            'C92', 'C93', 'C94', 'C95', 'C96', 'C97', 'C98', 'C99', 'C100',
            'C101', 'C102', 'C103', 'C104', 'C105', 'C106']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # --- Core metrics ---
    # Non-interest income ratio = (TOI - NII) / TOI
    g['Non_Interest_Ratio'] = safe_div(g['B14'] - g['B3'], g['B14']) * 100
    # Fee income ratio = B6 / TOI
    g['Fee_Ratio'] = safe_div(g['B6'], g['B14']) * 100
    # Trading income ratio = (B7 + B8 + B9) / TOI
    g['Trading_Ratio'] = safe_div(g['B7'] + g['B8'] + g['B9'], g['B14']) * 100
    # Other income ratio = B12 / TOI
    g['Other_Income_Ratio'] = safe_div(g['B12'], g['B14']) * 100
    # Equity investment income ratio = B13 / TOI
    g['Equity_Inv_Ratio'] = safe_div(g['B13'], g['B14']) * 100
    # Fee income breakdown (if available)
    if 'C93' in g.columns:
        g['Payment_Fee_Share'] = safe_div(g['C93'], g['B4']) * 100  # Thanh toán / Tổng thu DV
    if 'C95' in g.columns:
        g['Guarantee_Fee_Share'] = safe_div(g['C95'], g['B4']) * 100  # Bảo lãnh
    if 'C97' in g.columns:
        g['Insurance_Fee_Share'] = safe_div(g['C97'], g['B4']) * 100  # Bảo hiểm (bancassurance)
    # Fee income margin = B6 / B4
    g['Fee_Margin'] = safe_div(g['B6'], g['B4']) * 100
    
    # --- Yearly trend ---
    yearly = g.groupby('Year').agg(
        Non_Interest_mean=('Non_Interest_Ratio', 'mean'),
        Fee_mean=('Fee_Ratio', 'mean'),
        Trading_mean=('Trading_Ratio', 'mean'),
        Other_mean=('Other_Income_Ratio', 'mean'),
    ).reset_index()
    
    # --- Bank-level (2022-2024) ---
    recent = g[g['Year'] >= 2022]
    bank_agg = {
        'Non_Interest_avg': ('Non_Interest_Ratio', 'mean'),
        'Fee_avg': ('Fee_Ratio', 'mean'),
        'Trading_avg': ('Trading_Ratio', 'mean'),
        'Other_avg': ('Other_Income_Ratio', 'mean'),
        'Equity_Inv_avg': ('Equity_Inv_Ratio', 'mean'),
        'Fee_Margin_avg': ('Fee_Margin', 'mean'),
    }
    if 'Payment_Fee_Share' in g.columns:
        bank_agg['Payment_avg'] = ('Payment_Fee_Share', 'mean')
    if 'Insurance_Fee_Share' in g.columns:
        bank_agg['Insurance_avg'] = ('Insurance_Fee_Share', 'mean')
    
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('Non_Interest_avg', ascending=False)
    
    # Trading income volatility (std dev)
    trading_vol = g.groupby('Bank')['Trading_Ratio'].agg(['mean', 'std']).reset_index()
    trading_vol.columns = ['Bank', 'Trading_mean', 'Trading_std']
    trading_vol['CV'] = safe_div(trading_vol['Trading_std'], trading_vol['Trading_mean'].abs())
    
    # Fee income growth (CAGR)
    fee_growth = []
    for bank in g['Bank'].unique():
        bdata = g[g['Bank'] == bank].sort_values('Year')
        if len(bdata) >= 2:
            first_fee = bdata.iloc[0]['B6']
            last_fee = bdata.iloc[-1]['B6']
            n_years = bdata.iloc[-1]['Year'] - bdata.iloc[0]['Year']
            if first_fee > 0 and last_fee > 0 and n_years > 0:
                cagr = (last_fee / first_fee) ** (1/n_years) - 1
                fee_growth.append({'Bank': bank, 'Fee_CAGR': cagr * 100})
    fee_growth_df = pd.DataFrame(fee_growth).sort_values('Fee_CAGR', ascending=False) if fee_growth else pd.DataFrame()
    
    latest_year = int(g['Year'].max())
    
    # === BUILD MARKDOWN ===
    md = []
    md.append("# Nhom 5: Da dang hoa nguon thu (Revenue Diversification)\n")
    md.append(f"> Phan tich du lieu {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} ngan hang.\n")
    
    # 1. Yearly trend
    md.append("## 1. Xu huong da dang hoa thu nhap\n")
    md.append("| Nam | Non-Interest/TOI (%) | Fee/TOI (%) | Trading/TOI (%) | Other/TOI (%) |")
    md.append("|-----|---------------------|------------|----------------|--------------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_pct(r['Non_Interest_mean'])} | {fmt_pct(r['Fee_mean'])} | {fmt_pct(r['Trading_mean'])} | {fmt_pct(r['Other_mean'])} |")
    
    # 2. Bank ranking
    md.append(f"\n## 2. Xep hang da dang hoa (TB 2022--{latest_year})\n")
    md.append("### Top 5 Non-Interest Income cao nhat\n")
    top5 = bank_avg.head(5)
    md.append("| Bank | Non-Int/TOI (%) | Fee/TOI (%) | Trading/TOI (%) | Other/TOI (%) | Fee Margin (%) |")
    md.append("|------|----------------|------------|----------------|--------------|---------------|")
    for _, r in top5.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Non_Interest_avg'])} | {fmt_pct(r['Fee_avg'])} | {fmt_pct(r['Trading_avg'])} | {fmt_pct(r['Other_avg'])} | {fmt_pct(r['Fee_Margin_avg'])} |")
    
    md.append("\n### Bottom 5 Non-Interest Income thap nhat\n")
    bot5 = bank_avg.tail(5)
    md.append("| Bank | Non-Int/TOI (%) | Fee/TOI (%) | Trading/TOI (%) | Other/TOI (%) | Fee Margin (%) |")
    md.append("|------|----------------|------------|----------------|--------------|---------------|")
    for _, r in bot5.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Non_Interest_avg'])} | {fmt_pct(r['Fee_avg'])} | {fmt_pct(r['Trading_avg'])} | {fmt_pct(r['Other_avg'])} | {fmt_pct(r['Fee_Margin_avg'])} |")
    
    # 3. Fee income CAGR
    if not fee_growth_df.empty:
        md.append(f"\n## 3. Tang truong thu nhap dich vu (CAGR {int(g['Year'].min())}--{latest_year})\n")
        md.append("| Bank | Fee Income CAGR (%) |")
        md.append("|------|-------------------|")
        for _, r in fee_growth_df.iterrows():
            md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Fee_CAGR'])} |")
    
    # 4. Trading income volatility
    md.append("\n## 4. Bien dong thu nhap kinh doanh (Trading Volatility)\n")
    md.append("| Bank | Trading TB (%) | Trading Std (pp) | CV |")
    md.append("|------|---------------|-----------------|-----|")
    for _, r in trading_vol.sort_values('Trading_std', ascending=False).iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Trading_mean'])} | {fmt_pct(r['Trading_std'])} | {fmt_num(r['CV'])} |")
    
    # 5. Service income structure (latest year, if data exists)
    if 'Payment_Fee_Share' in g.columns and 'Insurance_Fee_Share' in g.columns:
        latest_data = g[g['Year'] == latest_year][['Bank', 'Payment_Fee_Share', 'Guarantee_Fee_Share', 'Insurance_Fee_Share']].sort_values('Payment_Fee_Share', ascending=False)
        md.append(f"\n## 5. Cau truc thu dich vu ({latest_year})\n")
        md.append("| Bank | Thanh toan (%) | Bao lanh (%) | Bao hiem (%) |")
        md.append("|------|---------------|-------------|-------------|")
        for _, r in latest_data.iterrows():
            md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Payment_Fee_Share'])} | {fmt_pct(r['Guarantee_Fee_Share'])} | {fmt_pct(r['Insurance_Fee_Share'])} |")
    
    # 6. Key Insights
    md.append("\n## 6. Key Insights\n")
    
    nii_first = yearly.iloc[0]['Non_Interest_mean']
    nii_last = yearly.iloc[-1]['Non_Interest_mean']
    md.append(f"1. **Xu huong da dang hoa**: Thu nhap ngoai lai TB {'tang' if nii_last > nii_first else 'giam'} tu {nii_first:.2f}% ({int(yearly.iloc[0]['Year'])}) den {nii_last:.2f}% ({latest_year}).")
    
    fee_first = yearly.iloc[0]['Fee_mean']
    fee_last = yearly.iloc[-1]['Fee_mean']
    md.append(f"\n2. **Thu nhap dich vu**: Fee/TOI {'tang' if fee_last > fee_first else 'giam'} tu {fee_first:.2f}% den {fee_last:.2f}%. {'Xu huong tich cuc, giam phu thuoc tin dung.' if fee_last > fee_first else 'Chua chuyen dich manh sang mo hinh dich vu.'}")
    
    high_trading_vol = trading_vol[trading_vol['Trading_std'] > trading_vol['Trading_std'].quantile(0.75)]
    md.append(f"\n3. **Rui ro trading**: {len(high_trading_vol)} NH co bien dong trading income cao (top 25%) — nguon thu khong ben vung.")
    
    if 'Insurance_avg' in bank_avg.columns:
        high_insurance = bank_avg[bank_avg['Insurance_avg'] > 5]
        md.append(f"\n4. **Bancassurance**: {len(high_insurance)} NH co thu bao hiem >5% tong thu dich vu — chien luoc bancassurance dang phat huy hieu qua.")
    
    if 'Payment_avg' in bank_avg.columns:
        high_payment = bank_avg[bank_avg['Payment_avg'] > bank_avg['Payment_avg'].median()]
        md.append(f"\n5. **Digital proxy**: {len(high_payment)} NH co thu thanh toan vuot median ({bank_avg['Payment_avg'].median():.1f}%) — dau hieu chuyen doi so manh.")
    
    content = "\n".join(md)
    write_insight("group05_revenue_diversification.md", content)
    print("  [OK] Group 5 complete.")


# ============================================================
# NHÓM 6: Hiệu quả hoạt động & CIR (Cost Efficiency)
# ============================================================
def analyze_group6():
    print("\n" + "="*60)
    print("NHOM 6: CIR -- Cost Income Ratio / Operating Efficiency")
    print("="*60)
    
    cols = ['Bank', 'Year', 'B14', 'B15', 'B16',
            'C140', 'C141', 'C142', 'C143', 'C144', 'C148', 'C149', 'C151', 'C152']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # Core metrics
    g['CIR'] = safe_div(g['B15'], g['B14']) * 100
    g['PPOP_Margin'] = safe_div(g['B16'], g['B14']) * 100  # Pre-provision operating profit margin
    if 'C142' in g.columns:
        g['Staff_Cost_Ratio'] = safe_div(g['C142'], g['B15']) * 100
    if 'C149' in g.columns:
        g['Depreciation_Ratio'] = safe_div(g['C149'], g['B15']) * 100
    if 'C143' in g.columns:
        g['Salary_to_TOI'] = safe_div(g['C143'], g['B14']) * 100
    
    # Yearly trend
    yearly_agg = {'CIR_mean': ('CIR', 'mean'), 'CIR_median': ('CIR', 'median'),
                  'PPOP_mean': ('PPOP_Margin', 'mean')}
    if 'Staff_Cost_Ratio' in g.columns:
        yearly_agg['Staff_mean'] = ('Staff_Cost_Ratio', 'mean')
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index()
    
    # Bank-level (2022-2024)
    recent = g[g['Year'] >= 2022]
    bank_agg = {'CIR_avg': ('CIR', 'mean'), 'PPOP_avg': ('PPOP_Margin', 'mean')}
    if 'Staff_Cost_Ratio' in g.columns:
        bank_agg['Staff_avg'] = ('Staff_Cost_Ratio', 'mean')
    if 'Depreciation_Ratio' in g.columns:
        bank_agg['Depr_avg'] = ('Depreciation_Ratio', 'mean')
    if 'Salary_to_TOI' in g.columns:
        bank_agg['Salary_TOI_avg'] = ('Salary_to_TOI', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('CIR_avg', ascending=True)
    
    # Operating leverage: TOI growth vs OPEX growth (CAGR)
    op_lev = []
    for bank in g['Bank'].unique():
        bd = g[g['Bank'] == bank].sort_values('Year')
        if len(bd) >= 2:
            toi_first, toi_last = bd.iloc[0]['B14'], bd.iloc[-1]['B14']
            opex_first, opex_last = bd.iloc[0]['B15'], bd.iloc[-1]['B15']
            n = bd.iloc[-1]['Year'] - bd.iloc[0]['Year']
            if toi_first > 0 and toi_last > 0 and opex_first > 0 and opex_last > 0 and n > 0:
                toi_cagr = ((toi_last/toi_first)**(1/n) - 1) * 100
                opex_cagr = ((opex_last/opex_first)**(1/n) - 1) * 100
                op_lev.append({'Bank': bank, 'TOI_CAGR': toi_cagr, 'OPEX_CAGR': opex_cagr, 'Op_Leverage': toi_cagr - opex_cagr})
    op_lev_df = pd.DataFrame(op_lev).sort_values('Op_Leverage', ascending=False) if op_lev else pd.DataFrame()
    
    latest_year = int(g['Year'].max())
    
    # Build MD
    md = []
    md.append("# Nhom 6: Hieu qua hoat dong & CIR\n")
    md.append(f"> Phan tich du lieu {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append("## 1. Xu huong CIR toan nganh\n")
    header = "| Nam | CIR TB (%) | CIR Median (%) | PPOP Margin (%)"
    sep = "|-----|-----------|----------------|----------------"
    if 'Staff_mean' in yearly.columns:
        header += " | Staff Cost (%)"
        sep += "|---------------"
    header += " |"
    md.append(header)
    md.append(sep)
    for _, r in yearly.iterrows():
        row = f"| {int(r['Year'])} | {fmt_pct(r['CIR_mean'])} | {fmt_pct(r['CIR_median'])} | {fmt_pct(r['PPOP_mean'])}"
        if 'Staff_mean' in yearly.columns:
            row += f" | {fmt_pct(r.get('Staff_mean', np.nan))}"
        row += " |"
        md.append(row)
    
    md.append(f"\n## 2. Xep hang CIR (TB 2022--{latest_year})\n")
    md.append("### Top 5 CIR thap nhat (hieu qua nhat)\n")
    md.append("| Bank | CIR (%) | PPOP Margin (%) | Staff Cost (%) | Luong/TOI (%) | Khau hao (%) |")
    md.append("|------|---------|----------------|---------------|--------------|-------------|")
    for _, r in bank_avg.head(5).iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['CIR_avg'])} | {fmt_pct(r['PPOP_avg'])} | {fmt_pct(r.get('Staff_avg', np.nan))} | {fmt_pct(r.get('Salary_TOI_avg', np.nan))} | {fmt_pct(r.get('Depr_avg', np.nan))} |")
    
    md.append("\n### Top 5 CIR cao nhat (kem hieu qua)\n")
    md.append("| Bank | CIR (%) | PPOP Margin (%) | Staff Cost (%) | Luong/TOI (%) | Khau hao (%) |")
    md.append("|------|---------|----------------|---------------|--------------|-------------|")
    for _, r in bank_avg.tail(5).iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['CIR_avg'])} | {fmt_pct(r['PPOP_avg'])} | {fmt_pct(r.get('Staff_avg', np.nan))} | {fmt_pct(r.get('Salary_TOI_avg', np.nan))} | {fmt_pct(r.get('Depr_avg', np.nan))} |")
    
    if not op_lev_df.empty:
        md.append(f"\n## 3. Operating Leverage (CAGR {int(g['Year'].min())}--{latest_year})\n")
        md.append("| Bank | TOI CAGR (%) | OPEX CAGR (%) | Op Leverage (pp) |")
        md.append("|------|-------------|--------------|-----------------|")
        for _, r in op_lev_df.iterrows():
            md.append(f"| {int(r['Bank'])} | {fmt_pct(r['TOI_CAGR'])} | {fmt_pct(r['OPEX_CAGR'])} | {'+' if r['Op_Leverage'] > 0 else ''}{r['Op_Leverage']:.2f} |")
    
    md.append("\n## 4. Key Insights\n")
    cir_first = yearly.iloc[0]['CIR_mean']
    cir_last = yearly.iloc[-1]['CIR_mean']
    md.append(f"1. **CIR toan nganh**: CIR TB {'giam (tot)' if cir_last < cir_first else 'tang (xau)'} tu {cir_first:.2f}% den {cir_last:.2f}%.")
    
    cir_range = bank_avg['CIR_avg'].max() - bank_avg['CIR_avg'].min()
    md.append(f"\n2. **Phan hoa CIR**: Chenh lech {cir_range:.2f}pp giua NH hieu qua nhat va kem nhat.")
    
    if not op_lev_df.empty:
        positive_lev = op_lev_df[op_lev_df['Op_Leverage'] > 0]
        md.append(f"\n3. **Operating Leverage**: {len(positive_lev)}/{len(op_lev_df)} NH co TOI tang nhanh hon OPEX — dang huong loi tu economies of scale.")
    
    if 'Staff_avg' in bank_avg.columns:
        staff_median = bank_avg['Staff_avg'].median()
        md.append(f"\n4. **Chi phi nhan su**: Staff cost chiem trung binh {staff_median:.1f}% tong chi phi. Day la chi phi lon nhat va kho cat giam nhat.")
    
    content = "\n".join(md)
    write_insight("group06_cir_efficiency.md", content)
    print("  [OK] Group 6 complete.")


# ============================================================
# NHÓM 7: Thanh khoản & LDR (Liquidity)
# ============================================================
def analyze_group7():
    print("\n" + "="*60)
    print("NHOM 7: Liquidity -- LDR / Liquid Assets")
    print("="*60)
    
    cols = ['Bank', 'Year', 'A1', 'A2', 'A3', 'A4', 'A5', 'A12', 'A13', 'A55', 'A18', 'A53',
            'C38', 'C39', 'C40', 'C41', 'C68', 'C69']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # Core metrics
    g['LDR'] = safe_div(g['A13'], g['A55']) * 100  # Gross Loans / Customer Deposits
    g['Liquid_Assets_Ratio'] = safe_div(g['A2'] + g['A3'] + g['A5'], g['A1']) * 100
    g['Securities_Ratio'] = safe_div(g['A18'], g['A1']) * 100  # Investment securities / Total assets
    # Loan maturity structure
    if 'C39' in g.columns:
        g['Short_Term_Loan'] = safe_div(g['C39'], g['C38']) * 100
    if 'C40' in g.columns:
        g['Medium_Term_Loan'] = safe_div(g['C40'], g['C38']) * 100
    if 'C41' in g.columns:
        g['Long_Term_Loan'] = safe_div(g['C41'], g['C38']) * 100
    # Interbank position
    if 'A5' in g.columns and 'A53' in g.columns:
        g['Interbank_Net'] = g['A5'] - g['A53']  # positive = net lender
        g['Net_Lender'] = g['Interbank_Net'] > 0
    # Credit-deposit gap growth
    g_sorted = g.sort_values(['Bank', 'Year'])
    g_sorted['LDR_yoy'] = g_sorted.groupby('Bank')['LDR'].diff()
    
    # Yearly trend
    yearly_agg = {'LDR_mean': ('LDR', 'mean'), 'LDR_median': ('LDR', 'median'),
                  'Liquid_mean': ('Liquid_Assets_Ratio', 'mean'),
                  'Securities_mean': ('Securities_Ratio', 'mean')}
    if 'Short_Term_Loan' in g.columns:
        yearly_agg['ST_Loan_mean'] = ('Short_Term_Loan', 'mean')
    if 'Long_Term_Loan' in g.columns:
        yearly_agg['LT_Loan_mean'] = ('Long_Term_Loan', 'mean')
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index()
    
    # Bank-level
    recent = g[g['Year'] >= 2022]
    bank_agg = {'LDR_avg': ('LDR', 'mean'), 'Liquid_avg': ('Liquid_Assets_Ratio', 'mean'),
                'Securities_avg': ('Securities_Ratio', 'mean')}
    if 'Short_Term_Loan' in g.columns:
        bank_agg['ST_avg'] = ('Short_Term_Loan', 'mean')
    if 'Long_Term_Loan' in g.columns:
        bank_agg['LT_avg'] = ('Long_Term_Loan', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('LDR_avg', ascending=True)
    
    latest_year = int(g['Year'].max())
    
    # Build MD
    md = []
    md.append("# Nhom 7: Thanh khoan & LDR\n")
    md.append(f"> Phan tich du lieu {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append("## 1. Xu huong LDR & Thanh khoan toan nganh\n")
    header = "| Nam | LDR TB (%) | LDR Median (%) | Liquid Assets (%) | CK Dau tu/TTS (%)"
    sep = "|-----|-----------|----------------|------------------|------------------"
    if 'ST_Loan_mean' in yearly.columns:
        header += " | Cho vay NH (%) | Cho vay DH (%)"
        sep += "|---------------|--------------"
    header += " |"
    md.append(header)
    md.append(sep)
    for _, r in yearly.iterrows():
        row = f"| {int(r['Year'])} | {fmt_pct(r['LDR_mean'])} | {fmt_pct(r['LDR_median'])} | {fmt_pct(r['Liquid_mean'])} | {fmt_pct(r['Securities_mean'])}"
        if 'ST_Loan_mean' in yearly.columns:
            row += f" | {fmt_pct(r.get('ST_Loan_mean', np.nan))} | {fmt_pct(r.get('LT_Loan_mean', np.nan))}"
        row += " |"
        md.append(row)
    
    md.append(f"\n## 2. Xep hang LDR (TB 2022--{latest_year})\n")
    md.append("### Top 5 LDR thap nhat (thanh khoan tot)\n")
    md.append("| Bank | LDR (%) | Liquid Assets (%) | CK DT (%) | Cho vay NH (%) | Cho vay DH (%) |")
    md.append("|------|---------|------------------|---------|---------------|--------------|")
    for _, r in bank_avg.head(5).iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['LDR_avg'])} | {fmt_pct(r['Liquid_avg'])} | {fmt_pct(r['Securities_avg'])} | {fmt_pct(r.get('ST_avg', np.nan))} | {fmt_pct(r.get('LT_avg', np.nan))} |")
    
    md.append("\n### Top 5 LDR cao nhat (rui ro thanh khoan)\n")
    md.append("| Bank | LDR (%) | Liquid Assets (%) | CK DT (%) | Cho vay NH (%) | Cho vay DH (%) |")
    md.append("|------|---------|------------------|---------|---------------|--------------|")
    for _, r in bank_avg.tail(5).iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['LDR_avg'])} | {fmt_pct(r['Liquid_avg'])} | {fmt_pct(r['Securities_avg'])} | {fmt_pct(r.get('ST_avg', np.nan))} | {fmt_pct(r.get('LT_avg', np.nan))} |")
    
    # Interbank position
    if 'Net_Lender' in g.columns:
        latest = g[g['Year'] == latest_year][['Bank', 'Interbank_Net', 'Net_Lender']].sort_values('Interbank_Net', ascending=False)
        md.append(f"\n## 3. Vi the lien ngan hang -- {latest_year}\n")
        md.append("| Bank | Net Interbank | Vi the |")
        md.append("|------|--------------|--------|")
        for _, r in latest.iterrows():
            md.append(f"| {int(r['Bank'])} | {fmt_num(r['Interbank_Net'])} | {'Net Lender' if r['Net_Lender'] else 'Net Borrower'} |")
    
    md.append("\n## 4. Key Insights\n")
    ldr_first = yearly.iloc[0]['LDR_mean']
    ldr_last = yearly.iloc[-1]['LDR_mean']
    md.append(f"1. **LDR toan nganh**: LDR TB {'tang' if ldr_last > ldr_first else 'giam'} tu {ldr_first:.2f}% den {ldr_last:.2f}%. {'Ap luc thanh khoan gia tang.' if ldr_last > 90 else 'Van trong nguong an toan.'}")
    
    high_ldr = bank_avg[bank_avg['LDR_avg'] > 100]
    md.append(f"\n2. **Vuot tran LDR**: {len(high_ldr)} NH co LDR >100% — cho vay vuot kha nang huy dong tien gui.")
    
    if 'LT_avg' in bank_avg.columns:
        high_lt = bank_avg[bank_avg['LT_avg'] > 40]
        md.append(f"\n3. **Rui ro ky han**: {len(high_lt)} NH co cho vay dai han >40% — rui ro maturity mismatch khi huy dong chu yeu ngan han.")
    
    low_liquid = bank_avg[bank_avg['Liquid_avg'] < 5]
    md.append(f"\n4. **Dem thanh khoan mong**: {len(low_liquid)} NH co liquid assets <5% TTS — kha nang chong do ap luc rut tien yeu.")
    
    content = "\n".join(md)
    write_insight("group07_liquidity_ldr.md", content)
    print("  [OK] Group 7 complete.")

# ============================================================
# NHÓM 8: Credit Portfolio Concentration
# ============================================================
def analyze_group8():
    print("\n" + "="*60)
    print("NHOM 8: Credit Concentration -- Sector / Customer Mix")
    print("="*60)
    
    sector_cols = ['C5','C6','C7','C12','C22','C23','C24','C25','C26','C27','C28','C29','C30','C31']
    customer_cols = ['C42','C43','C44','C45','C46','C47','C48']
    cols = ['Bank','Year','A13','C4'] + sector_cols + customer_cols
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # Sector shares
    for c in sector_cols:
        if c in g.columns:
            g[f'{c}_share'] = safe_div(g[c], g['A13']) * 100
    
    # Real estate exposure
    if 'C28' in g.columns:
        g['RE_exposure'] = safe_div(g['C28'], g['A13']) * 100
    # Retail (ca nhan) vs Corporate
    if 'C47' in g.columns:
        g['Retail_Share'] = safe_div(g['C47'], g['A13']) * 100
    # SOE lending
    if 'C43' in g.columns:
        g['SOE_Share'] = safe_div(g['C43'], g['A13']) * 100
    
    # HHI (sector concentration)
    hhi_list = []
    for _, row in g.iterrows():
        shares = []
        for c in sector_cols:
            if c in g.columns and not pd.isna(row.get(c)) and not pd.isna(row['A13']) and row['A13'] > 0:
                s = row[c] / row['A13']
                shares.append(s)
        if shares:
            hhi = sum(s**2 for s in shares) * 10000
            hhi_list.append(hhi)
        else:
            hhi_list.append(np.nan)
    g['HHI'] = hhi_list
    
    # Yearly
    yearly_agg = {'HHI_mean': ('HHI', 'mean')}
    if 'RE_exposure' in g.columns:
        yearly_agg['RE_mean'] = ('RE_exposure', 'mean')
    if 'Retail_Share' in g.columns:
        yearly_agg['Retail_mean'] = ('Retail_Share', 'mean')
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index()
    
    # Bank-level
    recent = g[g['Year'] >= 2022]
    bank_agg = {'HHI_avg': ('HHI', 'mean')}
    if 'RE_exposure' in g.columns:
        bank_agg['RE_avg'] = ('RE_exposure', 'mean')
    if 'Retail_Share' in g.columns:
        bank_agg['Retail_avg'] = ('Retail_Share', 'mean')
    if 'SOE_Share' in g.columns:
        bank_agg['SOE_avg'] = ('SOE_Share', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('HHI_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    md = []
    md.append("# Nhom 8: Tap trung danh muc tin dung\n")
    md.append(f"> Phan tich {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append("## 1. Xu huong tap trung toan nganh\n")
    md.append("| Nam | HHI TB | BDS TB (%) | Retail TB (%) |")
    md.append("|-----|--------|-----------|--------------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_num(r['HHI_mean'])} | {fmt_pct(r.get('RE_mean', np.nan))} | {fmt_pct(r.get('Retail_mean', np.nan))} |")
    
    md.append(f"\n## 2. Xep hang tap trung (TB 2022--{latest_year})\n")
    md.append("| Bank | HHI | BDS (%) | Retail (%) | DNNN (%) |")
    md.append("|------|-----|---------|-----------|---------|")
    for _, r in bank_avg.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_num(r['HHI_avg'])} | {fmt_pct(r.get('RE_avg', np.nan))} | {fmt_pct(r.get('Retail_avg', np.nan))} | {fmt_pct(r.get('SOE_avg', np.nan))} |")
    
    # COVID sensitive sectors
    if 'C29' in g.columns:
        g['Hotel_Restaurant'] = safe_div(g['C29'], g['A13']) * 100
    if 'C22' in g.columns:
        g['Transport'] = safe_div(g['C22'], g['A13']) * 100
    
    md.append("\n## 3. Key Insights\n")
    hhi_last = yearly.iloc[-1]['HHI_mean']
    md.append(f"1. **HHI**: HHI trung binh {hhi_last:.0f} — {'tap trung cao (>2500)' if hhi_last > 2500 else 'tap trung trung binh (1500-2500)' if hhi_last > 1500 else 'phan tan (<1500)'}.")
    
    if 'RE_avg' in bank_avg.columns:
        high_re = bank_avg[bank_avg['RE_avg'] > 20]
        md.append(f"\n2. **Phoi nhiem BDS**: {len(high_re)} NH co ty le cho vay BDS >20% — rui ro tap trung lon.")
    
    if 'Retail_avg' in bank_avg.columns:
        retail_trend_first = yearly.iloc[0].get('Retail_mean', np.nan)
        retail_trend_last = yearly.iloc[-1].get('Retail_mean', np.nan)
        if not pd.isna(retail_trend_first) and not pd.isna(retail_trend_last):
            md.append(f"\n3. **Ban le hoa**: Ty le cho vay ca nhan {'tang' if retail_trend_last > retail_trend_first else 'giam'} tu {retail_trend_first:.1f}% len {retail_trend_last:.1f}%.")
    
    content = "\n".join(md)
    write_insight("group08_credit_concentration.md", content)
    print("  [OK] Group 8 complete.")


# ============================================================
# NHÓM 9: Investment Portfolio & Market Sensitivity
# ============================================================
def analyze_group9():
    print("\n" + "="*60)
    print("NHOM 9: Investment & Market Risk")
    print("="*60)
    
    cols = ['Bank','Year','A1','A8','A9','A10','A11','A18','A19','A20','A21',
            'C49','C50','C51','C52','C53','C54','C55','C56','C57','C58','C59','C60','C61','C62','C63','C64','C65','C66',
            'B7','B8','B9']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # Metrics
    g['Inv_to_Assets'] = safe_div(g['A18'], g['A1']) * 100
    g['Trading_to_Assets'] = safe_div(g['A8'], g['A1']) * 100
    if 'A19' in g.columns and 'A20' in g.columns:
        g['AFS_Share'] = safe_div(g['A19'], g['A18']) * 100  # Available for sale
        g['HTM_Share'] = safe_div(g['A20'], g['A18']) * 100  # Hold to maturity
    if 'C52' in g.columns and 'C60' in g.columns:
        g['GovBond_Share'] = safe_div(g.get('C52', 0) + g.get('C60', 0), g['A18']) * 100
    if 'C55' in g.columns and 'C63' in g.columns:
        g['CorpBond_Share'] = safe_div(g.get('C55', 0) + g.get('C63', 0), g['A18']) * 100
    if 'C64' in g.columns:
        g['VAMC_Share'] = safe_div(g['C64'], g['A18']) * 100
    if 'A11' in g.columns:
        g['Derivative_to_Assets'] = safe_div(g['A11'], g['A1']) * 100
    # Provision coverage for securities
    if 'A21' in g.columns:
        g['Sec_Provision_Ratio'] = safe_div(g['A21'].abs(), g['A18']) * 100
    
    # Yearly
    yearly_agg = {'Inv_mean': ('Inv_to_Assets', 'mean')}
    if 'GovBond_Share' in g.columns:
        yearly_agg['GovBond_mean'] = ('GovBond_Share', 'mean')
    if 'VAMC_Share' in g.columns:
        yearly_agg['VAMC_mean'] = ('VAMC_Share', 'mean')
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index()
    
    # Bank-level
    recent = g[g['Year'] >= 2022]
    bank_agg = {'Inv_avg': ('Inv_to_Assets', 'mean')}
    if 'AFS_Share' in g.columns:
        bank_agg['AFS_avg'] = ('AFS_Share', 'mean')
    if 'HTM_Share' in g.columns:
        bank_agg['HTM_avg'] = ('HTM_Share', 'mean')
    if 'GovBond_Share' in g.columns:
        bank_agg['GovBond_avg'] = ('GovBond_Share', 'mean')
    if 'CorpBond_Share' in g.columns:
        bank_agg['CorpBond_avg'] = ('CorpBond_Share', 'mean')
    if 'VAMC_Share' in g.columns:
        bank_agg['VAMC_avg'] = ('VAMC_Share', 'mean')
    if 'Derivative_to_Assets' in g.columns:
        bank_agg['Deriv_avg'] = ('Derivative_to_Assets', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('Inv_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    md = []
    md.append("# Nhom 9: Danh muc dau tu & Rui ro thi truong\n")
    md.append(f"> Phan tich {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append("## 1. Xu huong dau tu toan nganh\n")
    md.append("| Nam | CK DT/TTS (%) | TPCP (%) | VAMC (%) |")
    md.append("|-----|--------------|---------|---------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_pct(r['Inv_mean'])} | {fmt_pct(r.get('GovBond_mean', np.nan))} | {fmt_pct(r.get('VAMC_mean', np.nan))} |")
    
    md.append(f"\n## 2. Cau truc dau tu theo NH (TB 2022--{latest_year})\n")
    md.append("| Bank | CK DT/TTS (%) | AFS (%) | HTM (%) | TPCP (%) | TPDN (%) | VAMC (%) | Phai sinh/TTS (%) |")
    md.append("|------|--------------|---------|---------|---------|---------|---------|------------------|")
    for _, r in bank_avg.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Inv_avg'])} | {fmt_pct(r.get('AFS_avg', np.nan))} | {fmt_pct(r.get('HTM_avg', np.nan))} | {fmt_pct(r.get('GovBond_avg', np.nan))} | {fmt_pct(r.get('CorpBond_avg', np.nan))} | {fmt_pct(r.get('VAMC_avg', np.nan))} | {fmt_pct(r.get('Deriv_avg', np.nan))} |")
    
    md.append("\n## 3. Key Insights\n")
    if 'VAMC_avg' in bank_avg.columns:
        vamc_positive = bank_avg[bank_avg['VAMC_avg'] > 0.1]
        md.append(f"1. **VAMC bonds**: {len(vamc_positive)} NH con nam giu trai phieu dac biet VAMC — no xau an chua xu ly xong.")
    if 'CorpBond_avg' in bank_avg.columns:
        high_corp = bank_avg[bank_avg['CorpBond_avg'] > 10]
        md.append(f"\n2. **TPDN**: {len(high_corp)} NH co ty trong TPDN >10% danh muc CK DT — rui ro tin dung doanh nghiep.")
    if 'Deriv_avg' in bank_avg.columns:
        using_deriv = bank_avg[bank_avg['Deriv_avg'] > 0.01]
        md.append(f"\n3. **Su dung phai sinh**: {len(using_deriv)} NH su dung cong cu phai sinh — quan tri rui ro tinh vi hon.")
    
    content = "\n".join(md)
    write_insight("group09_investment_market.md", content)
    print("  [OK] Group 9 complete.")


# ============================================================
# NHÓM 10: Capital Adequacy
# ============================================================
def analyze_group10():
    print("\n" + "="*60)
    print("NHOM 10: Capital Adequacy -- Equity Structure")
    print("="*60)
    
    cols = ['Bank','Year','A1','A49','A64','A65','A66','A67','A68','A69','A70','A71','A72','A73','A74','A75','A76']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # Metrics
    g['Equity_Ratio'] = safe_div(g['A64'], g['A1']) * 100
    g['Retained_Earnings_Ratio'] = safe_div(g['A75'], g['A64']) * 100
    if 'A68' in g.columns:
        g['Share_Premium_Ratio'] = safe_div(g['A68'], g['A64']) * 100
    if 'A76' in g.columns:
        g['Minority_Interest_Ratio'] = safe_div(g['A76'], g['A64']) * 100
    if 'A66' in g.columns:
        g['Charter_to_Equity'] = safe_div(g['A66'], g['A64']) * 100
    
    # Charter capital growth
    cap_growth = []
    for bank in g['Bank'].unique():
        bd = g[g['Bank'] == bank].sort_values('Year')
        if len(bd) >= 2 and 'A66' in bd.columns:
            first = bd.iloc[0]['A66']
            last = bd.iloc[-1]['A66']
            n = bd.iloc[-1]['Year'] - bd.iloc[0]['Year']
            if first > 0 and last > 0 and n > 0:
                cagr = ((last/first)**(1/n) - 1) * 100
                cap_growth.append({'Bank': bank, 'Cap_CAGR': cagr, 'Cap_2024': last})
    cap_growth_df = pd.DataFrame(cap_growth).sort_values('Cap_CAGR', ascending=False) if cap_growth else pd.DataFrame()
    
    # Yearly
    yearly = g.groupby('Year').agg(
        Equity_mean=('Equity_Ratio', 'mean'),
        Equity_median=('Equity_Ratio', 'median'),
        Retained_mean=('Retained_Earnings_Ratio', 'mean'),
    ).reset_index()
    
    # Bank-level
    recent = g[g['Year'] >= 2022]
    bank_agg = {'Equity_avg': ('Equity_Ratio', 'mean'), 'Retained_avg': ('Retained_Earnings_Ratio', 'mean')}
    if 'Share_Premium_Ratio' in g.columns:
        bank_agg['Premium_avg'] = ('Share_Premium_Ratio', 'mean')
    if 'Charter_to_Equity' in g.columns:
        bank_agg['Charter_pct'] = ('Charter_to_Equity', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('Equity_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    md = []
    md.append("# Nhom 10: An toan von & Cau truc VCSH\n")
    md.append(f"> Phan tich {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append("## 1. Xu huong Equity Ratio toan nganh\n")
    md.append("| Nam | Equity/TTS TB (%) | Equity/TTS Median (%) | LN chua PP/VCSH (%) |")
    md.append("|-----|------------------|----------------------|---------------------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_pct(r['Equity_mean'])} | {fmt_pct(r['Equity_median'])} | {fmt_pct(r['Retained_mean'])} |")
    
    md.append(f"\n## 2. Xep hang an toan von (TB 2022--{latest_year})\n")
    md.append("| Bank | Equity/TTS (%) | LN chua PP/VCSH (%) | Thang du/VCSH (%) | VDL/VCSH (%) |")
    md.append("|------|---------------|---------------------|-------------------|-------------|")
    for _, r in bank_avg.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Equity_avg'])} | {fmt_pct(r['Retained_avg'])} | {fmt_pct(r.get('Premium_avg', np.nan))} | {fmt_pct(r.get('Charter_pct', np.nan))} |")
    
    if not cap_growth_df.empty:
        md.append(f"\n## 3. Tang truong von dieu le (CAGR)\n")
        md.append("| Bank | VDL hien tai | VDL CAGR (%) |")
        md.append("|------|------------|-------------|")
        for _, r in cap_growth_df.iterrows():
            md.append(f"| {int(r['Bank'])} | {fmt_num(r['Cap_2024'])} | {fmt_pct(r['Cap_CAGR'])} |")
    
    md.append("\n## 4. Key Insights\n")
    eq_first = yearly.iloc[0]['Equity_mean']
    eq_last = yearly.iloc[-1]['Equity_mean']
    md.append(f"1. **Equity Ratio toan nganh**: {'Tang' if eq_last > eq_first else 'Giam'} tu {eq_first:.2f}% den {eq_last:.2f}%.")
    
    thin_cap = bank_avg[bank_avg['Equity_avg'] < 6]
    md.append(f"\n2. **Von mong**: {len(thin_cap)} NH co Equity/TTS <6% — dem von mong, rui ro cao.")
    
    eq_range = bank_avg['Equity_avg'].max() - bank_avg['Equity_avg'].min()
    md.append(f"\n3. **Phan hoa von**: Chenh lech Equity Ratio {eq_range:.2f}pp giua NH manh nhat va yeu nhat.")
    
    content = "\n".join(md)
    write_insight("group10_capital_adequacy.md", content)
    print("  [OK] Group 10 complete.")

# ============================================================
# NHÓM 11: ALM — Cấu trúc kỳ hạn
# ============================================================
def analyze_group11():
    print("\n" + "="*60)
    print("NHOM 11: ALM -- Maturity Mismatch")
    print("="*60)
    
    cols = ['Bank','Year','C38','C39','C40','C41','C68','C69','C70','A55','A58','B1','B2']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    if 'C39' in g.columns:
        g['Short_Loan_Pct'] = safe_div(g['C39'], g['C38']) * 100
    if 'C40' in g.columns:
        g['Medium_Loan_Pct'] = safe_div(g['C40'], g['C38']) * 100
    if 'C41' in g.columns:
        g['Long_Loan_Pct'] = safe_div(g['C41'], g['C38']) * 100
    if 'C68' in g.columns:
        g['Demand_Deposit_Pct'] = safe_div(g['C68'], g['A55']) * 100
    if 'C69' in g.columns:
        g['Term_Deposit_Pct'] = safe_div(g['C69'], g['A55']) * 100
    if 'A58' in g.columns:
        g['Bond_to_Deposits'] = safe_div(g['A58'], g['A55']) * 100
    # Maturity gap proxy: Long-term loan % - Term deposit %
    if 'Long_Loan_Pct' in g.columns and 'Term_Deposit_Pct' in g.columns:
        g['Maturity_Gap'] = g['Long_Loan_Pct'] - g['Term_Deposit_Pct']
    
    yearly_agg = {}
    for m in ['Short_Loan_Pct', 'Long_Loan_Pct', 'Demand_Deposit_Pct', 'Bond_to_Deposits']:
        if m in g.columns:
            yearly_agg[f'{m}_mean'] = (m, 'mean')
    yearly = g.groupby('Year').agg(**yearly_agg).reset_index() if yearly_agg else pd.DataFrame()
    
    recent = g[g['Year'] >= 2022]
    bank_agg = {}
    for m in ['Short_Loan_Pct', 'Medium_Loan_Pct', 'Long_Loan_Pct', 'Demand_Deposit_Pct', 'Term_Deposit_Pct', 'Bond_to_Deposits', 'Maturity_Gap']:
        if m in g.columns:
            bank_agg[f'{m}_avg'] = (m, 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index()
    if 'Long_Loan_Pct_avg' in bank_avg.columns:
        bank_avg = bank_avg.sort_values('Long_Loan_Pct_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    md = []
    md.append("# Nhom 11: Cau truc ky han & ALM\n")
    md.append(f"> Phan tich {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    if not yearly.empty:
        md.append("## 1. Xu huong cau truc ky han toan nganh\n")
        md.append("| Nam | Cho vay NH (%) | Cho vay DH (%) | TG Khong KH (%) | GTCG/TG (%) |")
        md.append("|-----|---------------|---------------|----------------|------------|")
        for _, r in yearly.iterrows():
            md.append(f"| {int(r['Year'])} | {fmt_pct(r.get('Short_Loan_Pct_mean', np.nan))} | {fmt_pct(r.get('Long_Loan_Pct_mean', np.nan))} | {fmt_pct(r.get('Demand_Deposit_Pct_mean', np.nan))} | {fmt_pct(r.get('Bond_to_Deposits_mean', np.nan))} |")
    
    md.append(f"\n## 2. Chi tiet ALM theo NH (TB 2022--{latest_year})\n")
    md.append("| Bank | CV NH (%) | CV TH (%) | CV DH (%) | TG KKH (%) | TG CKH (%) | GTCG/TG (%) | Gap (pp) |")
    md.append("|------|---------|---------|---------|----------|----------|-----------|---------|")
    for _, r in bank_avg.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r.get('Short_Loan_Pct_avg', np.nan))} | {fmt_pct(r.get('Medium_Loan_Pct_avg', np.nan))} | {fmt_pct(r.get('Long_Loan_Pct_avg', np.nan))} | {fmt_pct(r.get('Demand_Deposit_Pct_avg', np.nan))} | {fmt_pct(r.get('Term_Deposit_Pct_avg', np.nan))} | {fmt_pct(r.get('Bond_to_Deposits_avg', np.nan))} | {fmt_pct(r.get('Maturity_Gap_avg', np.nan))} |")
    
    md.append("\n## 3. Key Insights\n")
    if 'Long_Loan_Pct_avg' in bank_avg.columns:
        high_lt = bank_avg[bank_avg['Long_Loan_Pct_avg'] > 40]
        md.append(f"1. **Cho vay dai han**: {len(high_lt)} NH co >40% cho vay dai han — rui ro lai suat cao khi huy dong chu yeu ngan han.")
    if 'Maturity_Gap_avg' in bank_avg.columns:
        high_gap = bank_avg[bank_avg['Maturity_Gap_avg'] > 0]
        md.append(f"\n2. **Maturity Gap**: {len(high_gap)} NH co gap duong (cho vay DH > TG co ky han) — ap luc tai cap von khi lai suat tang.")
    if 'Bond_to_Deposits_avg' in bank_avg.columns:
        high_bond = bank_avg[bank_avg['Bond_to_Deposits_avg'] > 5]
        md.append(f"\n3. **Phat hanh GTCG**: {len(high_bond)} NH co GTCG/TG >5% — dang keo dai ky han no de cai thien ALM.")
    
    content = "\n".join(md)
    write_insight("group11_alm.md", content)
    print("  [OK] Group 11 complete.")


# ============================================================
# NHÓM 12: Strategic Investments
# ============================================================
def analyze_group12():
    print("\n" + "="*60)
    print("NHOM 12: Strategic Investments -- Subsidiaries / Fixed Assets")
    print("="*60)
    
    cols = ['Bank','Year','A1','A22','A23','A24','A25','A26','A27','A28','A29',
            'A30','A31','A32','A33','A34','A35','A36','A37','A38','A39','A40','A41','A47','B13']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    g['LT_Inv_Ratio'] = safe_div(g['A22'], g['A1']) * 100
    if 'A23' in g.columns:
        g['Subsidiary_Ratio'] = safe_div(g['A23'], g['A1']) * 100
    g['Fixed_Asset_Ratio'] = safe_div(g['A29'], g['A1']) * 100
    if 'A36' in g.columns:
        g['Intangible_Ratio'] = safe_div(g['A36'], g['A1']) * 100
    if 'A47' in g.columns:
        g['Goodwill_Ratio'] = safe_div(g['A47'], g['A1']) * 100
    if 'B13' in g.columns and 'A22' in g.columns:
        g['Inv_Yield'] = safe_div(g['B13'], g['A22']) * 100
    if 'A39' in g.columns:
        g['Inv_RE_Ratio'] = safe_div(g['A39'], g['A1']) * 100
    
    recent = g[g['Year'] >= 2022]
    bank_agg = {'LT_Inv_avg': ('LT_Inv_Ratio', 'mean'), 'Fixed_avg': ('Fixed_Asset_Ratio', 'mean')}
    if 'Subsidiary_Ratio' in g.columns:
        bank_agg['Sub_avg'] = ('Subsidiary_Ratio', 'mean')
    if 'Intangible_Ratio' in g.columns:
        bank_agg['Intangible_avg'] = ('Intangible_Ratio', 'mean')
    if 'Goodwill_Ratio' in g.columns:
        bank_agg['Goodwill_avg'] = ('Goodwill_Ratio', 'mean')
    if 'Inv_Yield' in g.columns:
        bank_agg['Yield_avg'] = ('Inv_Yield', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('LT_Inv_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    md = []
    md.append("# Nhom 12: Dau tu dai han & Cong ty con\n")
    md.append(f"> Phan tich {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append(f"## 1. Cau truc dau tu dai han (TB 2022--{latest_year})\n")
    md.append("| Bank | DT DH/TTS (%) | Cong ty con (%) | TSCD/TTS (%) | TS Vo hinh (%) | Goodwill (%) | Yield DT (%) |")
    md.append("|------|--------------|----------------|-------------|---------------|-------------|-------------|")
    for _, r in bank_avg.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['LT_Inv_avg'])} | {fmt_pct(r.get('Sub_avg', np.nan))} | {fmt_pct(r['Fixed_avg'])} | {fmt_pct(r.get('Intangible_avg', np.nan))} | {fmt_pct(r.get('Goodwill_avg', np.nan))} | {fmt_pct(r.get('Yield_avg', np.nan))} |")
    
    md.append("\n## 2. Key Insights\n")
    if 'Sub_avg' in bank_avg.columns:
        has_sub = bank_avg[bank_avg['Sub_avg'] > 0.1]
        md.append(f"1. **Cong ty con**: {len(has_sub)} NH co dau tu cong ty con dang ke — chien luoc tap doan hoa (bao hiem, chung khoan, fintech).")
    if 'Goodwill_avg' in bank_avg.columns:
        has_gw = bank_avg[bank_avg['Goodwill_avg'] > 0.01]
        md.append(f"\n2. **Goodwill (M&A)**: {len(has_gw)} NH co goodwill — da thuc hien M&A, can theo doi rui ro suy giam gia tri.")
    if 'Intangible_avg' in bank_avg.columns:
        high_intangible = bank_avg[bank_avg['Intangible_avg'] > bank_avg['Intangible_avg'].median()]
        md.append(f"\n3. **TSCD vo hinh (IT proxy)**: {len(high_intangible)} NH co ty le TS vo hinh tren median — co the phan anh dau tu cong nghe/phan mem.")
    
    content = "\n".join(md)
    write_insight("group12_strategic_investments.md", content)
    print("  [OK] Group 12 complete.")


# ============================================================
# NHÓM 13: Earnings Quality & Tax
# ============================================================
def analyze_group13():
    print("\n" + "="*60)
    print("NHOM 13: Earnings Quality -- Core / Non-Recurring / Tax")
    print("="*60)
    
    cols = ['Bank','Year','B14','B16','B17','B18','B19','B20','B21','B22','B23','B24',
            'B10','B11','B12','C127','C128','C129','C130','C131','C132','C133','C134','C135','C136','C137','C138','C139',
            'A45','A61']
    existing = [c for c in cols if c in df.columns]
    g = df[existing].copy()
    
    # Core earnings ratio
    g['Core_Earnings_Ratio'] = safe_div(g['B16'], g['B18']) * 100
    # Provisioning impact
    g['Prov_Impact'] = safe_div(g['B17'].abs(), g['B16']) * 100
    # Non-recurring income
    g['NonRecurring_Ratio'] = safe_div(g['B12'], g['B14']) * 100
    # Effective tax rate
    g['Eff_Tax_Rate'] = safe_div(g['B21'].abs(), g['B18']) * 100
    # Minority interest drag
    if 'B23' in g.columns:
        g['Minority_Drag'] = safe_div(g['B23'].abs(), g['B22']) * 100
    # VAMC income
    if 'C131' in g.columns:
        g['VAMC_Income_Ratio'] = safe_div(g['C131'], g['B14']) * 100
    # Bad debt recovery
    if 'C128' in g.columns:
        g['BadDebt_Recovery_Ratio'] = safe_div(g['C128'], g['B14']) * 100
    # Deferred tax position
    if 'A45' in g.columns and 'A61' in g.columns:
        g['Net_DTA'] = g['A45'] - g['A61']
    
    # Yearly
    yearly = g.groupby('Year').agg(
        Core_mean=('Core_Earnings_Ratio', 'mean'),
        Prov_mean=('Prov_Impact', 'mean'),
        NonRecur_mean=('NonRecurring_Ratio', 'mean'),
        Tax_mean=('Eff_Tax_Rate', 'mean'),
    ).reset_index()
    
    # Bank-level
    recent = g[g['Year'] >= 2022]
    bank_agg = {
        'Core_avg': ('Core_Earnings_Ratio', 'mean'),
        'Prov_avg': ('Prov_Impact', 'mean'),
        'NonRecur_avg': ('NonRecurring_Ratio', 'mean'),
        'Tax_avg': ('Eff_Tax_Rate', 'mean'),
    }
    if 'Minority_Drag' in g.columns:
        bank_agg['Minority_avg'] = ('Minority_Drag', 'mean')
    if 'VAMC_Income_Ratio' in g.columns:
        bank_agg['VAMC_Inc_avg'] = ('VAMC_Income_Ratio', 'mean')
    if 'BadDebt_Recovery_Ratio' in g.columns:
        bank_agg['Recovery_avg'] = ('BadDebt_Recovery_Ratio', 'mean')
    bank_avg = recent.groupby('Bank').agg(**bank_agg).reset_index().sort_values('Core_avg', ascending=False)
    
    latest_year = int(g['Year'].max())
    
    md = []
    md.append("# Nhom 13: Chat luong loi nhuan & Thue\n")
    md.append(f"> Phan tich {int(g['Year'].min())}--{latest_year}, {g['Bank'].nunique()} NH.\n")
    
    md.append("## 1. Xu huong chat luong LN toan nganh\n")
    md.append("| Nam | Core Earnings (%) | Prov/PPOP (%) | Non-Recurring (%) | Eff Tax Rate (%) |")
    md.append("|-----|------------------|--------------|-------------------|-----------------|")
    for _, r in yearly.iterrows():
        md.append(f"| {int(r['Year'])} | {fmt_pct(r['Core_mean'])} | {fmt_pct(r['Prov_mean'])} | {fmt_pct(r['NonRecur_mean'])} | {fmt_pct(r['Tax_mean'])} |")
    
    md.append(f"\n## 2. Chi tiet chat luong LN (TB 2022--{latest_year})\n")
    md.append("| Bank | Core (%) | Prov/PPOP (%) | Non-Recur (%) | Eff Tax (%) | VAMC Inc (%) | Thu hoi no (%) | CDTS (%) |")
    md.append("|------|---------|--------------|--------------|------------|-------------|---------------|---------|")
    for _, r in bank_avg.iterrows():
        md.append(f"| {int(r['Bank'])} | {fmt_pct(r['Core_avg'])} | {fmt_pct(r['Prov_avg'])} | {fmt_pct(r['NonRecur_avg'])} | {fmt_pct(r['Tax_avg'])} | {fmt_pct(r.get('VAMC_Inc_avg', np.nan))} | {fmt_pct(r.get('Recovery_avg', np.nan))} | {fmt_pct(r.get('Minority_avg', np.nan))} |")
    
    md.append("\n## 3. Key Insights\n")
    
    core_last = yearly.iloc[-1]['Core_mean']
    md.append(f"1. **Core Earnings**: PPOP chiem trung binh {core_last:.1f}% LNTT — {'loi nhuan cot loi on dinh.' if core_last > 90 else 'co thanh phan khong cot loi dang ke.'}")
    
    high_nonrecur = bank_avg[bank_avg['NonRecur_avg'] > 10]
    md.append(f"\n2. **Thu nhap khong ben vung**: {len(high_nonrecur)} NH co thu nhap khac >10% TOI — chat luong LN khong ben vung.")
    
    tax_deviation = bank_avg[bank_avg['Tax_avg'] < 18]
    md.append(f"\n3. **Thue suat thuc te**: {len(tax_deviation)} NH co thue suat thuc te <18% (thap hon danh nghia 20%) — co the do uu dai thue hoac chenh lech ke toan.")
    
    if 'Recovery_avg' in bank_avg.columns:
        high_recovery = bank_avg[bank_avg['Recovery_avg'] > 1]
        md.append(f"\n4. **Thu hoi no xau**: {len(high_recovery)} NH co thu hoi no/TOI >1% — hieu qua xu ly no xau tot, nhung cung phan anh no xau lich su lon.")
    
    high_prov = bank_avg[bank_avg['Prov_avg'] > 50]
    md.append(f"\n5. **Ap luc du phong**: {len(high_prov)} NH co du phong/PPOP >50% — loi nhuan goc tot nhung bi bao mon nghiem trong.")
    
    content = "\n".join(md)
    write_insight("group13_earnings_quality.md", content)
    print("  [OK] Group 13 complete.")


# === RUN ===
analyze_group11()
analyze_group12()
analyze_group13()

print("\n" + "="*60)
print("ALL 13 GROUPS COMPLETED!")
print("="*60)

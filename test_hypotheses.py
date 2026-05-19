"""
Kiểm định 13 giả thuyết phân tích theo giai đoạn — G'Contest 2026
Dựa trên file hypotheses_phase_analysis.md
"""
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
import sys
sys.stdout.reconfigure(encoding='utf-8')


# ============================================================
# LOAD DATA
# ============================================================
def load_data():
    bs = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_1. Balance Sheet.csv")
    ic = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv")
    note = pd.read_csv(r"d:\uni\gcontest\[G'Contest 2026] Đề Vòng 2_3. Note.csv")
    
    df = bs.merge(ic, on=['Công ty', 'Năm'], how='outer')
    df = df.merge(note, on=['Công ty', 'Năm'], how='outer')
    
    # Convert numeric
    for c in df.columns:
        if c not in ['Công ty', 'Năm']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    
    return df

def safe_div(a, b):
    return np.where((b == 0) | b.isna() | a.isna(), np.nan, a / b)

# ============================================================
# COMPUTE METRICS
# ============================================================
def compute_metrics(df):
    m = pd.DataFrame()
    m['Bank'] = df['Công ty']
    m['Year'] = df['Năm']
    
    # Profitability
    m['ROA'] = safe_div(df['B22'], df['A1'])
    m['ROE'] = safe_div(df['B22'], df['A64'])
    m['Profit_Margin'] = safe_div(df['B22'], df['B14'])
    m['Asset_Turnover'] = safe_div(df['B14'], df['A1'])
    m['Leverage'] = safe_div(df['A1'], df['A64'])
    
    # NIM & Spread
    m['NIM'] = safe_div(df['B3'], df['A1'])
    m['CoF'] = safe_div(df['C88'], df['A55'])
    m['Yield_Loan'] = safe_div(df['C80'], df['A13'])
    m['Spread'] = m['Yield_Loan'] - m['CoF']
    
    # Asset Quality
    npl_sum = df[['C35','C36','C37']].sum(axis=1)
    m['NPL_ratio'] = safe_div(npl_sum, df['A13'])
    m['Watch_list'] = safe_div(df['C34'], df['A13'])
    m['Coverage'] = safe_div(df['A14'].abs(), npl_sum)
    m['Credit_cost'] = safe_div(df['B17'], df['A13'])
    m['Prov_PPOP'] = safe_div(df['B17'], df['B16'])
    
    # Funding & CASA
    m['CASA'] = safe_div(df['C68'], df['A55'])
    m['Wholesale'] = safe_div(df['A54'] + df['A58'], df['A50'])
    m['GTCG_ratio'] = safe_div(df['A58'], df['A55'])
    m['Deposit_Individual'] = safe_div(df['C77'], df['A55'])
    
    # Revenue Diversification
    m['Fee_ratio'] = safe_div(df['B6'], df['B14'])
    m['Non_II_ratio'] = safe_div(df['B14'] - df['B3'], df['B14'])
    m['Bancassurance'] = safe_div(df['C97'], df['B4'])
    m['Digital_proxy'] = safe_div(df['C93'], df['B4'])
    
    # Efficiency
    m['CIR'] = safe_div(df['B15'], df['B14'])
    m['PPOP_LNTT'] = safe_div(df['B16'], df['B18'])
    
    # Liquidity
    m['LDR'] = safe_div(df['A13'], df['A55'])
    m['Liquid_ratio'] = safe_div(df['A2'] + df['A3'] + df['A5'], df['A1'])
    
    # Credit Concentration
    m['RE_exposure'] = safe_div(df['C28'], df['A13'])
    m['Hotel_exposure'] = safe_div(df['C29'], df['A13'])
    m['Transport_exposure'] = safe_div(df['C22'], df['A13'])
    m['Retail_ratio'] = safe_div(df['C47'], df['A13'])
    
    # Capital
    m['Equity_ratio'] = safe_div(df['A64'], df['A1'])
    
    # ALM
    m['LT_loan_ratio'] = safe_div(df['C41'], df['C39'] + df['C40'] + df['C41'])
    
    # Earnings Quality
    m['Non_recurring'] = safe_div(df['B12'], df['B14'])
    m['Recovery_ratio'] = safe_div(df['C128'], df['B14'])
    
    # VAMC
    m['VAMC'] = df['C64'].fillna(0)
    
    return m

# ============================================================
# DEFINE PHASES
# ============================================================
PHASES = {
    'GD1_COVID': [2020, 2021],
    'GD2_RECOVERY': [2022, 2023],
    'GD3_REBALANCE': [2024]
}

def phase_avg(m, years):
    return m[m['Year'].isin(years)].groupby('Bank').mean(numeric_only=True).reset_index()

# ============================================================
# TEST FUNCTIONS
# ============================================================
def test_correlation(x, y, label_x, label_y):
    mask = x.notna() & y.notna()
    if mask.sum() < 5:
        return None, None, "Không đủ dữ liệu"
    r, p = stats.pearsonr(x[mask], y[mask])
    return r, p, f"r = {r:.3f}, p = {p:.4f}"

def test_group_diff(metric, group_var, data, q=0.25):
    high = data[data[group_var] >= data[group_var].quantile(1-q)][metric].dropna()
    low = data[data[group_var] <= data[group_var].quantile(q)][metric].dropna()
    if len(high) < 3 or len(low) < 3:
        return None, None, "Không đủ dữ liệu"
    t, p = stats.mannwhitneyu(high, low, alternative='two-sided')
    return high.mean(), low.mean(), f"High={high.mean():.4f}, Low={low.mean():.4f}, p={p:.4f}"

# ============================================================
# RUN ALL HYPOTHESES
# ============================================================
def main():
    print("Loading data...")
    df = load_data()
    m = compute_metrics(df)
    
    results = []
    
    # ========== GĐ1: COVID (2020-2021) ==========
    gd1 = phase_avg(m, PHASES['GD1_COVID'])
    
    print("\n" + "="*70)
    print("GĐ1: COVID-19 (2020-2021)")
    print("="*70)
    
    # H1.1 — CASA → NIM shield
    print("\n--- H1.1: CASA là lá chắn NIM ---")
    r, p, desc = test_correlation(gd1['CASA'], gd1['NIM'], 'CASA', 'NIM')
    print(f"  CASA vs NIM: {desc}")
    r2, p2, desc2 = test_correlation(gd1['CoF'], gd1['NIM'], 'CoF', 'NIM')
    print(f"  CoF vs NIM: {desc2}")
    supported = (r is not None and r > 0 and p < 0.1) or (r2 is not None and r2 < 0 and p2 < 0.1)
    verdict = "✅ ỦNG HỘ" if supported else "⚠️ KHÔNG RÕ RÀNG"
    print(f"  → Kết luận: {verdict}")
    results.append(('H1.1', 'CASA→NIM shield (GĐ1)', verdict, f"CASA-NIM: {desc}; CoF-NIM: {desc2}"))
    
    # H1.2 — Đòn bẩy ≠ ROE
    print("\n--- H1.2: Đòn bẩy cao ≠ ROE cao ---")
    h_mean, l_mean, desc = test_group_diff('ROE', 'Leverage', gd1, q=0.25)
    print(f"  Leverage nhóm: {desc}")
    supported = h_mean is not None and h_mean < l_mean
    verdict = "✅ ỦNG HỘ" if supported else "❌ BÁC BỎ"
    print(f"  → Kết luận: {verdict} (Đòn bẩy cao ROE={'thấp hơn' if supported else 'cao hơn'})")
    results.append(('H1.2', 'Đòn bẩy cao ≠ ROE cao (GĐ1)', verdict, desc))
    
    # H1.3 — Phơi nhiễm ngành COVID → NPL sớm
    print("\n--- H1.3: Phơi nhiễm BĐS/du lịch → NPL sớm ---")
    r, p, desc = test_correlation(gd1['RE_exposure'], gd1['NPL_ratio'], 'RE_exp', 'NPL')
    print(f"  BĐS vs NPL: {desc}")
    r2, p2, desc2 = test_correlation(gd1['Hotel_exposure'], gd1['Watch_list'], 'Hotel', 'Watch_list')
    print(f"  Khách sạn vs Nợ nhóm 2: {desc2}")
    supported = (r is not None and r > 0) or (r2 is not None and r2 > 0)
    verdict = "✅ ỦNG HỘ" if (supported and (p < 0.1 or (p2 is not None and p2 < 0.1))) else ("⚠️ CHIỀU ĐÚNG NHƯNG KHÔNG CÓ Ý NGHĨA THỐNG KÊ" if supported else "❌ BÁC BỎ")
    print(f"  → Kết luận: {verdict}")
    results.append(('H1.3', 'Phơi nhiễm COVID sectors→NPL (GĐ1)', verdict, f"RE-NPL: {desc}"))
    
    # H1.4 — Cơ cấu nợ che giấu NPL
    print("\n--- H1.4: Cơ cấu nợ che giấu NPL thực ---")
    gd1_yearly = m[m['Year'].isin([2020, 2021])]
    npl_2020 = gd1_yearly[gd1_yearly['Year']==2020]['NPL_ratio'].mean()
    npl_2021 = gd1_yearly[gd1_yearly['Year']==2021]['NPL_ratio'].mean()
    wl_2020 = gd1_yearly[gd1_yearly['Year']==2020]['Watch_list'].mean()
    wl_2021 = gd1_yearly[gd1_yearly['Year']==2021]['Watch_list'].mean()
    vamc_count = (gd1['VAMC'] > 0).sum()
    print(f"  NPL: {npl_2020:.4f} (2020) → {npl_2021:.4f} (2021)")
    print(f"  Nợ nhóm 2: {wl_2020:.4f} (2020) → {wl_2021:.4f} (2021)")
    print(f"  Số NH còn VAMC: {vamc_count}")
    supported = (npl_2021 - npl_2020) < (wl_2021 - wl_2020) or vamc_count > 5
    verdict = "✅ ỦNG HỘ" if supported else "⚠️ KHÔNG RÕ RÀNG"
    print(f"  → Kết luận: {verdict}")
    results.append(('H1.4', 'Cơ cấu nợ che giấu NPL (GĐ1)', verdict, f"NPL Δ={npl_2021-npl_2020:.4f}, WL Δ={wl_2021-wl_2020:.4f}, VAMC={vamc_count}"))
    
    # ========== GĐ2: PHỤC HỒI (2022-2023) ==========
    gd2 = phase_avg(m, PHASES['GD2_RECOVERY'])
    
    print("\n" + "="*70)
    print("GĐ2: PHỤC HỒI HẬU ĐẠI DỊCH (2022-2023)")
    print("="*70)
    
    # H2.1 — Tỷ giá → NIM sụp
    print("\n--- H2.1: Áp lực tỷ giá → NIM sụp đổ ---")
    nim_2022 = m[m['Year']==2022]['NIM'].mean()
    nim_2023 = m[m['Year']==2023]['NIM'].mean()
    nim_compression_count = 0
    for bank in m['Bank'].unique():
        bd = m[m['Bank']==bank]
        n22 = bd[bd['Year']==2022]['NIM'].values
        n24 = bd[bd['Year']==2024]['NIM'].values
        if len(n22) > 0 and len(n24) > 0 and n24[0] < n22[0]:
            nim_compression_count += 1
    r, p, desc = test_correlation(gd2['CoF'], gd2['NIM'], 'CoF', 'NIM')
    print(f"  NIM: {nim_2022:.4f} (2022) → {nim_2023:.4f} (2023)")
    print(f"  NH bị nén NIM (2022→2024): {nim_compression_count}/27")
    print(f"  CoF vs NIM (GĐ2): {desc}")
    supported = nim_2023 < nim_2022 and nim_compression_count > 13
    verdict = "✅ ỦNG HỘ" if supported else "❌ BÁC BỎ"
    print(f"  → Kết luận: {verdict}")
    results.append(('H2.1', 'Tỷ giá→NIM sụp (GĐ2)', verdict, f"NIM 22={nim_2022:.4f}→23={nim_2023:.4f}, Nén={nim_compression_count}/27"))
    
    # H2.2 — LDR bùng nổ
    print("\n--- H2.2: Tín dụng > M2 → LDR bùng nổ ---")
    ldr_2022 = m[m['Year']==2022]['LDR'].mean()
    ldr_2023 = m[m['Year']==2023]['LDR'].mean()
    ldr_over_100 = (gd2['LDR'] > 1.0).sum()
    gtcg_high = (gd2['GTCG_ratio'] > 0.05).sum()
    print(f"  LDR: {ldr_2022:.4f} (2022) → {ldr_2023:.4f} (2023)")
    print(f"  NH có LDR > 100%: {ldr_over_100}")
    print(f"  NH có GTCG/TG > 5%: {gtcg_high}")
    supported = ldr_over_100 > 10 and gtcg_high > 10
    verdict = "✅ ỦNG HỘ" if supported else "⚠️ KHÔNG RÕ RÀNG"
    print(f"  → Kết luận: {verdict}")
    results.append(('H2.2', 'Credit>M2→LDR bùng (GĐ2)', verdict, f"LDR>100%: {ldr_over_100}, GTCG>5%: {gtcg_high}"))
    
    # H2.3 — Nợ xấu độ trễ
    print("\n--- H2.3: Nợ xấu bùng nổ có độ trễ ---")
    npl_2022 = m[m['Year']==2022]['NPL_ratio'].mean()
    npl_2023 = m[m['Year']==2023]['NPL_ratio'].mean()
    npl_2024 = m[m['Year']==2024]['NPL_ratio'].mean()
    wl_2022 = m[m['Year']==2022]['Watch_list'].mean()
    wl_2023 = m[m['Year']==2023]['Watch_list'].mean()
    print(f"  NPL: {npl_2022:.4f} (2022) → {npl_2023:.4f} (2023) → {npl_2024:.4f} (2024)")
    print(f"  Nợ nhóm 2: {wl_2022:.4f} (2022) → {wl_2023:.4f} (2023)")
    supported = npl_2023 > npl_2022 or npl_2024 > npl_2022
    verdict = "✅ ỦNG HỘ" if supported else "❌ BÁC BỎ"
    print(f"  → Kết luận: {verdict}")
    results.append(('H2.3', 'Nợ xấu độ trễ (GĐ2)', verdict, f"NPL 22={npl_2022:.4f}→24={npl_2024:.4f}"))
    
    # H2.4 — Lợi nhuận phục hồi ảo
    print("\n--- H2.4: Lợi nhuận phục hồi ảo ---")
    prov_heavy = (gd2['Prov_PPOP'].abs() > 0.5).sum()
    non_recur_heavy = (gd2['Non_recurring'].abs() > 0.1).sum()
    recovery_heavy = (gd2['Recovery_ratio'].abs() > 0.01).sum()
    print(f"  NH dự phòng > 50% PPOP: {prov_heavy}")
    print(f"  NH thu nhập khác > 10% TOI: {non_recur_heavy}")
    print(f"  NH thu hồi nợ > 1% TOI: {recovery_heavy}")
    supported = prov_heavy >= 3 or non_recur_heavy >= 3 or recovery_heavy > 15
    verdict = "✅ ỦNG HỘ" if supported else "❌ BÁC BỎ"
    print(f"  → Kết luận: {verdict}")
    results.append(('H2.4', 'Lợi nhuận phục hồi ảo (GĐ2)', verdict, f"Prov>50%: {prov_heavy}, NonRecur>10%: {non_recur_heavy}, Recovery>1%: {recovery_heavy}"))
    
    # ========== GĐ3: TÁI CÂN BẰNG (2024) ==========
    gd3 = phase_avg(m, PHASES['GD3_REBALANCE'])
    
    print("\n" + "="*70)
    print("GĐ3: TÁI CÂN BẰNG (2024)")
    print("="*70)
    
    # H3.1 — CASA + Fee = sống còn
    print("\n--- H3.1: CASA + Fee income = chìa khóa sống còn ---")
    r_casa, p_casa, desc_casa = test_correlation(gd3['CASA'], gd3['ROA'], 'CASA', 'ROA')
    r_fee, p_fee, desc_fee = test_correlation(gd3['Fee_ratio'], gd3['ROA'], 'Fee', 'ROA')
    print(f"  CASA vs ROA: {desc_casa}")
    print(f"  Fee ratio vs ROA: {desc_fee}")
    supported = (r_casa is not None and r_casa > 0) or (r_fee is not None and r_fee > 0)
    verdict = "✅ ỦNG HỘ" if supported else "⚠️ KHÔNG RÕ RÀNG"
    print(f"  → Kết luận: {verdict}")
    results.append(('H3.1', 'CASA+Fee=sống còn (GĐ3)', verdict, f"CASA-ROA: {desc_casa}; Fee-ROA: {desc_fee}"))
    
    # H3.2 — Kỷ luật vốn & dự phòng
    print("\n--- H3.2: Kỷ luật vốn & dự phòng → bền vững ---")
    eq_thin = (gd3['Equity_ratio'] < 0.06).sum()
    cov_low = (gd3['Coverage'] < 1.0).sum()
    r_eq, p_eq, desc_eq = test_correlation(gd3['Equity_ratio'], gd3['ROA'], 'Equity', 'ROA')
    print(f"  NH vốn mỏng (Equity<6%): {eq_thin}")
    print(f"  NH thiếu dự phòng (Coverage<100%): {cov_low}")
    print(f"  Equity ratio vs ROA: {desc_eq}")
    supported = eq_thin >= 3 and cov_low >= 10
    verdict = "✅ ỦNG HỘ" if supported else "⚠️ KHÔNG RÕ RÀNG"
    print(f"  → Kết luận: {verdict}")
    results.append(('H3.2', 'Kỷ luật vốn & dự phòng (GĐ3)', verdict, f"Vốn mỏng: {eq_thin}, Thiếu DP: {cov_low}"))
    
    # H3.3 — Profit Margin > Leverage
    print("\n--- H3.3: Profit Margin là driver ROE chính ---")
    r_pm, p_pm, _ = test_correlation(gd3['Profit_Margin'], gd3['ROE'], 'PM', 'ROE')
    r_at, p_at, _ = test_correlation(gd3['Asset_Turnover'], gd3['ROE'], 'AT', 'ROE')
    r_lev, p_lev, _ = test_correlation(gd3['Leverage'], gd3['ROE'], 'Lev', 'ROE')
    print(f"  Profit Margin vs ROE: r={r_pm:.3f}, p={p_pm:.4f}" if r_pm else "  PM: N/A")
    print(f"  Asset Turnover vs ROE: r={r_at:.3f}, p={p_at:.4f}" if r_at else "  AT: N/A")
    print(f"  Leverage vs ROE: r={r_lev:.3f}, p={p_lev:.4f}" if r_lev else "  Lev: N/A")
    if r_pm is not None and r_lev is not None:
        supported = abs(r_pm) > abs(r_lev)
        verdict = "✅ ỦNG HỘ" if supported else "❌ BÁC BỎ"
        print(f"  → Kết luận: {verdict} (|r_PM|={abs(r_pm):.3f} {'>' if supported else '<'} |r_Lev|={abs(r_lev):.3f})")
    else:
        verdict = "⚠️ KHÔNG RÕ RÀNG"
        print(f"  → Kết luận: {verdict}")
    results.append(('H3.3', 'Profit Margin > Leverage (GĐ3)', verdict, f"r_PM={r_pm}, r_Lev={r_lev}"))
    
    # ========== SUMMARY ==========
    print("\n" + "="*70)
    print("TỔNG HỢP KẾT QUẢ KIỂM ĐỊNH")
    print("="*70)
    
    out = []
    out.append("# Kết Quả Kiểm Định Giả Thuyết\n")
    out.append("| # | Giả thuyết | Kết luận | Chi tiết |")
    out.append("|---|-----------|---------|---------|")
    
    for code, name, verdict, detail in results:
        print(f"  {code}: {verdict} — {name}")
        out.append(f"| {code} | {name} | {verdict} | {detail} |")
    
    supported_count = sum(1 for _, _, v, _ in results if '✅' in v)
    rejected_count = sum(1 for _, _, v, _ in results if '❌' in v)
    unclear_count = sum(1 for _, _, v, _ in results if '⚠️' in v)
    
    print(f"\n  ✅ Ủng hộ: {supported_count}/{len(results)}")
    print(f"  ❌ Bác bỏ: {rejected_count}/{len(results)}")
    print(f"  ⚠️ Không rõ: {unclear_count}/{len(results)}")
    
    out.append(f"\n**Tổng kết**: ✅ Ủng hộ: {supported_count} | ❌ Bác bỏ: {rejected_count} | ⚠️ Không rõ: {unclear_count}")
    
    with open(r'd:\uni\gcontest\hypothesis_results.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f"\n  → Saved: d:\\uni\\gcontest\\hypothesis_results.md")

if __name__ == '__main__':
    main()

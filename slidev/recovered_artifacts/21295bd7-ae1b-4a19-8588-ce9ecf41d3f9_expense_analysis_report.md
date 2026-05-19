# Vietnamese Banking Sector: Expense Structure and Trends (2015-2024)

> [!NOTE]
> This analysis is conducted to track the operational, financial, and credit risk costs across 27 major Vietnamese commercial banks. Data has been consolidated, aggregated system-wide, and mapped from high-level Income Statement metrics to granular Note disclosures.

---

## 1. Expense Classification Map

Based on [[G'Contest 2026] Đề Vòng 2_4. Mapping.csv](file:///d:/uni/gcontest/%5BG%27Contest%202026%5D%20%C4%90%E1%BB%81%20V%C3%B2ng%202_4.%20Mapping.csv), we extracted all categories that represent outflows, expenses, and losses. These are cross-referenced with their source datasets below:

### High-Level Income Statement Expenses (B-Series)
*Located in [[G'Contest 2026] Đề Vòng 2_2. Income Statement.csv](file:///d:/uni/gcontest/%5BG%27Contest%202026%5D%20%C4%90%E1%BB%81%20V%C3%B2ng%202_2.%20Income%20Statement.csv)*

| Code | Description (Vietnamese) | Account Type | Sign in CSV |
| :--- | :--- | :--- | :--- |
| **B2** | Chi phí lãi và các chi phí tương tự | Interest/Financing Expense | Negative |
| **B5** | Chi phí hoạt động dịch vụ | Fee/Service Expense | Negative |
| **B11** | Chi phí hoạt động khác | Non-Operating/Other Expense | Negative |
| **B15** | Chi phí hoạt động | General & Admin Expense (OPEX) | Negative |
| **B17** | Chi phí dự phòng rủi ro tín dụng | Provision/Credit Risk Cost | Negative |
| **B19** | Chi phí thuế TNDN hiện hành | Current Tax Expense | Negative |
| **B20** | Chi phí thuế TNDN hoãn lại | Deferred Tax Expense | Negative |
| **B21** | Chi phí thuế thu nhập doanh nghiệp | Total Corporate Income Tax | Negative |

### Granular Disclosures (C-Series Breakdown)
*Located in [[G'Contest 2026] Đề Vòng 2_3. Note.csv](file:///d:/uni/gcontest/%5BG%27Contest%202026%5D%20%C4%90%E1%BB%81%20V%C3%B2ng%202_3.%20Note.csv)*

```mermaid
graph TD
    classDef main fill:#2C3E50,stroke:#34495E,stroke-width:2px,color:#fff;
    classDef group fill:#3498DB,stroke:#2980B9,stroke-width:1.5px,color:#fff;
    classDef item fill:#EAFAF1,stroke:#2ECC71,stroke-width:1px,color:#27AE60;

    TotalExpenses["Total Bank Outflows"] ::: main

    TotalExpenses --> InterestExp["Interest Expenses (B2 / C87)"] ::: group
    InterestExp --> C88["C88: Interest on Deposits"] ::: item
    InterestExp --> C89["C89: Interest on Loans"] ::: item
    InterestExp --> C90["C90: Interest on Debt Securities"] ::: item
    InterestExp --> C91["C91: Other Credit Interest"] ::: item

    TotalExpenses --> OpexExp["Operating Expenses (B15 / C140)"] ::: group
    OpexExp --> C141["C141: Taxes, Fees & Levies"] ::: item
    OpexExp --> C142["C142: Staff Expenses"] ::: item
    C142 --> C143["C143: Salary & Allowance"] ::: item
    C142 --> C144["C144: Social Security Contributions"] ::: item
    C142 --> C145["C145: Severance Pay/Benefits"] ::: item
    OpexExp --> C148["C148: Asset-related Expenses"] ::: item
    C148 --> C149["C149: Depreciation of Fixed Assets"] ::: item
    OpexExp --> C151["C151: Administrative/Office Expenses"] ::: item
    OpexExp --> C152["C152: Deposit Insurance Premiums"] ::: item
    OpexExp --> C153["C153: Investment & Bad Debt Provision"] ::: item

    TotalExpenses --> FeeExp["Service & Fee Expenses (B5)"] ::: group
    FeeExp --> ServiceBreakdown["C100 - C106: Payment, Cash, Insurance, Brokerage Costs"] ::: item

    TotalExpenses --> OtherExp["FX, Securities & Trading Losses"] ::: group
    OtherExp --> C112_115["C112-C115: FX Trading & Gold Losses"] ::: item
    OtherExp --> C118_124["C118, C123-C124: Securities Trading Losses"] ::: item
    OtherExp --> C134_139["C134-C139: Swap, Asset Disposal & Other Losses"] ::: item
```

---

## 2. Visualizations and Trend Analysis

To study these expense behaviors over the decade (**2015-2024**), we designed and executed [plot_expenses.py](file:///d:/uni/gcontest/plot_expenses.py), which generated 7 specialized line charts showing system-wide aggregated totals, plus a consolidated Executive Master Dashboard.

All visualizations have been successfully exported to the [pictures](file:///d:/uni/gcontest/pictures) directory in high resolution.

### Interactive Chart Carousel
Toggle through the generated slide deck below to see the specific trend profiles:

````carousel
![1. High-Level Income Statement Trends](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_high_level_is.png)
<!-- slide -->
![2. Interest Expenses Breakdown](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_interest_breakdown.png)
<!-- slide -->
![3. Fee and Service Expenses Breakdown](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_service_breakdown.png)
<!-- slide -->
![4. Operating Expenses (OPEX) Breakdown](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_operating_breakdown.png)
<!-- slide -->
![5. Human Resources & Staff Costs Breakdown](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_staff_breakdown.png)
<!-- slide -->
![6. Asset Management & Depreciation Costs](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_asset_breakdown.png)
<!-- slide -->
![7. FX Trading, Investment Securities & Miscellaneous Losses](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_fx_securities_other_breakdown.png)
<!-- slide -->
![8. Executive Master Combined Dashboard](C:/Users/trucf/.gemini/antigravity/brain/21295bd7-ae1b-4a19-8588-ce9ecf41d3f9/artifacts/expense_master_dashboard.png)
````

---

## 3. Executive Insights & Storytelling

### 1. Interest Cost Volatility and the 2023 Shock
*   **Observation**: **Interest Expense (B2)** represents the single largest cost for commercial banks, overshadowing all operational outlays by a factor of 2.5x to 3x. 
*   **Trend**: System-wide interest expenses spiked from ~195K (2015) to a massive peak of **715,857** in **2023** due to aggressive rate hikes and tight domestic liquidity. In **2024**, it receded to **573,097** as monetary policy eased.
*   **Driver**: Notes analysis confirms that **C88 (Interest Paid on Customer Deposits)** is the overwhelming driver of financing costs, making up over 82% of interest outlays, followed by debt securities issuance (`C90`).

### 2. Operational Rigidity vs Digital Transformation (OPEX)
*   **Observation**: **Operating Expenses (B15 / C140)** exhibit high rigidity, growing linearly every single year from **87,928** (2015) to **249,668** (2024), without showing any downward breaks during crises (like COVID-19 in 2020-2021).
*   **Drivers**:
    *   **Staff Costs (C142)**: Human resources represent the largest piece of OPEX (~55% to 57%). Salaries & allowances (`C143`) expanded rapidly from **28.4K** to **138.3K**, proving that the banking industry remains highly talent-intensive.
    *   **Administrative Expenses (C151)**: Management and office upkeep increased steadily, representing the second-largest core OPEX driver.
    *   **Depreciation (C149)**: Fixed-asset depreciation climbed continuously, reflecting heavy capital expenditures (CapEx) in IT infrastructure and digital transformation networks.

### 3. Credit Provisioning Lag (B17)
*   **Observation**: **Credit Provisioning Expense (B17)** grew rapidly from **47.4K** (2015) to **158.5K** (2024). 
*   **Insight**: Provisioning expenses peaked heavily in **2021 (142.6K)** and **2024 (158.5K)**. The 2021 spike was driven by anticipatory COVID-19 restructuring provisions, while the 2024 expansion reflects a delayed response to real-estate and corporate sector defaults.

---

> [!TIP]
> **Macro Correlation**: Commercial banks with a high ratio of cheap funding (CASA) possess a strong defense mechanism against interest expense shocks (`B2`). Conversely, banks heavily reliant on interbank borrowing (`C89`) faced severe margin compression in the high-rate environment of 2023.

---

### Executable Script Reference
If you need to re-run the pipeline or export these charts with different formatting (e.g., changing colors or DPI), the fully automated pipeline script is located in:
*   [plot_expenses.py](file:///d:/uni/gcontest/plot_expenses.py)
*   Outputs are saved inside [pictures](file:///d:/uni/gcontest/pictures) directory.

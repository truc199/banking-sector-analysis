# Bộ Giả Thuyết Phân Tích Theo Giai Đoạn — G'Contest 2026 Vòng 2

> **Mục tiêu**: Xây dựng các giả thuyết kiểm chứng được bằng dữ liệu (data-driven hypotheses) cho 3 giai đoạn, phục vụ Phần II của bài trình bày. Mỗi giả thuyết gắn với trường dữ liệu cụ thể từ Mapping và kết quả tính toán từ `analyze_group.py`.

---

## Phương pháp luận chung

**K-Means Clustering** trên 6 biến chuẩn hóa (z-score) cho từng giai đoạn:

| Biến | Công thức | Trường dữ liệu | Nhóm phân tích |
|------|-----------|-----------------|----------------|
| ROA | B22 / A1 | B22, A1 | Nhóm 1 |
| NPL | (C35+C36+C37) / A13 | C35, C36, C37, A13 | Nhóm 3 |
| CASA | C68 / A55 | C68, A55 | Nhóm 4 |
| CIR | B15 / B14 | B15, B14 | Nhóm 6 |
| NIM | B3 / Avg(A1) | B3, A1 | Nhóm 2 |
| LDR | A13 / A55 | A13, A55 | Nhóm 7 |

**4 cụm mục tiêu**: 🟢 Ngôi sao / 🔵 Ổn định / 🟡 Chuyển đổi / 🔴 Cần giám sát

---

## GĐ1: COVID-19 & Cú Shock Hệ Thống (2020-2021)

### H1.1 — CASA là lá chắn chống nén NIM trong thời kỳ COVID

> **Giả thuyết**: NH có CASA cao duy trì NIM tốt hơn khi NHNN yêu cầu giãn/giảm lãi suất cho vay (TT01/02), vì chi phí huy động (Cost of Funds) thấp hơn bù đắp được phần yield giảm.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| CASA ratio | C68, A55 | C68 / A55 |
| Cost of Funds | C88, A55 | C88 / A55 |
| NIM | B3, A1 | B3 / Avg(A1) |
| Tương quan CASA vs NIM | — | Pearson r |

**Kết quả insight đã có**: r = -0.418 (CoF vs NIM), CASA phân hóa 33.14pp → **Khả năng cao giả thuyết đúng**.

---

### H1.2 — Đòn bẩy tài chính cao làm khuếch đại tổn thất, không khuếch đại lợi nhuận

> **Giả thuyết**: Trong bối cảnh COVID (chất lượng tài sản suy giảm, phải trích dự phòng), NH có đòn bẩy cao (A1/A64 lớn) sẽ có ROE thấp hơn thay vì cao hơn như lý thuyết dự đoán.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| Leverage | A1, A64 | A1 / A64 |
| ROE | B22, A64 | B22 / A64 |
| Provisioning pressure | B17, B16 | B17 / B16 |

**Kết quả insight đã có**: Nhóm đòn bẩy cao ROE = 6.62% vs nhóm đòn bẩy thấp ROE = 12.12% → **Giả thuyết được xác nhận**.

---

### H1.3 — NH phơi nhiễm ngành nhạy cảm COVID (BĐS, du lịch, vận tải) chịu áp lực nợ xấu sớm hơn

> **Giả thuyết**: NH có tỷ trọng cho vay BĐS (C28), Khách sạn/Nhà hàng (C29), Vận tải (C22-C23) cao sẽ có nợ Nhóm 2 (C34) tích tụ nhanh hơn trong 2020-2021.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| RE Exposure | C28, A13 | C28 / A13 |
| Hospitality Exposure | C29, A13 | C29 / A13 |
| Transport Exposure | C22, A13 | C22 / A13 |
| Nợ cần chú ý | C34, A13 | C34 / A13 |
| NPL ratio | C35+C36+C37, A13 | (C35+C36+C37) / A13 |

**Kết quả insight đã có**: 2 NH có BĐS >20%. Cần kiểm chứng thêm tương quan C28 vs C34 theo năm.

---

### H1.4 — Cơ cấu nợ (TT01/02) che giấu nợ xấu thực sự, NPL chưa phản ánh đúng rủi ro

> **Giả thuyết**: NPL (C35+C36+C37) trong 2020-2021 chưa tăng mạnh do NHNN cho phép cơ cấu nợ, nhưng nợ Nhóm 2 (C34) và VAMC (C64) là chỉ báo sớm đáng tin cậy hơn.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| NPL ratio | C35+C36+C37, A13 | (C35+C36+C37) / A13 |
| Watch-list loan ratio | C34, A13 | C34 / A13 |
| VAMC bonds | C64 | Giá trị tuyệt đối |
| Provisioning expense | B17 | Tăng trưởng YoY |

**Kết quả insight đã có**: 7 NH có nợ Nhóm 2 >1.73%, 9 NH còn VAMC → **Giả thuyết có cơ sở**.

---

## GĐ2: Phục Hồi Hậu Đại Dịch & Bùng Nổ Tín Dụng (2022-2023)

### H2.1 — Áp lực tỷ giá → Thắt chặt tiền tệ → NIM sụp đổ

> **Giả thuyết**: Áp lực DXY tăng buộc NHNN thắt chặt thanh khoản → Cost of Funds vọt lên → NIM bị nén mạnh sau khi đạt đỉnh 2022, đặc biệt ở nhóm NH có CASA thấp.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| NIM | B3, A1 | B3 / Avg(A1) |
| Cost of Funds | C88, A55 | C88 / A55 |
| Yield on loans | C80, A13 | C80 / A13 |
| Spread | — | Yield - CoF |
| Macro: DXY, USDVND | Tỷ giá.csv | USDVND BGN Curncy |

**Kết quả insight đã có**: NIM đỉnh 3.23% (2022), 18/27 NH bị thu hẹp NIM → **Giả thuyết đúng**.

---

### H2.2 — Tín dụng tăng nóng vượt M2 → LDR bùng nổ → Khủng hoảng thanh khoản

> **Giả thuyết**: Tốc độ tăng trưởng cho vay (A13) vượt xa tốc độ tăng trưởng tiền gửi (A55) và M2, đẩy LDR lên trên 100% và buộc NH phải phát hành GTCG (A58) dài hạn để bù đắp.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| LDR | A13, A55 | A13 / A55 |
| Credit growth | A13 | YoY% |
| Deposit growth | A55 | YoY% |
| GTCG ratio | A58, A55 | A58 / A55 |
| Maturity mismatch | C41, C69 | C41 / (C69 + C70) |
| Macro: M2 growth | Monetary.csv | Tăng trưởng M2 YTD |

**Kết quả insight đã có**: LDR vọt 104.87%, 15 NH vượt trần, 20 NH có GTCG/TG >5% → **Giả thuyết đúng**.

---

### H2.3 — Nợ xấu bùng nổ có "độ trễ" — Nợ cơ cấu COVID hết ân hạn

> **Giả thuyết**: Các khoản nợ được cơ cấu theo TT01/02 hết thời hạn ân hạn vào 2022-2023, khiến nợ Nhóm 2 (C34) nhảy nhóm thành nợ xấu (C35+C36+C37), đẩy NPL vọt lên.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| NPL ratio | C35+C36+C37, A13 | (C35+C36+C37) / A13 |
| Watch-list (Nhóm 2) | C34, A13 | C34 / A13 |
| Provisioning expense | B17 | YoY% |
| Coverage ratio | A14, C35+C36+C37 | A14 / (C35+C36+C37) |

**Kết quả insight đã có**: NPL vọt lên 2.87%, 7 NH nợ Nhóm 2 đột biến → **Giả thuyết có cơ sở mạnh**.

---

### H2.4 — Lợi nhuận "phục hồi ảo" — Thu hồi nợ cũ và thu nhập không cốt lõi đóng vai trò lớn

> **Giả thuyết**: Lợi nhuận sau thuế (B22) tăng trở lại, nhưng một phần đáng kể đến từ: (a) thu hồi nợ đã xử lý bằng quỹ dự phòng (C128), (b) thu nhập từ hoạt động khác (B12) — không phải từ hoạt động cốt lõi.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| PPOP / LNTT | B16, B18 | B16 / B18 |
| Non-recurring ratio | B12, B14 | B12 / B14 |
| Bad debt recovery | C128, B14 | C128 / B14 |
| Provisioning / PPOP | B17, B16 | B17 / B16 |
| Core earnings | B16 | Trend |

**Kết quả insight đã có**: 5 NH dự phòng >50% PPOP, 6 NH thu nhập khác >10% TOI, 24 NH thu hồi nợ >1% TOI → **Giả thuyết xác nhận**.

---

## GĐ3: Tái Cân Bằng & Thách Thức Mới (2024)

### H3.1 — CASA và Đa dạng hóa thu nhập là "chìa khóa sống còn" khi NIM bị nén

> **Giả thuyết**: Trong môi trường NIM bị nén kéo dài, NH duy trì profitability bằng 2 con đường: (a) CASA cao → giữ NIM, hoặc (b) Đa dạng hóa thu nhập phi tín dụng (fee income) → bù đắp NIM mất.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| CASA ratio | C68, A55 | C68 / A55 |
| Fee income ratio | B6, B14 | B6 / B14 |
| Non-interest income | B14 - B3, B14 | (B14 - B3) / B14 |
| Bancassurance | C97, B4 | C97 / B4 |
| Digital proxy | C93, B4 | C93 / B4 |
| ROA | B22, A1 | B22 / A1 |

**Kết quả insight đã có**: Fee/TOI tăng từ 4.89% lên 7.99%, 15 NH bancassurance thành công, 13 NH chuyển đổi số mạnh → **Giả thuyết có cơ sở**.

---

### H3.2 — Kỷ luật vốn và dự phòng quyết định sự bền vững dài hạn

> **Giả thuyết**: NH có Equity Ratio (A64/A1) cao VÀ Coverage Ratio (A14/NPL) >100% sẽ duy trì vị trí trong cụm 🟢/🔵 xuyên suốt 3 giai đoạn, trong khi NH vốn mỏng + thiếu dự phòng sẽ tụt về 🟡/🔴.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| Equity ratio | A64, A1 | A64 / A1 |
| Coverage ratio | A14, C35+C36+C37 | A14 / (C35+C36+C37) |
| NPL ratio | C35+C36+C37, A13 | (C35+C36+C37) / A13 |
| RE Exposure | C28, A13 | C28 / A13 |
| Cluster trajectory | K-Means output | GĐ1 → GĐ2 → GĐ3 |

**Kết quả insight đã có**: 4 NH Equity <6%, 18 NH Coverage <100%, 2 NH BĐS >20% → **Giả thuyết cần kiểm chứng bằng trajectory**.

---

### H3.3 — Profit Margin (không phải đòn bẩy) là yếu tố phân hóa ROE mạnh nhất

> **Giả thuyết**: Phân rã DuPont (ROE = Profit Margin × Asset Turnover × Equity Multiplier) cho thấy Profit Margin là biến giải thích ROE tốt nhất, vượt trội so với đòn bẩy tài chính.

| Kiểm chứng | Trường dữ liệu | Công thức |
|-------------|-----------------|-----------|
| Profit Margin | B22, B14 | B22 / B14 |
| Asset Turnover | B14, A1 | B14 / A1 |
| Equity Multiplier | A1, A64 | A1 / A64 |
| ROE | B22, A64 | B22 / A64 |
| Tương quan | — | Pearson r từng factor vs ROE |

**Kết quả insight đã có**: r = -0.904 (Profit Margin vs ROE) — **Giả thuyết xác nhận mạnh**.

---

## Giả thuyết Trajectory (Cross-phase)

### HT.1 — NH bền vững = NH giỏi cả 3 yếu tố: CASA, Profit Margin, Kỷ luật tín dụng

> **Giả thuyết**: NH ở cụm 🟢/🔵 xuyên suốt 3 giai đoạn sẽ đồng thời có: (a) CASA top quartile, (b) Profit Margin top quartile, (c) NPL bottom quartile. Đây là 3 điều kiện cần và đủ.

| Kiểm chứng | Trường dữ liệu | Phương pháp |
|-------------|-----------------|-------------|
| CASA | C68, A55 | Quartile ranking per phase |
| Profit Margin | B22, B14 | Quartile ranking per phase |
| NPL | C35+C36+C37, A13 | Quartile ranking per phase |
| Cluster assignment | K-Means | Phase 1, 2, 3 |
| Trajectory | — | Transition matrix 🟢↔🔵↔🟡↔🔴 |

---

### HT.2 — NH "phục hồi" (🔴/🟡 → 🔵/🟢) có đặc điểm chung: Tăng CASA + Giảm CIR + Xử lý VAMC

> **Giả thuyết**: NH di chuyển từ cụm xấu sang cụm tốt qua 3 giai đoạn sẽ cho thấy cải thiện đồng thời ở: CASA ratio, CIR, và tất toán trái phiếu VAMC (C64 → 0).

| Kiểm chứng | Trường dữ liệu | Phương pháp |
|-------------|-----------------|-------------|
| ΔCASA | C68, A55 | Change GĐ1 → GĐ3 |
| ΔCIR | B15, B14 | Change GĐ1 → GĐ3 |
| VAMC tất toán | C64 | Value GĐ1 vs GĐ3 |
| VAMC income | C131 | Thu từ tất toán TP VAMC |
| Cluster trajectory | K-Means | Transition identification |

---

## Tóm tắt: Ma trận Giả thuyết × Giai đoạn

| # | Giả thuyết | GĐ1 | GĐ2 | GĐ3 | Cross |
|---|------------|------|------|------|-------|
| H1.1 | CASA → NIM shield | ✅ | | | |
| H1.2 | Đòn bẩy cao ≠ ROE cao | ✅ | | | |
| H1.3 | Phơi nhiễm ngành COVID → NPL sớm | ✅ | | | |
| H1.4 | Cơ cấu nợ che giấu NPL | ✅ | | | |
| H2.1 | Tỷ giá → Thắt chặt → NIM sụp | | ✅ | | |
| H2.2 | Credit > M2 → LDR bùng | | ✅ | | |
| H2.3 | Nợ xấu "độ trễ" | | ✅ | | |
| H2.4 | Lợi nhuận phục hồi ảo | | ✅ | | |
| H3.1 | CASA + Fee = chìa khóa sống còn | | | ✅ | |
| H3.2 | Kỷ luật vốn & dự phòng | | | ✅ | |
| H3.3 | Profit Margin > Leverage | | | ✅ | |
| HT.1 | NH bền vững = giỏi cả 3 | | | | ✅ |
| HT.2 | NH phục hồi: CASA↑ + CIR↓ + VAMC→0 | | | | ✅ |

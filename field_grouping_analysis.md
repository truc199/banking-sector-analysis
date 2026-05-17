# Phân Tích Gom Nhóm Trường Dữ Liệu — G'Contest 2026 Vòng 2

## Khung lý thuyết áp dụng
- **CAMELS** (Capital Adequacy, Asset Quality, Management, Earnings, Liquidity, Sensitivity)
- **DuPont Decomposition** (ROE = Profit Margin × Asset Turnover × Equity Multiplier)
- **Revenue Diversification Framework**
- **Funding Structure & Cost of Funds Analysis**
- **Credit Risk & Portfolio Concentration**

> Mỗi nhóm gồm: danh sách trường, lý do gom nhóm, và các insight có thể khai thác.

---

## Nhóm 1: Khả năng sinh lời tổng thể (Profitability – ROA/ROE)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A1 | Tổng tài sản |
| A64 | Vốn chủ sở hữu |
| A66 | Vốn điều lệ |
| A75 | Lợi nhuận chưa phân phối |
| B18 | Tổng lợi nhuận trước thuế |
| B22 | Lợi nhuận sau thuế |
| B14 | Tổng thu nhập hoạt động |
| B15 | Chi phí hoạt động |
| B21 | Chi phí thuế TNDN |

### Lý do gom nhóm
Đây là nhóm cốt lõi để tính **ROA** (B22/A1), **ROE** (B22/A64), **Profit Margin** (B22/B14). Kết hợp DuPont: ROE = (B22/B14) × (B14/A1) × (A1/A64).

### Insight tiềm năng
- **ROA/ROE trend 2020-2024**: Ngân hàng nào phục hồi nhanh nhất sau COVID?
- **DuPont decomposition**: Tăng trưởng ROE do cải thiện biên lợi nhuận, hiệu quả tài sản, hay do đòn bẩy tài chính?
- **Leverage ratio** (A1/A64): Nhóm ngân hàng nào sử dụng đòn bẩy cao — rủi ro hay cơ hội?
- **Retained earnings growth** (A75): Mức tích lũy nội bộ phản ánh sức khỏe tài chính dài hạn.

---

## Nhóm 2: Thu nhập lãi thuần và Biên lãi ròng (NIM – Net Interest Margin)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| B1 | Thu nhập lãi và các khoản thu nhập tương tự |
| B2 | Chi phí lãi và các chi phí tương tự |
| B3 | Thu nhập lãi thuần (NII) |
| A1 | Tổng tài sản |
| A12 | Cho vay khách hàng (net) |
| A13 | Cho vay khách hàng (gross) |
| C79–C86 | Chi tiết thu nhập lãi (cho vay, tiền gửi, chứng khoán, cho thuê TC) |
| C87–C91 | Chi tiết chi phí lãi (tiền gửi, tiền vay, trái phiếu) |

### Lý do gom nhóm
NIM = B3 / Earning Assets. Nhóm này cho phép phân tích **cấu trúc thu nhập lãi** và **cấu trúc chi phí lãi**.

### Insight tiềm năng
- **NIM compression/expansion**: NIM bị thu hẹp hay mở rộng qua các năm?
- **Yield on loans** (C80/A13): So sánh lãi suất cho vay bình quân giữa các NH.
- **Cost of deposits** (C88/A55): Ngân hàng nào có chi phí huy động thấp nhất?
- **Interest income mix**: Tỷ trọng thu lãi từ chứng khoán tăng → thiếu cầu tín dụng?
- **Spread analysis**: Chênh lệch giữa yield và cost — ai có competitive advantage?

---

## Nhóm 3: Chất lượng tài sản và Rủi ro tín dụng (Asset Quality – NPL)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A13 | Cho vay khách hàng (gross) |
| A14 | Dự phòng rủi ro cho vay khách hàng |
| B17 | Chi phí dự phòng rủi ro tín dụng |
| C33 | Nợ đủ tiêu chuẩn |
| C34 | Nợ cần chú ý |
| C35 | Nợ dưới tiêu chuẩn |
| C36 | Nợ nghi ngờ |
| C37 | Nợ có khả năng mất vốn |
| A15–A17 | Hoạt động mua nợ và dự phòng |
| A48 | Dự phòng rủi ro cho tài sản Có nội bảng khác |

### Lý do gom nhóm
Trụ cột **Asset Quality** trong CAMELS. NPL ratio = (C35+C36+C37)/A13. Coverage ratio = A14/(C35+C36+C37).

### Insight tiềm năng
- **NPL ratio trend**: Diễn biến nợ xấu 2020-2024 — đỉnh COVID vs. phục hồi.
- **Loan loss coverage**: Ngân hàng nào có đệm dự phòng dày nhất?
- **Credit cost** (B17/A13): Chi phí tín dụng — ai đang trả giá cho nợ xấu?
- **Migration analysis**: Nợ nhóm 2 (C34) tăng → dấu hiệu cảnh báo sớm.
- **Provisioning pressure vs. earnings**: B17/B16 — dự phòng ăn bao nhiêu % lợi nhuận?

---

## Nhóm 4: Cấu trúc nguồn vốn & Chiến lược CASA (Funding Structure)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A50 | Tổng nợ phải trả |
| A51 | Các khoản nợ chính phủ và NHNN |
| A52 | Tiền gửi và vay các TCTD khác |
| A53 | Tiền gửi của các TCTD khác |
| A54 | Vay các TCTD khác |
| A55 | Tiền gửi của khách hàng |
| A57 | Vốn tài trợ, ủy thác đầu tư |
| A58 | Phát hành giấy tờ có giá |
| C67–C72 | Phân loại tiền gửi theo loại (không kỳ hạn, có kỳ hạn, tiết kiệm, ký quỹ) |
| C73–C78 | Phân loại tiền gửi theo nhóm KH (DNNN, tư nhân, nước ngoài, cá nhân) |

### Lý do gom nhóm
Cấu trúc nguồn vốn quyết định **cost of funds** và **thanh khoản**. CASA ratio = C68 / A55 (tiền gửi không kỳ hạn / tổng tiền gửi KH).

### Insight tiềm năng
- **CASA ratio**: NH nào có CASA cao → lợi thế chi phí vốn rẻ → NIM tốt hơn.
- **Funding mix**: Tỷ trọng tiền gửi KH (A55) vs. vay liên ngân hàng (A54) vs. phát hành GTCG (A58) — ai phụ thuộc vốn rẻ, ai phụ thuộc vốn đắt?
- **Deposit stability**: Tiền gửi cá nhân (C77) vs. doanh nghiệp (C74-C76) — cơ sở KH bền vững?
- **Term structure**: Tỷ lệ tiền gửi không kỳ hạn vs. có kỳ hạn — rủi ro thanh khoản?
- **Wholesale funding dependency**: (A54 + A58) / A50 — mức phụ thuộc vốn thị trường.

---

## Nhóm 5: Đa dạng hóa nguồn thu (Revenue Diversification)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| B3 | Thu nhập lãi thuần |
| B6 | Lãi/lỗ thuần từ hoạt động dịch vụ |
| B4 | Thu nhập từ hoạt động dịch vụ |
| B5 | Chi phí hoạt động dịch vụ |
| B7 | Lãi/lỗ thuần từ kinh doanh ngoại hối và vàng |
| B8 | Lãi/lỗ thuần từ mua bán CK kinh doanh |
| B9 | Lãi/lỗ thuần từ mua bán CK đầu tư |
| B12 | Lãi/lỗ thuần từ hoạt động khác |
| B13 | Thu nhập từ góp vốn, mua cổ phần |
| B14 | Tổng thu nhập hoạt động |
| C92–C106 | Chi tiết thu/chi dịch vụ (thanh toán, bảo lãnh, bảo hiểm, ủy thác, môi giới) |

### Lý do gom nhóm
Đánh giá mức **đa dạng hóa thu nhập** — giảm phụ thuộc vào tín dụng truyền thống. Fee income ratio = B6/B14.

### Insight tiềm năng
- **Non-interest income ratio**: (B14 - B3) / B14 — ai đa dạng nhất?
- **Fee income growth**: B6 tăng trưởng nhanh hơn B3 → chuyển dịch mô hình kinh doanh.
- **Service income breakdown**: Thu từ thanh toán (C93) vs. bảo hiểm (C97) vs. bảo lãnh (C95) — nguồn thu dịch vụ chính?
- **Trading income volatility**: B7, B8, B9 biến động mạnh → rủi ro thu nhập không bền vững.
- **Bancassurance potential**: C97 (thu bảo hiểm) tăng → chiến lược bancassurance thành công?
- **Digital banking proxy**: Thu từ dịch vụ thanh toán (C93) tăng mạnh → dấu hiệu chuyển đổi số.

---

## Nhóm 6: Hiệu quả hoạt động & Quản trị chi phí (CIR – Cost Efficiency)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| B14 | Tổng thu nhập hoạt động |
| B15 | Chi phí hoạt động |
| B16 | LN thuần từ HĐKD trước CP dự phòng RRTD |
| C140–C155 | Chi tiết chi phí hoạt động |
| C141 | Chi nộp thuế, phí, lệ phí |
| C142 | Chi phí cho nhân viên |
| C143 | Chi lương và phụ cấp |
| C144 | Các khoản chi đóng góp theo lương |
| C148 | Chi về tài sản |
| C149 | Chi khấu hao TSCĐ |
| C151 | Chi cho hoạt động quản lý công vụ |
| C152 | Chi nộp phí bảo hiểm, bảo toàn tiền gửi KH |

### Lý do gom nhóm
CIR = B15 / B14 — trụ cột **Management** trong CAMELS. Phân tích cấu trúc chi phí để tìm cơ hội tối ưu.

### Insight tiềm năng
- **CIR trend**: Ngân hàng nào cải thiện CIR tốt nhất qua các năm?
- **Staff cost ratio**: C142/B15 — nhân sự chiếm bao nhiêu % chi phí? Tương quan với quy mô?
- **Compensation per employee proxy**: C143 tương đối → mức lương cạnh tranh?
- **Depreciation intensity**: C149/B15 — đầu tư TSCĐ (công nghệ?) phản ánh qua khấu hao.
- **Operating leverage**: Khi B14 tăng mà B15 tăng chậm hơn → economies of scale.
- **PPOP margin**: B16/B14 — lợi nhuận hoạt động trước dự phòng, đo lường "sức khỏe gốc".

---

## Nhóm 7: Thanh khoản & Cân đối tài sản – nợ (Liquidity – LDR)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A1 | Tổng tài sản |
| A2 | Tiền mặt, vàng bạc, đá quý |
| A3 | Tiền gửi tại NHNN |
| A4 | Tiền gửi tại các TCTD khác và cho vay TCTD khác |
| A5 | Tiền gửi tại các TCTD khác |
| A12 | Cho vay khách hàng (net) |
| A13 | Cho vay khách hàng (gross) |
| A55 | Tiền gửi của khách hàng |
| A18 | Chứng khoán đầu tư |
| C38–C41 | Cho vay phân theo thời gian (ngắn/trung/dài hạn) |
| C68 | Tiền gửi không kỳ hạn |
| C69 | Tiền gửi có kỳ hạn |

### Lý do gom nhóm
Trụ cột **Liquidity** trong CAMELS. LDR = A13/A55. Liquid assets ratio = (A2+A3+A5)/A1.

### Insight tiềm năng
- **LDR trend**: Ngân hàng nào cho vay sát trần huy động? Rủi ro thanh khoản?
- **Liquid assets ratio**: (A2+A3+A5) / A1 — đệm thanh khoản dày hay mỏng?
- **Maturity mismatch**: So sánh cấu trúc kỳ hạn cho vay (C39-C41) với cấu trúc tiền gửi (C68-C69) — gap kỳ hạn?
- **Interbank position**: A5 (tiền gửi tại TCTD) vs. A53 (tiền gửi từ TCTD) — net lender hay net borrower trên liên ngân hàng?
- **Credit-to-deposit gap expansion**: LDR tăng nhanh hơn tăng trưởng tiền gửi → áp lực thanh khoản.

---

## Nhóm 8: Tập trung danh mục tín dụng (Credit Portfolio Concentration)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A13 | Cho vay khách hàng (gross) |
| C4 | Tổng cho vay phân theo ngành |
| C5 | Thương mại |
| C6 | Nông nghiệp và lâm nghiệp |
| C7 | Sản xuất |
| C8–C11 | Chi tiết sản xuất (chế biến, điện khí, nước, khai khoáng) |
| C12 | Xây dựng |
| C13–C21 | Dịch vụ cộng đồng (y tế, giải trí, hành chính...) |
| C22–C24 | Kho bãi, vận tải, viễn thông |
| C25–C27 | Giáo dục, khoa học công nghệ |
| C28 | Bất động sản và tư vấn |
| C29 | Khách sạn và nhà hàng |
| C30 | Dịch vụ tài chính |
| C31 | Các ngành khác |
| C42–C48 | Cho vay phân theo nhóm KH (DNNN, TNHH, nước ngoài, cá nhân...) |

### Lý do gom nhóm
Đo lường **rủi ro tập trung** — một ngân hàng cho vay quá nhiều vào một ngành/nhóm KH sẽ chịu tổn thương lớn khi ngành đó suy thoái.

### Insight tiềm năng
- **Real estate exposure**: C28 / A13 — tỷ trọng BĐS, ngành nhạy cảm nhất thị trường VN.
- **Retail vs. corporate mix**: C47 (cá nhân) vs. (C43+C44+C45+C46) — xu hướng bán lẻ hóa?
- **Industry HHI index**: Tính Herfindahl index từ C5-C31 → mức tập trung ngành.
- **COVID-sensitive sectors**: C29 (khách sạn/nhà hàng), C22 (vận tải) — tác động COVID lên danh mục?
- **SOE lending** (C43): Cho vay DNNN — tỷ trọng giảm/tăng → thay đổi chính sách?
- **Sectoral shift**: Thay đổi cơ cấu ngành qua 5 năm → chiến lược tín dụng của từng NH.

---

## Nhóm 9: Danh mục đầu tư & Rủi ro thị trường (Investment Portfolio & Market Sensitivity)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A8 | Chứng khoán kinh doanh |
| A9 | Chứng khoán kinh doanh (gross) |
| A10 | Dự phòng giảm giá CK kinh doanh |
| A11 | Công cụ tài chính phái sinh và TSTC khác |
| A18 | Chứng khoán đầu tư |
| A19 | CK đầu tư sẵn sàng để bán |
| A20 | CK đầu tư giữ đến ngày đáo hạn |
| A21 | Dự phòng giảm giá CK đầu tư |
| C1–C3 | Chi tiết CK kinh doanh (nợ vs. vốn) |
| C49–C66 | Chi tiết CK đầu tư (TPCP, TPDN, VAMC, dự phòng) |
| B7 | Lãi/lỗ thuần từ ngoại hối và vàng |
| B8 | Lãi/lỗ thuần từ mua bán CK kinh doanh |
| B9 | Lãi/lỗ thuần từ mua bán CK đầu tư |
| C107–C115 | Chi tiết thu/chi kinh doanh ngoại hối |
| C116–C126 | Chi tiết thu/chi mua bán CK |

### Lý do gom nhóm
Trụ cột **Sensitivity to Market Risk** trong CAMELS. Đánh giá mức độ phơi nhiễm trước biến động lãi suất, tỷ giá, giá chứng khoán.

### Insight tiềm năng
- **Government bond reliance**: (C52+C60) / A18 — tỷ trọng TPCP → mức an toàn nhưng yield thấp.
- **Corporate bond exposure**: (C55+C63) / A18 — rủi ro TPDN, nhạy cảm thị trường VN.
- **VAMC bond** (C64): Trái phiếu đặc biệt VAMC → nợ xấu ẩn chưa xử lý.
- **Trading vs. HTM strategy**: A19 vs. A20 — chiến lược đầu tư ngắn hạn hay dài hạn?
- **FX trading profitability**: B7 & C107-C115 — lãi/lỗ ngoại hối → rủi ro tỷ giá.
- **Derivative usage** (A11): Ngân hàng nào sử dụng phái sinh → quản trị rủi ro tinh vi?
- **Unrealized gains/losses**: Dự phòng CK (A10, A21) vs. giá trị gốc → tổn thất tiềm ẩn.

---

## Nhóm 10: An toàn vốn & Cấu trúc vốn chủ sở hữu (Capital Adequacy)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A49 | Nợ phải trả và vốn chủ sở hữu |
| A64 | Vốn chủ sở hữu |
| A65 | Vốn của TCTD |
| A66 | Vốn điều lệ |
| A67 | Vốn đầu tư XDCB |
| A68 | Thặng dư vốn cổ phần |
| A69 | Cổ phiếu quỹ |
| A70 | Cổ phiếu ưu đãi |
| A71 | Vốn khác |
| A72 | Quỹ của TCTD |
| A73 | Chênh lệch tỷ giá hối đoái |
| A74 | Chênh lệch đánh giá lại tài sản |
| A75 | Lợi nhuận chưa phân phối |
| A76 | Lợi ích cổ đông thiểu số |
| A1 | Tổng tài sản |

### Lý do gom nhóm
Trụ cột **Capital Adequacy** trong CAMELS. Equity/Assets = A64/A1. Phân tích cấu trúc nội bộ vốn CSH.

### Insight tiềm năng
- **Equity ratio** (A64/A1): Đệm vốn — ai mỏng nhất, rủi ro nhất?
- **Chartered capital growth** (A66): Tốc độ tăng vốn điều lệ → khả năng huy động vốn CSH.
- **Share premium** (A68): Thặng dư vốn cổ phần lớn → phát hành thành công, thị trường tin tưởng.
- **Treasury shares** (A69): Mua lại cổ phiếu quỹ → dấu hiệu gì? Thừa vốn hay hỗ trợ giá?
- **Retained earnings ratio**: A75 / A64 — mức tích lũy nội bộ.
- **Minority interest** (A76): Lợi ích CĐTS lớn → cấu trúc tập đoàn phức tạp.
- **FX revaluation** (A73): Biến động tỷ giá ảnh hưởng trực tiếp đến vốn CSH.

---

## Nhóm 11: Cấu trúc kỳ hạn tín dụng & Quản trị tài sản – nợ (ALM)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| C38 | Tổng cho vay phân theo thời gian |
| C39 | Cho vay ngắn hạn |
| C40 | Cho vay trung hạn |
| C41 | Cho vay dài hạn |
| C68 | Tiền gửi không kỳ hạn |
| C69 | Tiền gửi có kỳ hạn |
| C70 | Tiền gửi tiết kiệm |
| A55 | Tiền gửi của khách hàng |
| A58 | Phát hành giấy tờ có giá |
| B1 | Thu nhập lãi |
| B2 | Chi phí lãi |

### Lý do gom nhóm
Quản trị **Asset-Liability Management** — cân đối kỳ hạn giữa tài sản sinh lời và nghĩa vụ nợ. Mismatch kỳ hạn = rủi ro lãi suất.

### Insight tiềm năng
- **Long-term loan ratio**: C41 / (C39+C40+C41) — tỷ trọng dài hạn tăng → rủi ro lãi suất cao hơn.
- **Maturity gap**: (C41 - tiền gửi dài hạn proxy) → mức chênh lệch kỳ hạn.
- **Short-term funding for long-term assets**: C68 (không kỳ hạn) lớn nhưng C41 (cho vay dài hạn) cũng lớn → rủi ro ALM.
- **Interest rate sensitivity**: Khi lãi suất thay đổi, NIM sẽ bị ảnh hưởng thế nào dựa trên cấu trúc kỳ hạn?
- **Bond issuance trend** (A58): Phát hành GTCG tăng → kéo dài kỳ hạn nợ, cải thiện ALM.

---

## Nhóm 12: Đầu tư dài hạn & Hoạt động công ty con/liên kết (Strategic Investments)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| A22 | Góp vốn, đầu tư dài hạn |
| A23 | Đầu tư vào công ty con |
| A24 | Đầu tư vào công ty liên doanh |
| A25 | Vốn góp liên doanh |
| A26 | Đầu tư vào công ty liên kết |
| A27 | Đầu tư dài hạn khác |
| A28 | Dự phòng giảm giá đầu tư dài hạn |
| B13 | Thu nhập từ góp vốn, mua cổ phần |
| A29 | Tài sản cố định |
| A30–A38 | Chi tiết TSCĐ (hữu hình, thuê tài chính, vô hình) |
| A39–A41 | Bất động sản đầu tư |
| A47 | Lợi thế thương mại (goodwill) |

### Lý do gom nhóm
Đánh giá **chiến lược mở rộng hệ sinh thái** của ngân hàng — đầu tư vào công ty con (bảo hiểm, chứng khoán, fintech), bất động sản, và tài sản vô hình.

### Insight tiềm năng
- **Subsidiary investment ratio**: A23/A1 — mức đầu tư vào công ty con → chiến lược tập đoàn?
- **Investment income yield**: B13/A22 — hiệu quả đầu tư dài hạn.
- **Goodwill** (A47): Lợi thế thương mại → M&A đã thực hiện, rủi ro suy giảm giá trị.
- **Fixed asset intensity**: A29/A1 — đầu tư cơ sở hạ tầng, chi nhánh.
- **Intangible assets** (A36): TSCĐ vô hình → phần mềm, bản quyền, đầu tư công nghệ?
- **Provisioning for investments** (A28): Dự phòng giảm giá → chất lượng khoản đầu tư?
- **Investment real estate** (A39): NH nào nắm BĐS đầu tư — tài sản hay rủi ro?

---

## Nhóm 13: Chất lượng lợi nhuận & Thuế (Earnings Quality & Tax)

### Trường dữ liệu
| Mã | Mô tả |
|-----|--------|
| B16 | LN thuần từ HĐKD trước CP dự phòng RRTD |
| B17 | Chi phí dự phòng rủi ro tín dụng |
| B18 | Tổng lợi nhuận trước thuế |
| B19 | Chi phí thuế TNDN hiện hành |
| B20 | Chi phí thuế TNDN hoãn lại |
| B21 | Chi phí thuế TNDN |
| B22 | Lợi nhuận sau thuế |
| B23 | Lợi ích cổ đông thiểu số |
| B24 | Lợi nhuận cổ đông công ty mẹ |
| B12 | Lãi/lỗ thuần từ hoạt động khác |
| B10 | Thu nhập từ hoạt động khác |
| B11 | Chi phí hoạt động khác |
| C127–C139 | Chi tiết thu nhập/chi phí hoạt động khác |
| A45 | Tài sản thuế TNDN hoãn lại |
| A61 | Thuế TNDN hoãn lại phải trả |

### Lý do gom nhóm
Đánh giá **chất lượng bền vững** của lợi nhuận. Thu nhập "khác" (B12) không ổn định. Thuế hoãn lại có thể cho thấy chênh lệch kế toán – thuế.

### Insight tiềm năng
- **Core earnings ratio**: B16/B18 — bao nhiêu % LNTT đến từ hoạt động cốt lõi?
- **Provisioning impact**: B17/B16 — dự phòng ăn mòn bao nhiêu % PPOP?
- **Non-recurring income**: B12/B14 — thu nhập khác chiếm tỷ trọng lớn → LN không bền vững.
- **VAMC income** (C131): Thu từ tất toán TP VAMC → thu nhập một lần, không lặp lại.
- **Effective tax rate**: B21/B18 — thuế suất thực tế vs. thuế suất danh nghĩa (20%).
- **Deferred tax position**: A45 vs. A61 — net deferred tax asset hay liability?
- **Minority interest drag**: B23/B22 — bao nhiêu % LN chia cho CĐTS?
- **Bad debt recovery** (C128): Thu hồi nợ đã xử lý → chất lượng quản trị nợ xấu.

---

## Ma trận tham chiếu chéo giữa các nhóm

| Nhóm | Liên kết với nhóm | Mối quan hệ |
|------|-------------------|-------------|
| 1 (Profitability) | 2, 5, 6 | ROA/ROE = f(NIM, Revenue Mix, CIR) |
| 2 (NIM) | 4, 7 | NIM phụ thuộc cost of funds (CASA) và LDR |
| 3 (Asset Quality) | 8, 13 | NPL tập trung ở ngành nào? Ảnh hưởng lên earnings quality |
| 4 (Funding/CASA) | 2, 7 | CASA → cost of funds → NIM; cấu trúc TG → thanh khoản |
| 5 (Diversification) | 1, 6 | Fee income cải thiện TOI → giảm CIR tương đối |
| 6 (CIR) | 1, 5 | Chi phí kiểm soát tốt → profit margin cao |
| 7 (Liquidity) | 4, 11 | LDR + maturity mismatch → rủi ro thanh khoản |
| 8 (Concentration) | 3, 9 | Tập trung ngành → NPL ngành đó; tương quan portfolio đầu tư |
| 9 (Investment) | 7, 3 | CK đầu tư là buffer thanh khoản; VAMC → nợ xấu ẩn |
| 10 (Capital) | 1, 3 | Đòn bẩy ảnh hưởng ROE; vốn đệm hấp thụ tổn thất nợ xấu |
| 11 (ALM) | 7, 2 | Kỳ hạn mismatch → rủi ro lãi suất → NIM volatility |
| 12 (Strategic Inv.) | 10, 1 | Đầu tư con/liên kết dùng vốn CSH; đóng góp vào lợi nhuận |
| 13 (Earnings Quality) | 1, 3 | LN bền vững vs. một lần; dự phòng ảnh hưởng bottom line |

---

## Gợi ý phân tích nâng cao (Cross-group)

1. **CAMELS Composite Score**: Tính điểm tổng hợp từ nhóm 1, 3, 6, 7, 9, 10 → xếp hạng sức khỏe tổng thể.
2. **Profitability Decomposition Tree**: Nhóm 1 + 2 + 5 + 6 → phân rã lợi nhuận theo cây nhân tố.
3. **Risk-Return Matrix**: Nhóm 1 (ROA/ROE) vs. Nhóm 3 (NPL) → scatter plot rủi ro – lợi nhuận.
4. **Funding Cost Advantage**: Nhóm 4 (CASA) → Nhóm 2 (NIM) → Nhóm 1 (ROA) — chuỗi nhân quả.
5. **COVID Impact & Recovery**: Nhóm 8 (sector exposure) + Nhóm 3 (NPL) + Nhóm 13 (provisioning) → câu chuyện COVID.
6. **Digital Transformation Proxy**: Nhóm 5 (thu thanh toán) + Nhóm 6 (CIR giảm) + Nhóm 12 (TSCĐ vô hình) → ai chuyển đổi số mạnh nhất?
7. **K-Means Clustering**: Dùng các chỉ số từ nhiều nhóm (ROA, NPL, CASA, CIR, NIM, LDR) để phân cụm ngân hàng.


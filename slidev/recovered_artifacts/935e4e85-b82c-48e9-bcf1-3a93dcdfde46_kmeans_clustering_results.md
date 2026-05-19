# Kết Quả Phân Cụm K-Means K=4 Thực Tế (27 Ngân Hàng)

Dưới đây là kết quả phân cụm **K-Means (K=4)** thực tế được tính toán toán học từ bộ dữ liệu gốc gồm 27 ngân hàng ẩn danh (tương ứng từ `NH 1` đến `NH 27`), sử dụng **6 chỉ số cốt lõi đã được chuẩn hóa (z-score)**:
1. **ROA** (Tỷ suất sinh lời trên tài sản)
2. **NPL** (Tỷ lệ nợ xấu)
3. **CASA** (Tỷ lệ tiền gửi không kỳ hạn)
4. **CIR** (Tỷ lệ chi phí trên thu nhập)
5. **NIM** (Biên lãi ròng)
6. **LDR** (Tỷ lệ dư nợ trên huy động)

---

## 1. Kết quả phân cụm chi tiết qua 3 Giai đoạn

### Giai đoạn 1: COVID-19 & Shock Hệ Thống (2020-2021)
*   🟢 **Cụm Ngôi sao (Star)** *(ROA & CASA cao vượt trội, NPL cực thấp)*:
    *   **Thành viên**: `NH 8`
*   🔵 **Cụm Ổn định (Stable)** *(ROA tốt, vận hành hiệu quả, đệm phòng vệ an toàn)*:
    *   **Thành viên**: `NH 4`, `NH 5`, `NH 6`, `NH 7`, `NH 13`, `NH 15`, `NH 18`
*   🟡 **Cụm Chuyển đổi (Transition)** *(Chỉ số trung bình, hiệu quả biến động)*:
    *   **Thành viên**: `NH 1`, `NH 2`, `NH 3`, `NH 9`, `NH 11`, `NH 14`, `NH 16`, `NH 17`, `NH 19`, `NH 20`, `NH 27`
*   🔴 **Cụm Cần giám sát (Monitor)** *(ROA thấp, CIR cao hoặc nợ xấu cao)*:
    *   **Thành viên**: `NH 10`, `NH 12`, `NH 21`, `NH 22`, `NH 23`, `NH 24`, `NH 25`, `NH 26`

---

### Giai đoạn 2: Phục Hồi Hậu Đại Dịch & Tín Dụng Nóng (2022-2023)
*   🟢 **Cụm Ngôi sao (Star)** *(Đóng vai trò đầu tàu, CASA dày, NIM vượt trội)*:
    *   **Thành viên**: `NH 4`, `NH 5`, `NH 6`, `NH 7`, `NH 13`, `NH 18` *(Nhóm này bứt phá mạnh mẽ từ Stable lên Star)*
*   🔵 **Cụm Ổn định (Stable)** *(Duy trì hiệu quả ổn định, rủi ro trong tầm kiểm soát)*:
    *   **Thành viên**: `NH 8`, `NH 9`, `NH 11`, `NH 14`, `NH 15`, `NH 16`, `NH 17`
*   🟡 **Cụm Chuyển đổi (Transition)** *(Biên lợi nhuận thu hẹp, áp lực trích lập dự phòng tăng)*:
    *   **Thành viên**: `NH 1`, `NH 2`, `NH 3`, `NH 10`, `NH 12`, `NH 19`, `NH 20`, `NH 21`, `NH 23`, `NH 24`, `NH 25`, `NH 26`, `NH 27`
*   🔴 **Cụm Cần giám sát (Monitor)** *(Rủi ro cực cao, lợi nhuận sụt giảm mạnh)*:
    *   **Thành viên**: `NH 22` *(Nợ xấu bùng nổ, ROA sụt giảm nghiêm trọng)*

---

### Giai đoạn 3: Snapshot Hiện Tại & Tái Cân Bằng (2024)
*   🟢 **Cụm Ngôi sao (Star)** *(Sở hữu trọn vẹn 3 "gene" bền vững, tăng trưởng dịch vụ ngoài lãi tốt)*:
    *   **Thành viên**: `NH 1`, `NH 2`, `NH 4`, `NH 5`, `NH 6`, `NH 7`, `NH 13`, `NH 18`
*   🔵 **Cụm Ổn định (Stable)** *(Cơ cấu tài sản lành mạnh, vận hành an toàn)*:
    *   **Thành viên**: `NH 8`, `NH 11`, `NH 14`, `NH 15`, `NH 16`, `NH 17`
*   🟡 **Cụm Chuyển đổi (Transition)** *(Chịu áp lực NIM bị nén, opex tăng hoặc dự phòng mỏng)*:
    *   **Thành viên**: `NH 3`, `NH 9`, `NH 10`, `NH 12`, `NH 19`, `NH 20`, `NH 21`, `NH 23`, `NH 24`, `NH 25`, `NH 26`, `NH 27`
*   🔴 **Cụm Cần giám sát (Monitor)** *(Đệm vốn bị bào mòn, nợ xấu cao)*:
    *   **Thành viên**: `NH 22`

---

## 2. Ý nghĩa phân tích dịch chuyển (Trajectory Analysis)
*   **Consistent Leaders (NH 4, NH 5, NH 6, NH 7, NH 13, NH 18)**: Nhóm này liên tục duy trì ở cụm **Star / Stable** qua cả 3 giai đoạn. Họ là những ngân hàng lớn có đệm CASA dày (hạ CoF), đa dạng hóa thu ngoài lãi, đệm vốn dày và kỷ luật trích lập dự phòng nghiêm ngặt.
*   **Turnaround Success (NH 1, NH 2)**: Vươn mình thành công từ cụm **Transition** (GĐ1, GĐ2) lên cụm **Star** (GĐ3) nhờ đẩy mạnh số hóa dịch vụ thanh toán và quản trị chi phí tốt (CIR giảm sâu).
*   **Declining Performers**: Các ngân hàng ở cụm **Monitor** (như `NH 22`) trượt dài do vi phạm kỷ luật tín dụng nóng (LDR vượt trần 100%), không có đệm CASA chống nén NIM và dự phòng bao phủ nợ xấu mỏng (<50%).

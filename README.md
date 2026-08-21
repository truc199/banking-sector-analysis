# G'Contest 2026 — Vòng 2 | Đội Vualidon.FP

Ứng dụng Data Analytics đánh giá hiệu quả hoạt động và tiềm năng tăng trưởng
ngành Ngân hàng Việt Nam giai đoạn **2020–2024**.

Sản phẩm cuối là bộ **36 slide** dựng bằng [Slidev](https://sli.dev/), toàn bộ
biểu đồ sinh bằng matplotlib từ dữ liệu gốc và tái lập được bằng một lệnh.

## Dữ liệu

27 ngân hàng ẩn danh (`NH 1`–`NH 27`), 10 năm (2015–2024), phân tích tập trung 2020–2024.

| Nguồn | Trường | Nội dung |
|---|---|---|
| Balance Sheet | `A1`–`A76` | Bảng cân đối kế toán |
| Income Statement | `B1`–`B24` | Kết quả kinh doanh |
| Note | `C1`–`C98` | Thuyết minh BCTC (phân loại nợ, cơ cấu tiền gửi, chi tiết thu/chi lãi) |
| Mapping | — | Từ điển mã trường → mô tả |
| Macro | — | GDP, FDI, Monetary (M2/tín dụng), PMI, tỷ giá, tổng mức bán lẻ |

Không phải ngân hàng nào cũng có đủ Thuyết minh BCTC.

## Luận điểm chính — "Sự tiến hóa của biến chi phối"

| Giai đoạn | Stress test vĩ mô | Biến chi phối #1 | Bằng chứng |
|---|---|---|---|
| **GĐ1** 2020–21 | COVID-19, TT01/02 ép giảm yield | Cấu trúc vốn (CASA → CoF) | CASA ↔ CoF `r = −0.864` |
| **GĐ2** 2022–23 | Thắt chặt tiền tệ, LDR tăng nóng, hết ân hạn nợ | CoF tăng vọt + nợ xấu phát nổ | NPL ↔ ROA `r = −0.460` |
| **GĐ3** 2024 | Nợ xấu tích tụ cực đại | Quản trị rủi ro nợ xấu | NPL ↔ ROA `r = −0.894` |

Kiểm định 11 giả thuyết: **10 ủng hộ, 1 không có ý nghĩa thống kê, 0 bác bỏ**.

Ba "gene" bền vững rút ra: CASA dày (điều kiện cần) · kỷ luật đệm vốn và dự phòng
(điều kiện đủ) · đa dạng nguồn thu Fee/TOI (lá chắn dự phòng).

## Cấu trúc

```
data/          13 file dữ liệu gốc (BCTC + macro)
docs/          tài liệu phân tích: storytelling flow, cây nhân quả,
               giả thuyết & kết quả kiểm định, 13 nhóm insight
analysis/      script tái lập kết quả phân tích
slidev/        bộ slide (slides.md) + 26 script sinh biểu đồ
appendix/      phân tích mở rộng không đưa vào slide (script + hình)
```

Mọi script dùng đường dẫn tương đối theo vị trí file, chạy được từ thư mục bất kỳ.

---

# Cài đặt

**Yêu cầu**: Python ≥ 3.14 ([uv](https://docs.astral.sh/uv/)) và Node.js ≥ 20.

```bash
uv sync                        # cài dependency Python (pandas, matplotlib, sklearn, seaborn, adjustText)
cd slidev && npm install       # cài dependency Slidev
```

# Xem slide

```bash
cd slidev
npm run dev
```

Lệnh này khởi động dev server và **tự mở trình duyệt**. Bốn chế độ xem:

| Chế độ | Địa chỉ | Dùng khi nào |
|---|---|---|
| Trình chiếu | http://localhost:3030/ | Xem/thuyết trình bình thường |
| Presenter | http://localhost:3030/presenter/ | Có ghi chú + đồng hồ, mở ở màn hình thứ 2 |
| Overview | http://localhost:3030/overview/ | Xem lưới toàn bộ 36 slide, click để nhảy |
| Export | http://localhost:3030/export/ | Xuất PDF/PNG |

**Phím tắt**: `←` `→` chuyển slide · `o` overview · `f` toàn màn hình · `d` dark mode ·
`g` nhảy tới số slide · `?` xem toàn bộ phím tắt.

Dev server có **hot reload**: sửa `slides.md` hoặc chạy lại script sinh biểu đồ thì
trang tự cập nhật ngay, không cần khởi động lại. Dừng server bằng `Ctrl+C`.

## Build & Deploy

```bash
cd slidev
npm run build                       # build tĩnh vào slidev/dist/
npx vite preview --outDir dist      # xem thử bản build
```

Deploy tự động qua Vercel ([vercel.json](slidev/vercel.json)) hoặc Netlify
([netlify.toml](slidev/netlify.toml)) — cả hai đều chạy `npm run build` và publish `dist/`.

Slidev mặc định đọc `slidev/slides.md`, nên **không được đổi tên file này**, nếu không
build trên CI sẽ ra sai bộ slide.

## Xuất PDF

Dùng trang `/export/` ở trên, hoặc chạy lệnh (cần cài thêm `playwright-chromium`):

```bash
cd slidev && npm run export
```

---

# Sinh lại biểu đồ

Sinh lại toàn bộ 26 biểu đồ từ dữ liệu gốc. Script tự đối chiếu kết quả với `slides.md`
và báo ngay nếu thiếu hoặc thừa ảnh:

```bash
python slidev/regenerate_all_charts.py
```

Sinh lại một biểu đồ duy nhất:

```bash
python slidev/gen_new_ch2_s2.py
```

# Tái lập kết quả phân tích

Ghi đè các file trong `docs/`:

```bash
python analysis/analyze_group.py      # 13 nhóm insight  → docs/insight/
python analysis/test_hypotheses.py    # 11 giả thuyết    → docs/hypothesis_results.md
python analysis/macro_analysis.py     # tổng hợp macro   → docs/macro_analysis.txt
```

---

# Tạo slide mới

Quy trình 4 bước. Ánh xạ **1 slide ↔ 1 ảnh ↔ 1 script** được giữ nghiêm ngặt để
`regenerate_all_charts.py` luôn kiểm tra được tính toàn vẹn.

## Bước 1 — Tính số liệu từ dữ liệu gốc

Tra mã trường cần dùng trong [data/Mapping.csv](data/), rồi tính từ CSV tương ứng.
Các chỉ số đã dùng trong bài:

| Chỉ số | Công thức | Trường |
|---|---|---|
| ROA | `B22 / A1` | Income + Balance |
| ROE | `B22 / A64` | Income + Balance |
| NIM | `B3 / Avg(A1)` | Income + Balance |
| NPL | `(C35+C36+C37) / A13` | Note |
| CASA | `C68 / A55` | Note + Balance |
| CIR | `B15 / B14` | Income |
| LDR | `A13 / A55` | Balance |
| Cost of Funds | `C88 / A55` | Note + Balance |
| Coverage | `A14 / (C35+C36+C37)` | Balance + Note |
| Equity Ratio | `A64 / A1` | Balance |

Không tự bịa số: mọi con số lên slide phải tính ra được từ `data/`.

## Bước 2 — Viết script sinh biểu đồ

Tạo file `slidev/gen_new_ch{chương}_s{slide}.py`. Ví dụ slide 10.1 → `gen_new_ch10_s1.py`.
Dùng template dưới đây (sao chép nguyên khối header, đây là chuẩn chung của cả 26 script):

```python
"""
Generate Chart for NEW Slide X.Y: <mô tả>
Saves to slidev/public/new_slide_X_Y_<tên>.png
"""
import os, glob
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# --- Đường dẫn tương đối theo vị trí file (không phụ thuộc máy) ---
import sys as _sys
_sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PUBLIC = ROOT / "slidev" / "public"
FONTS = ROOT / "slidev" / "fonts"
# ------------------------------------------------------------------

# ─── Setup ───────────────────────────────────────────────────────────────
for font_file in glob.glob(str(FONTS / "*.ttf")):
    try:
        fm.fontManager.addfont(font_file)
    except Exception:
        pass

plt.rcParams['font.family'] = 'Roboto'
plt.rcParams['font.sans-serif'] = ['Roboto', 'Segoe UI', 'Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['text.color'] = '#1e293b'
plt.rcParams['axes.labelcolor'] = '#334155'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

# ─── Color Palette ───────────────────────────────────────────────────────
NAVY_DARK  = '#003366'; NAVY_MID_D = '#004C99'; NAVY_MID = '#0066CC'
AZURE      = '#007FFF'; DODGER     = '#3399FF'
FRENCH_SKY = '#66B2FF'; BABY_BLUE  = '#99CCFF'
SECONDARY_ORANGE = '#E67300'
GRID_COLOR = '#f1f5f9'; SPINE_COLOR = '#cbd5e1'
TEXT_DARK  = '#0f172a'; TEXT_MID    = '#1e293b'

# ─── Font Sizes ──────────────────────────────────────────────────────────
FS_TITLE = 13; FS_LABEL = 11; FS_TICK = 10.5; FS_VAL = 9.5; FS_LEG = 10

# ─── Đọc dữ liệu ─────────────────────────────────────────────────────────
bs = pd.read_csv(glob.glob(str(DATA / "*Balance*"))[0])
# inc  = pd.read_csv(glob.glob(str(DATA / "*Income*"))[0])
# note = pd.read_csv(glob.glob(str(DATA / "*Note*"))[0])

# ─── Vẽ ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=350)

# ... vẽ ở đây ...

ax.set_title('<Tiêu đề biểu đồ>', fontsize=FS_TITLE, fontweight='bold',
             pad=12, color=TEXT_DARK)
ax.set_ylabel('<Tên trục Y> (%)', fontsize=FS_LABEL, fontweight='bold',
              labelpad=6, color=TEXT_MID)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f%%'))

# Grid & Spines
ax.grid(True, axis='y', linestyle='--', color=GRID_COLOR, zorder=0)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(SPINE_COLOR)
ax.spines['bottom'].set_color(SPINE_COLOR)

# Legend LUÔN đặt dưới biểu đồ
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
          ncol=2, frameon=False, fontsize=FS_LEG)

plt.tight_layout()
plt.savefig(os.path.join(str(PUBLIC), 'new_slide_X_Y_<tên>.png'),
            dpi=350, bbox_inches='tight', pad_inches=0.03, transparent=True)
plt.close()
print('DONE')
```

Chạy thử: `python slidev/gen_new_chX_sY.py` → kiểm tra ảnh trong `slidev/public/`.

## Bước 3 — Thêm slide vào `slides.md`

Mỗi slide ngăn cách bằng `---`. **Mọi slide đều dùng layout `ImpressiveHeader`**
(trừ slide bìa dùng `ImpressiveCover`). Bố cục 2 cột chuẩn: chữ bên trái, biểu đồ bên phải.

```html
---
transition: slide-left
---

<!-- SLIDE X.Y: <mô tả ngắn> -->
<ImpressiveHeader>
<template #title>Tiêu đề chương</template>
<template #subtitle>Mô tả phạm vi phân tích của slide (2020 – 2024)</template>

<div class="grid grid-cols-12 gap-x-6 text-slate-700">
  <!-- CỘT TRÁI: nội dung phân tích -->
  <div class="col-span-6 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2.5 mb-2 text-justify text-[11px] leading-[1.3] text-slate-600 font-medium">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11.5px]">Luận điểm thứ nhất:</strong><br />
        Diễn giải, số liệu quan trọng bôi đậm kèm màu khớp với legend trong biểu đồ:
        <span class="font-bold text-[#003366]">19.31 triệu tỷ VND</span> (2024).
      </p>
      <p>
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11.5px]">Luận điểm thứ hai:</strong><br />
        Nội dung...
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI: biểu đồ -->
  <div class="col-span-6 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_X_Y_<tên>.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần N: Tên phần | Slide X.Y – Tiêu đề slide</template>
</ImpressiveHeader>
```

Tỷ lệ cột thường dùng: `col-span-6 / col-span-6` (cân bằng), `col-span-7 / col-span-5`
(nhiều chữ), `col-span-8 / col-span-4` (rất nhiều chữ). Chiều cao cột `h-[390px]`
đến `h-[460px]` tùy lượng nội dung.

Ký tự đặc biệt trong HTML phải escape: `&` viết thành `&amp;`, `<` thành `&lt;`.

## Bước 4 — Kiểm tra

```bash
python slidev/regenerate_all_charts.py    # xác nhận ảnh khớp với slides.md
cd slidev && npm run build                # xác nhận build không lỗi
```

`regenerate_all_charts.py` sẽ báo `THIẾU` nếu slide tham chiếu ảnh chưa tồn tại, và
`THỪA` nếu có ảnh không slide nào dùng — dọn ảnh thừa để `public/` không phình ra.

---

# Quy ước trình bày

## Biểu đồ

- **Dải màu chủ đạo navy**: `#003366` → `#004C99` → `#0066CC` → `#007FFF` → `#3399FF`
  → `#66B2FF` → `#99CCFF`. Màu phụ để highlight: đỏ gạch, cam đất (`#E67300`), xanh ngọc.
- Biểu đồ kết hợp **bar + line** phải chọn cặp màu tương phản cao, **bar đậm hơn line**.
- Toàn bộ vẽ bằng **matplotlib**, font **Roboto** (`slidev/fonts/`), **dpi 350**,
  nền trong suốt (`transparent=True`).
- Trục tọa độ rõ ràng có chia vạch, có tiêu đề trục, tiêu đề biểu đồ.
- **Legend luôn đặt dưới biểu đồ**, `frameon=False`.
- Đường xu hướng dùng `PchipInterpolator` (dotted line) để làm mượt.
- Cỡ chữ trong biểu đồ phải tương đương cỡ chữ trên slide — tăng `figsize` nếu chữ đè nhau.

## Slide

- Văn phong báo cáo tài chính chuyên nghiệp, không ví von, không dùng ngoặc kép tùy tiện.
- Số liệu quan trọng bôi đậm với **màu khớp legend** trong biểu đồ tương ứng.
- Hạn chế khoảng trắng thừa; mỗi slide tập trung một luận điểm.
- Footer ghi rõ `Phần N: Tên phần | Slide X.Y – Tiêu đề`.

Chi tiết đầy đủ: [.agents/workflows/create-slide.md](.agents/workflows/create-slide.md).
Mạch kể của cả bài: [docs/storytelling_flow.md](docs/storytelling_flow.md).

---

# Ghi chú kỹ thuật

- **Đường dẫn ảnh**: slide dùng `./public/x.png`. Slidev phục vụ `public/` ở root nên
  console sẽ cảnh báo nên dùng `/x.png`. Đây chỉ là cảnh báo, build vẫn resolve đúng.
- **Lỗi `fixWebmDuration`** trong console dev: đến từ dependency của Slidev, chỉ liên
  quan tính năng quay video màn hình, không ảnh hưởng trình chiếu.
- **Windows**: mọi script đã bật `sys.stdout.reconfigure(encoding="utf-8")` để không
  lỗi `UnicodeEncodeError` khi in tiếng Việt ra console cp1252.

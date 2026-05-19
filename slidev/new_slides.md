---
title: Vualidon.FP New Presentation
info: |
  ## Slidev Starter Template (Scroll-Safe & Single Chart Optimized)
  Created with ImpressiveCover and ImpressiveHeader templates.
fonts:
  sans: 'Roboto'
---

<!-- SLIDE 1: COVER PAGE -->
<ImpressiveCover>
<template #subtitle>Investment & Financial Evaluation Dossier</template>
<template #info>
  <div>Prepared by: Analysis Team</div>
  <div>Author: Vualidon.FP</div>
  <div>Date: May 2026 | Version 1.0</div>
</template>
<template #image>
  <!-- Replace with your cover image -->
  <img src="./image.png" />
</template>
</ImpressiveCover>

---
transition: slide-left
---

<!-- SLIDE 2: 50-50 SPLIT (Optimized for HEAVY TEXT + 1 Large Chart, No Scroll) -->
<ImpressiveHeader>
<template #title>Tiêu Đề Slide: Bố Cục 50-50 Cho Nhiều Text</template>
<template #subtitle>Thiết kế tinh gọn, cỡ chữ và dòng tối ưu giúp chứa nhiều thông tin không bị tràn trang</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-6) - Tối ưu cho NHIỀU TEXT (Cỡ chữ 11px, dòng 1.3, khoảng cách hẹp) -->
  <div class="col-span-6 flex flex-col justify-start h-[390px] pr-2">
    <div class="space-y-2.5 mb-2 text-justify text-[11px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11.5px]">Đệm vốn và Thanh khoản (Ý chính 1):</strong><br />
        Bằng cách giảm nhẹ cỡ chữ xuống <span class="font-bold text-slate-800">11px</span> và dòng <span class="font-bold text-slate-800">leading-[1.3]</span>, bạn có thể viết được nhiều nội dung hơn mà hoàn toàn không sợ xuất hiện thanh cuộn (scroll).
      </p>
      <p>
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11.5px]">Kiểm định thực nghiệm giả thuyết (Ý chính 2):</strong><br />
        Khi trình bày các số liệu phức tạp từ mô hình hồi quy hoặc K-Means, việc trình bày văn bản rõ ràng, súc tích là cực kỳ quan trọng. Hãy sử dụng các màu sắc đồng bộ với biểu đồ để dẫn dắt mắt người đọc.
      </p>
      <p>
        <span class="text-[#0D9488] font-bold mr-1">♦</span>
        <strong class="text-[#0D9488] text-[11.5px]">Khuyến nghị chiến lược (Ý chính 3):</strong><br />
        Tóm tắt các hành động cụ thể ở cuối cột văn bản để tạo điểm nhấn kết thúc slide trước khi chuyển tiếp sang nội dung mới.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-6) - 1 Biểu đồ cân đối chiều rộng -->
  <div class="col-span-6 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <div class="w-full h-full bg-slate-50 border border-dashed border-slate-300 rounded flex items-center justify-center text-slate-400">
        [Biểu đồ 1 - Cân đối tỷ lệ 50-50]
      </div>
    </div>
  </div>
</div>

<template #footer-left>Phần I: Khái Quát | Slide 1.1 - Mẫu Text Nhiều</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 3: 40-60 SPLIT (Text Ít/Trung Bình + Chart To Rõ Nét) -->
<ImpressiveHeader>
<template #title>Tiêu Đề Slide: Bố Cục 40-60 (Ưu Tiên Chart)</template>
<template #subtitle>Tập trung thị giác vào biểu đồ bên trái, text bên phải bổ trợ thông tin</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-7) - Chart to chiếm 60% diện tích -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pr-4">
    <div class="w-full h-[370px]">
      <div class="w-full h-full bg-slate-50 border border-dashed border-slate-300 rounded flex items-center justify-center text-slate-400">
        [Biểu đồ 2 - Kích thước lớn nổi bật]
      </div>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-5) - Text ngắn gọn xúc tích (Cỡ 11.5px) -->
  <div class="col-span-5 flex flex-col justify-start h-[390px] pl-4 border-l border-slate-200/60">
    <div class="space-y-3 mb-2 text-justify text-[11.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-rose-600 font-bold mr-1">♦</span>
        <strong class="text-rose-600 text-[12px]">Điểm nóng dữ liệu:</strong><br />
        Bố cục này tập trung 60% diện tích cho biểu đồ bên trái để làm nổi bật các biến động lớn. Cột phải chỉ nên chứa 2 ý chính quan trọng nhất.
      </p>
      <p>
        <span class="text-slate-800 font-bold mr-1">♦</span>
        <strong class="text-slate-800 text-[12px]">Kết luận then chốt:</strong><br />
        Hạn chế nhồi nhét chữ ở cột này để giữ được khoảng thở (whitespace) cho slide thêm phần sang trọng và chuyên nghiệp.
      </p>
    </div>
  </div>
</div>

<template #footer-left>Phần I: Khái Quát | Slide 1.2 - Mẫu Ưu Tiên Chart</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 4: FULL-WIDTH CHART (Text Ngắn Trên Đầu + Chart Khổng Lồ Phía Dưới) -->
<ImpressiveHeader>
<template #title>Tiêu Đề Slide: Bố Cục Biểu Đồ Toàn Chiều Rộng</template>
<template #subtitle>Phù hợp cho biểu đồ dạng đường (Time-series) hoặc phân cụm (Scatter) cần hiển thị tối đa</template>

<div class="flex flex-col h-[420px] gap-2 text-slate-700">
  <!-- PHẦN TRÊN: Tóm tắt 2-3 dòng rất ngắn gọn (Không quá 3 dòng để tránh chiếm diện tích chart) -->
  <div class="text-[11px] leading-[1.25] text-slate-600 font-medium border-l-[3px] border-[#003366] pl-3 mb-2 flex-shrink-0 text-justify">
    <strong class="text-slate-800">Thông điệp cốt lõi:</strong>
    Tóm tắt thật ngắn gọn thông điệp chính tại đây. Bố cục này dành hơn 80% không gian đứng và 100% không gian ngang cho biểu đồ phía dưới, giúp hiển thị các biểu đồ phức tạp mà không bị vỡ hoặc mờ chữ.
  </div>

  <!-- PHẦN DƯỚI: Biểu đồ toàn chiều rộng, chiều cao cực lớn -->
  <div class="flex-grow min-h-0">
    <div class="w-full h-[330px] bg-slate-50 border border-dashed border-slate-300 rounded flex items-center justify-center text-slate-400">
      [Biểu đồ Full-Width Cực Lớn]
    </div>
  </div>
</div>

<template #footer-left>Phần II: Xu hướng | Slide 2.1 - Mẫu Biểu Đồ Toàn Rộng</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 1.1: Tổng tài sản toàn ngành & GDP Macro Context -->
<ImpressiveHeader>
<template #title>Chương 1: Quy mô &amp; Tăng trưởng</template>
<template #subtitle>Tổng tài sản toàn hệ thống Ngân hàng Việt Nam &amp; Bối cảnh phục hồi GDP vĩ mô (2020 – 2024)</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-6) -->
  <div class="col-span-6 flex flex-col justify-start h-[390px] pr-2">
    <div class="space-y-2.5 mb-2 text-justify text-[11px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11.5px]">Tài sản mở rộng mạnh mẽ đồng pha vĩ mô:</strong><br />
        Tổng tài sản toàn ngành ghi nhận đà tăng trưởng liên tục, từ <span class="font-bold text-[#003366]">10.87 triệu tỷ VND</span> (2020) lên <span class="font-bold text-[#003366]">19.31 triệu tỷ VND</span> (2024), tương đương mức tăng trưởng tích lũy <span class="font-bold text-[#003366]">+77.7%</span> trong 5 năm. Quy mô bảng cân đối kế toán toàn hệ thống được thúc đẩy trực tiếp từ đà phục hồi GDP vĩ mô, vọt từ đáy <span class="font-bold text-[#E67300]">2.91%</span> (2020) lên <span class="font-bold text-[#E67300]">7.09%</span> (2024).
      </p>
      <p>
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11.5px]">Tốc độ tăng trưởng tài sản duy trì hai chữ số:</strong><br />
        Tăng trưởng TTS YoY liên tục duy trì trên <span class="font-bold text-[#003366]">11%</span> mỗi năm, đạt đỉnh <span class="font-bold text-[#003366]">16.33%</span> (2024), phản ánh nhu cầu tín dụng bùng nổ sau đại dịch và sự mở rộng quy mô bảng cân đối toàn hệ thống. Đáng chú ý, tốc độ mở rộng tài sản vượt xa tốc độ tăng trưởng GDP thực, cho thấy vai trò trung gian tài chính của ngành ngân hàng ngày càng được khuếch đại trong nền kinh tế.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-6) - Biểu đồ -->
  <div class="col-span-6 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_1_1_assets_gdp.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần I: Bức tranh toàn cảnh | Slide 1.1 – Quy mô Tài sản &amp; Bối cảnh GDP</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 1.2: Tăng trưởng Vốn điều lệ & Vốn CSH + Equity/TTS -->
<ImpressiveHeader>
<template #title>Chương 1: Tăng trưởng Vốn &amp; Đệm An toàn</template>
<template #subtitle>Vốn điều lệ, Vốn chủ sở hữu &amp; Tỷ lệ an toàn vốn Equity/TTS toàn hệ thống (2020 – 2024)</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-6) -->
  <div class="col-span-6 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2.5 mb-2 text-justify text-[11px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#3399FF] font-bold mr-1">♦</span>
        <strong class="text-[#3399FF] text-[11.5px]">Năng lực tài chính cốt lõi liên tục được củng cố:</strong><br />
        Quy mô vốn chủ sở hữu (VCSH) và vốn điều lệ (VĐL) toàn hệ thống ghi nhận đà tăng trưởng tích cực, đạt lần lượt <span class="font-bold text-[#3399FF]">1,612 nghìn tỷ VND</span> và <span class="font-bold text-[#003366]">817 nghìn tỷ VND</span> vào cuối năm 2024, tương ứng mức tăng trưởng <span class="font-bold text-[#3399FF]">+105.3%</span> và <span class="font-bold text-[#003366]">+91.9%</span> so với năm 2020. Sự gia tăng này cho thấy nỗ lực của các ngân hàng trong việc gia tăng bộ đệm vốn tự có nhằm đáp ứng tiêu chuẩn Basel II.
      </p>
      <p>
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11.5px]">Đệm vốn suy yếu dưới áp lực đòn bẩy rủi ro:</strong><br />
        Mặc dù tăng trưởng mạnh, tốc độ tăng của VCSH và VĐL vẫn không bắt kịp tốc độ phình to của tổng tài sản, khiến tỷ lệ an toàn vốn (được đo lường bằng tỷ lệ Equity/TTS) đạt đỉnh <span class="font-bold text-[#E67300]">9.15%</span> (năm 2022) rồi giảm dần xuống còn <span class="font-bold text-[#E67300]">8.77%</span> (năm 2024). Mức sụt giảm <span class="font-bold text-[#E67300]">0.38 điểm phần trăm (pp)</span> trong 2 năm cho thấy các ngân hàng đang có xu hướng tăng cường sử dụng đòn bẩy tài chính để tối ưu lợi nhuận thay vì củng cố đệm vốn.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-6) - Biểu đồ -->
  <div class="col-span-6 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_1_2_capital.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần I: Bức tranh toàn cảnh | Slide 1.2 – Tăng trưởng Vốn &amp; Đệm An toàn Hệ thống</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 1.3: Phân hóa Đệm vốn toàn hệ thống -->
<ImpressiveHeader>
<template #title>Chương 1: Phân hóa Đệm vốn Hệ thống</template>
<template #subtitle>Khoảng cách Equity/TTS giữa nhóm dẫn đầu &amp; nhóm cuối bảng — Năm 2024</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2.5 mb-2 text-justify text-[11px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11.5px]">Phân hóa tiềm lực tài chính rõ rệt:</strong><br />
        Hệ thống ghi nhận sự phân hóa cao về tiềm lực tài chính khi khoảng cách về tỷ lệ Equity/TTS lên tới <span class="font-bold text-[#003366]">10.80 điểm phần trăm (pp)</span> giữa nhóm ngân hàng dẫn đầu (<span class="font-bold text-[#003366]">NH 8: 15.94%</span>) và nhóm cuối bảng (<span class="font-bold text-[#CC3333]">NH 22: 5.14%</span>).
      </p>
      <p>
        <span class="text-[#CC3333] font-bold mr-1">♦</span>
        <strong class="text-[#CC3333] text-[11.5px]">Cảnh báo đệm vốn mỏng:</strong><br />
        Đáng chú ý, hệ thống xuất hiện sự phân hóa rủi ro lớn khi có <span class="font-bold text-[#CC3333]">5 ngân hàng</span> sở hữu đệm vốn mỏng dưới 6% (tiệm cận mức cảnh báo nguy hiểm): <span class="font-bold text-[#CC3333]">NH 22 (5.14%)</span>, <span class="font-bold text-[#CC3333]">NH 1 (5.25%)</span>, <span class="font-bold text-[#CC3333]">NH 24 (5.34%)</span>, <span class="font-bold text-[#CC3333]">NH 3 (5.55%)</span> và <span class="font-bold text-[#CC3333]">NH 21 (5.94%)</span>, đặt nhóm này trước rủi ro tổn thương cực lớn khi chất lượng tài sản suy giảm đột ngột.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) - Biểu đồ lớn -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[380px]">
      <img src="./public/new_slide_1_3_equity_dispersion.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần I: Bức tranh toàn cảnh | Slide 1.3 – Phân hóa Đệm vốn Hệ thống</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 2.1: ROA & ROE toàn ngành -->
<ImpressiveHeader>
<template #title>Chương 2: Hiệu quả Sinh lời Hệ thống</template>
<template #subtitle>ROA &amp; ROE trung bình toàn ngành ngân hàng (2020 – 2024)</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2.5 mb-2 text-justify text-[11px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11.5px]">ROA toàn ngành đi theo quỹ đạo hình chữ ∩:</strong><br />
        Chỉ số ROA trung bình hệ thống tăng từ <span class="font-bold text-[#003366]">1.04%</span> (2020) lên đỉnh <span class="font-bold text-[#003366]">1.40%</span> (2022), rồi hạ nhiệt trở lại mức <span class="font-bold text-[#003366]">1.04%</span> (2024). Điều này phản ánh khả năng sinh lời trên tổng tài sản đã quay về mức xuất phát sau giai đoạn bùng nổ hậu COVID-19, cho thấy áp lực lên hiệu suất sử dụng tài sản đang gia tăng.
      </p>
      <p>
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11.5px]">ROE suy giảm rõ rệt, phân hóa khốc liệt:</strong><br />
        Hiệu quả sử dụng vốn chủ sở hữu (ROE) trung bình giảm mạnh từ đỉnh <span class="font-bold text-[#E67300]">15.07%</span> (2022) xuống <span class="font-bold text-[#E67300]">10.57%</span> (2024). Đặc biệt, hệ thống ghi nhận sự phân hóa cực đoan với biên độ chênh lệch lên tới <span class="font-bold text-[#E67300]">107.56pp</span> giữa NH 11 (<span class="font-bold text-[#E67300]">23.38%</span>) và NH 22 (<span class="font-bold text-[#CC3333]">−84.18%</span>), chứng minh rằng đòn bẩy tài chính và chất lượng tài sản sinh lời tại mỗi ngân hàng đang được tối ưu hóa theo những kịch bản rất khác nhau.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) - Biểu đồ -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_2_1_roa_roe.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần II: Hiệu quả Sinh lời | Slide 2.1 – ROA &amp; ROE Hệ thống</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 2.2: Áp lực biên lãi thuần (NIM) -->
<ImpressiveHeader>
<template #title>Chương 2: Áp lực Biên lãi thuần (NIM)</template>
<template #subtitle>NIM đạt đỉnh 2022 rồi co hẹp — 19/27 ngân hàng bị thu hẹp biên lãi trong giai đoạn 2022–2024</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI: Text + NIM system chart (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-start h-[390px] pr-2">
    <!-- Text -->
    <div class="text-justify text-[10.5px] leading-[1.35] text-slate-600 font-medium mb-3 animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">NIM đạt đỉnh rồi co hẹp dưới sức ép vĩ mô:</strong><br />
        Biên lãi thuần (NIM) toàn ngành đạt đỉnh <span class="font-bold text-[#003366]">3.23%</span> vào năm 2022, sau đó liên tục thu hẹp còn <span class="font-bold text-[#003366]">2.79%</span> (2024). Chính sách tiền tệ giật cục và áp lực tỷ giá làm mặt bằng Cost of Funds biến động mạnh, bóp nghẹt biên lãi. Kết quả là <span class="font-bold text-[#E67300]">19/27 ngân hàng (70.4%)</span> bị thu hẹp NIM trong giai đoạn 2022–2024.
      </p>
    </div>
    <!-- NIM System chart (small, phía dưới text) -->
    <div class="flex-grow flex items-center justify-start">
      <img src="./public/new_slide_2_2_nim.png" class="h-[230px] w-auto object-contain" />
    </div>
  </div>

  <!-- CỘT PHẢI: NIM Compression chart (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[380px]">
      <img src="./public/new_slide_2_2_nim_compression.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần II: Hiệu quả Sinh lời | Slide 2.2 – Áp lực Biên lãi thuần (NIM)</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 3.1: Cơ cấu thu nhập hoạt động -->
<ImpressiveHeader>
<template #title>Chương 3: Cơ cấu Thu nhập & Chi phí</template>
<template #subtitle>Phân rã nguồn thu nhập hoạt động (TOI) toàn hệ thống (2020 – 2024)</template>

<div class="grid grid-cols-12 gap-x-6 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2 mb-2 text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">Thu nhập lãi thuần vẫn chiếm vị thế áp đảo:</strong><br />
        Tỷ trọng thu nhập lãi thuần trên TOI tăng từ <span class="font-bold text-[#003366]">75.30%</span> (2020) lên <span class="font-bold text-[#003366]">78.33%</span> (2024), cho thấy hệ thống ngân hàng Việt Nam vẫn phụ thuộc nặng nề vào hoạt động tín dụng truyền thống. Ngược lại, tỷ trọng thu ngoài lãi giảm từ <span class="font-bold text-[#E67300]">24.70%</span> xuống <span class="font-bold text-[#E67300]">21.67%</span>.
      </p>
      <p>
        <span class="text-[#00897B] font-bold mr-1">♦</span>
        <strong class="text-[#00897B] text-[11px]">Thu dịch vụ thuần co hẹp:</strong><br />
        Đáng chú ý, tỷ trọng thu nhập dịch vụ thuần (Fee Income Ratio) giảm từ <span class="font-bold text-[#00897B]">10.86%</span> xuống <span class="font-bold text-[#00897B]">9.00%</span>, cho thấy nỗ lực đa dạng hóa nguồn thu từ phí dịch vụ chưa đạt kỳ vọng, trong khi mảng ngoại hối & vàng tăng nhẹ từ 2.97% lên 4.11% nhờ biến động tỷ giá.
      </p>
      <p class="italic text-slate-500 text-[10px] mt-1">
        *Macro: Dòng vốn FDI giải ngân đạt đỉnh lịch sử 25.35 tỷ USD (2024) và tiêu dùng bán lẻ phục hồi mạnh mẽ là động lực hỗ trợ mảng thu ngoại hối và dịch vụ thanh toán.*
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-4 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_3_1_income_mix.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần III: Cơ cấu Thu nhập & Chi phí | Slide 3.1 – Đa dạng hóa Nguồn thu</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 3.2: Phân hóa CIR -->
<ImpressiveHeader>
<template #title>Chương 3: Phân hóa Chi phí Hoạt động</template>
<template #subtitle>Tỷ lệ Chi phí trên Thu nhập (CIR) toàn hệ thống năm 2024</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2 mb-2 text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">Phân hóa khổng lồ về hiệu quả chi phí:</strong><br />
        Tỷ lệ CIR (Cost-to-Income Ratio) năm 2024 ghi nhận khoảng cách chênh lệch lên tới <span class="font-bold text-[#CC3333]">46.94pp</span> giữa ngân hàng tối ưu chi phí tốt nhất (NH 8: <span class="font-bold text-[#00897B]">23.0%</span>) và kém nhất (NH 25: <span class="font-bold text-[#CC3333]">70.0%</span>). Trung bình hệ thống ở mức <span class="font-bold text-[#007FFF]">40.1%</span>.
      </p>
      <p>
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11px]">Nhóm chi phí cao — rủi ro vận hành:</strong><br />
        Có 5 ngân hàng duy trì CIR trên 50% (NH 25, NH 20, NH 21, NH 26, NH 19), phản ánh bộ máy vận hành cồng kềnh hoặc năng lực tạo thu nhập còn hạn chế. Các ngân hàng này đối mặt áp lực lớn khi biên lãi tiếp tục thu hẹp.
      </p>
      <p class="italic text-slate-500 text-[10px] mt-1">
        *Lưu ý: NH 22 (TOI âm) được loại trừ khỏi phân tích CIR do không có ý nghĩa thống kê.*
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[380px]">
      <img src="./public/new_slide_3_2_cir_dispersion.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần III: Cơ cấu Thu nhập & Chi phí | Slide 3.2 – Phân hóa CIR</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 4.1: CASA Ratio -->
<ImpressiveHeader>
<template #title>Chương 4: Huy động & Tín dụng</template>
<template #subtitle>Tỷ lệ tiền gửi không kỳ hạn (CASA) duy trì xu hướng thấp quanh 15.7%</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">Dòng tiền rẻ chững lại:</strong><br />
        Tỷ lệ tiền gửi không kỳ hạn (CASA Ratio) trung bình toàn ngành biến động trồi sụt, sau khi giảm từ đỉnh 17.70% (2021) hiện đang neo ở mức <span class="font-bold text-[#003366]">15.72%</span>. Điều này phản ánh xu hướng thắt chặt chi tiêu của người dân và sự dịch chuyển của dòng tiền nhàn rỗi sang các kênh đầu tư hoặc tiền gửi có kỳ hạn dài hơn để tìm kiếm lợi suất an toàn.
      </p>
      <p class="mt-3">
        <span class="text-[#E67300] font-bold mr-1">♦</span>
        <strong class="text-[#E67300] text-[11px]">Phân hóa CASA khổng lồ:</strong><br />
        Lợi thế nguồn vốn rẻ không chia đều. Dữ liệu ghi nhận mức chênh lệch CASA khổng lồ lên tới <span class="font-bold text-[#E67300]">35.23 điểm phần trăm (pp)</span> giữa nhóm dẫn đầu và nhóm cuối bảng trong năm 2024, tạo ra áp lực huy động vốn (Cost of Funds) rất lớn cho các ngân hàng top dưới.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[320px]">
      <img src="./public/new_slide_4_1_casa.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần IV: Huy động & Tín dụng | Slide 4.1 – Xu hướng CASA</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 4.2: LDR bùng nổ -->
<ImpressiveHeader>
<template #title>Chương 4: Rủi ro Thanh khoản (LDR)</template>
<template #subtitle>Tỷ lệ LDR vượt mức 100%, huy động không theo kịp tín dụng</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#CC3333] font-bold mr-1">♦</span>
        <strong class="text-[#CC3333] text-[11px]">LDR tăng vọt lên mức báo động:</strong><br />
        Tỷ lệ dư nợ trên tổng vốn huy động (LDR) trung bình toàn ngành leo dốc liên tục từ mức an toàn <span class="font-bold text-[#003366]">91.11%</span> (2020) lên <span class="font-bold text-[#CC3333]">103.25%</span> (2024). Đáng chú ý, có tới <span class="font-bold text-[#CC3333]">15/27 ngân hàng</span> thương mại đã vượt qua ngưỡng "trần an toàn" 100%.
      </p>
      <p class="mt-3">
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">Rủi ro kỳ hạn & Thanh khoản:</strong><br />
        Thực trạng này phản ánh tình trạng căng thẳng thanh khoản trầm trọng và rủi ro kỳ hạn (Maturity Gap) ngày càng lớn khi nguồn vốn huy động tiền gửi từ khách hàng không đuổi kịp tốc độ bơm tín dụng ra nền kinh tế.
      </p>
      <p class="italic text-slate-500 text-[10px] mt-2">
        *Macro Context: Áp lực tỷ giá từ sức mạnh đồng USD (DXY) buộc NHNN phải hút tiền trong nhiều giai đoạn, làm cung tiền M2 tăng trưởng chậm lại so với dư nợ, gây khát thanh khoản cục bộ.*
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[320px]">
      <img src="./public/new_slide_4_2_ldr.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần IV: Huy động & Tín dụng | Slide 4.2 – Áp lực LDR</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 4.3: Bán lẻ hóa tín dụng -->
<ImpressiveHeader>
<template #title>Chương 4: Cấu trúc Tín dụng</template>
<template #subtitle>Tỷ trọng cho vay cá nhân tăng trưởng mạnh mẽ đạt mức ~48%</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#00897B] font-bold mr-1">♦</span>
        <strong class="text-[#00897B] text-[11px]">Chuyển dịch sang mảng bán lẻ:</strong><br />
        Cấu trúc tín dụng hệ thống chứng kiến sự dịch chuyển chiến lược. Tỷ trọng cho vay khách hàng cá nhân (theo quy mô dư nợ tổng hợp) đã tăng từ <span class="font-bold text-[#00897B]">47.18%</span> (2020) lên mức <span class="font-bold text-[#00897B]">48.49%</span> (2024), phản ánh định hướng phân tán rủi ro và cải thiện biên lợi nhuận (NIM) của các ngân hàng.
      </p>
      <p class="mt-3">
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">Động lực từ vĩ mô:</strong><br />
        Sau "vực thẳm" đại dịch (tháng 8/2021), tổng mức bán lẻ hàng hóa lấy lại quỹ đạo tăng trưởng ổn định 8-9% YoY. Điểm tựa tiêu dùng mạnh mẽ này đã kích thích trực tiếp đến mảng cho vay tiêu dùng, thẻ tín dụng và vay mua nhà cá nhân.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[320px]">
      <img src="./public/new_slide_4_3_retail.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần IV: Huy động & Tín dụng | Slide 4.3 – Cấu trúc Tín dụng</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 5.1: NPL Trend -->
<ImpressiveHeader>
<template #title>Chương 5: Sức khỏe Tài sản</template>
<template #subtitle>Bão nợ xấu: Vết sẹo có độ trễ từ thời kỳ COVID-19</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#CC3333] font-bold mr-1">♦</span>
        <strong class="text-[#CC3333] text-[11px]">Tỷ lệ nợ xấu (NPL) vọt tăng:</strong><br />
        Tỷ lệ nợ xấu trung bình toàn ngành ghi nhận đà tăng mạnh từ mức an toàn <span class="font-bold text-[#003366]">1.74%</span> (năm 2020) lên mức <span class="font-bold text-[#CC3333]">2.87%</span> (năm 2024), tương đương mức tăng hơn 1.6 lần. Đây là hồi chuông cảnh báo về rủi ro mất vốn tiềm ẩn trên bảng cân đối kế toán.
      </p>
      <p class="mt-3">
        <span class="text-[#003366] font-bold mr-1">♦</span>
        <strong class="text-[#003366] text-[11px]">Hết thời gian ân hạn:</strong><br />
        Các khoản nợ được gia hạn, giãn hoãn theo Thông tư 01 và 02 từ thời kỳ đại dịch Covid-19 đã dần hết thời gian ân hạn, buộc các ngân hàng phải chuyển nhóm nợ. Điều này khiến nợ xấu tích tụ bấy lâu nay chính thức bùng phát.
      </p>
      <p class="italic text-slate-500 text-[10px] mt-2">
        *Macro Context: Mặc dù hoạt động sản xuất đã phục hồi (PMI liên tục >51.0 vào năm 2024), dòng tiền thực tế của nhiều doanh nghiệp vẫn ở trạng thái kiệt quệ sau chuỗi cú sốc liên tiếp, không đủ khả năng trả nợ cũ.*
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[320px]">
      <img src="./public/new_slide_5_1_npl.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần V: Sức khỏe Tài sản | Slide 5.1 – Nợ xấu (NPL)</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 5.2: LLR -->
<ImpressiveHeader>
<template #title>Chương 5: Phân hóa Rủi ro</template>
<template #subtitle>Đệm dự phòng (LLR) mỏng đi đáng lo ngại trên diện rộng</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10.5px] leading-[1.3] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-[#CC3333] font-bold mr-1">♦</span>
        <strong class="text-[#CC3333] text-[11px]">Đệm dự phòng suy yếu:</strong><br />
        Tỷ lệ bao phủ nợ xấu (Coverage Ratio - LLR) đánh giá khả năng chống chịu của ngân hàng trước các cú sốc tín dụng. Hệ thống ghi nhận mức LLR suy giảm nghiêm trọng khi có tới <span class="font-bold text-[#CC3333]">22 trên tổng số 27 ngân hàng</span> (chiếm hơn 80% hệ thống) có tỷ lệ bao phủ dưới mức 100%.
      </p>
      <p class="mt-3">
        <span class="text-[#00897B] font-bold mr-1">♦</span>
        <strong class="text-[#00897B] text-[11px]">Nhóm phòng thủ vững chắc:</strong><br />
        Sự phân hóa diễn ra cực đoan khi chỉ có đúng <span class="font-bold text-[#00897B]">2 ngân hàng</span> duy trì được tỷ lệ bao phủ nợ xấu ở mức an toàn cao (trên 150%). Các ngân hàng top dưới không chỉ đối mặt với nợ xấu tăng cao (NPL > 3.0%) mà còn không có đủ nguồn lực trích lập dự phòng (LLR < 50%), đe dọa trực tiếp đến lợi nhuận cốt lõi trong tương lai.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[380px]">
      <img src="./public/new_slide_5_2_llr.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần V: Sức khỏe Tài sản | Slide 5.2 – Tỷ lệ Bao phủ Nợ xấu</template>
</ImpressiveHeader>

---
transition: fade
layout: center
---

<!-- SLIDE SUMMARY -->
<div class="w-full max-w-[900px] bg-white rounded-xl shadow-xl overflow-hidden border border-slate-200 p-8 relative">
  <!-- Decorative top bar -->
  <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-[#003366] via-[#0066CC] to-[#00897B]"></div>
  
  <div class="text-center mb-8">
    <h2 class="text-2xl font-bold text-[#003366] mb-2 font-serif">TỔNG HỢP: SCORECARD (2024)</h2>
    <p class="text-sm text-slate-500 font-medium italic">Bức tranh toàn cảnh: Duy trì tăng trưởng quy mô đi kèm với sự phân hóa sâu sắc và rủi ro tiềm ẩn gia tăng</p>
  </div>
  
  <div class="grid grid-cols-4 gap-4 mb-8">
    <!-- Sinh lời -->
    <div class="bg-blue-50/50 rounded-lg p-4 border border-blue-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
      <span class="text-[10px] uppercase font-bold text-blue-800 tracking-wider mb-1">Sinh lời (ROA)</span>
      <span class="text-2xl font-bold text-[#003366]">1.04%</span>
      <span class="text-[9px] text-blue-600 font-medium mt-1">Trạng thái đi ngang</span>
    </div>
    <div class="bg-blue-50/50 rounded-lg p-4 border border-blue-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
      <span class="text-[10px] uppercase font-bold text-blue-800 tracking-wider mb-1">Sinh lời (ROE)</span>
      <span class="text-2xl font-bold text-[#003366]">11.23%</span>
      <span class="text-[9px] text-blue-600 font-medium mt-1">Đà tăng trưởng chững lại</span>
    </div>
    <div class="bg-indigo-50/50 rounded-lg p-4 border border-indigo-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
      <span class="text-[10px] uppercase font-bold text-indigo-800 tracking-wider mb-1">Biên lãi (NIM)</span>
      <span class="text-2xl font-bold text-[#003366]">2.79%</span>
      <span class="text-[9px] text-indigo-600 font-medium mt-1">Thu hẹp đáng kể</span>
    </div>
    <div class="bg-indigo-50/50 rounded-lg p-4 border border-indigo-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
      <span class="text-[10px] uppercase font-bold text-indigo-800 tracking-wider mb-1">Chi phí (CIR)</span>
      <span class="text-2xl font-bold text-[#003366]">40.1%</span>
      <span class="text-[9px] text-indigo-600 font-medium mt-1">Phân hóa mạnh mẽ (46.9pp)</span>
    </div>
    <!-- Huy động & Tín dụng & Nợ -->
    <div class="col-span-4 grid grid-cols-3 gap-4 mt-2">
      <div class="bg-amber-50/50 rounded-lg p-4 border border-amber-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
        <span class="text-[10px] uppercase font-bold text-amber-800 tracking-wider mb-1">Nguồn vốn (CASA)</span>
        <span class="text-2xl font-bold text-[#E67300]">15.72%</span>
        <span class="text-[9px] text-amber-600 font-medium mt-1">Nguồn vốn thắt chặt, chi phí huy động tăng</span>
      </div>
      <div class="bg-red-50/50 rounded-lg p-4 border border-red-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
        <span class="text-[10px] uppercase font-bold text-red-800 tracking-wider mb-1">Thanh khoản (LDR)</span>
        <span class="text-2xl font-bold text-[#CC3333]">103.25%</span>
        <span class="text-[9px] text-red-600 font-medium mt-1">Áp lực thanh khoản (15 NH vượt mốc 100%)</span>
      </div>
      <div class="bg-red-50/50 rounded-lg p-4 border border-red-100 flex flex-col items-center justify-center transform transition-transform hover:scale-105">
        <span class="text-[10px] uppercase font-bold text-red-800 tracking-wider mb-1">Nợ xấu (NPL)</span>
        <span class="text-2xl font-bold text-[#CC3333]">2.87%</span>
        <span class="text-[9px] text-red-600 font-medium mt-1">Rủi ro gia tăng, đệm dự phòng suy yếu</span>
      </div>
    </div>
  </div>
  
  <div class="bg-slate-50 border-l-4 border-[#003366] p-4 rounded-r-lg">
    <p class="text-[12px] leading-relaxed text-slate-700">
      <span class="font-bold text-[#003366] uppercase">Phần II: Đào sâu nguyên nhân tạo nên sự phân hóa</span><br/>
      Nhìn chung, hệ thống ngân hàng về mặt tổng thể vẫn ghi nhận sự mở rộng về quy mô tín dụng. Tuy nhiên, hiệu quả vận hành và chất lượng tài sản lại bộc lộ mức độ phân hóa sâu sắc. <strong class="text-[#E67300]">Phần tiếp theo sẽ đi sâu phân tích cấu trúc nhân quả, nhằm bóc tách các yếu tố cốt lõi đang trực tiếp chi phối sự khác biệt về năng lực sinh lời bền vững trong chu kỳ hiện tại.</strong>
    </p>
  </div>
</div>

---
transition: slide-left
---

<!-- SLIDE 6.1: Giai đoạn 1 - Bối cảnh Vĩ mô -->
<ImpressiveHeader>
<template #title>Chương 6: Giai đoạn 1 (2020-2021) — "Ai có vốn rẻ, người đó sống"</template>
<template #subtitle>1. Bối cảnh vĩ mô: Cú sốc hệ thống & Áp lực ép giảm lợi suất đầu ra</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-4) -->
  <div class="col-span-4 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10px] leading-[1.2] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <strong class="text-[#003366] text-[10.5px] uppercase border-b border-slate-300 pb-0.5 mb-1 block">1. Đứt gãy chuỗi sản xuất</strong>
        Dưới tác động kép của COVID-19, kinh tế vĩ mô Việt Nam rơi vào suy thoái kỹ thuật. <span class="font-bold text-[#003366]">GDP rớt xuống đáy lịch sử</span>: chỉ đạt 2.91% (2020) và 2.56% (2021) do giãn cách. Chỉ số <span class="font-bold text-[#CC3333]">PMI sụp đổ về mức 32.7 điểm</span> (T4/2020), phản ánh sự ngưng trệ chuỗi sản xuất.
      </p>
      <p class="mt-2">
        <strong class="text-[#E67300] text-[10.5px] uppercase border-b border-slate-300 pb-0.5 mb-1 block">2. Áp lực chính sách lên Yield</strong>
        Trước tình thế cấp bách, NHNN ban hành Thông tư 01 và Thông tư 03 yêu cầu các TCTD cơ cấu lại nợ, miễn giảm lãi và phí để hỗ trợ doanh nghiệp. Chi phí huy động chưa kịp giảm nhưng lãi suất cho vay buộc phải hạ ngay lập tức.
      </p>
      <div class="bg-blue-50 border-l-2 border-[#003366] p-1.5 mt-2 rounded text-[9.5px] leading-[1.2]">
        <strong class="text-[#003366]">Hệ quả then chốt:</strong><br/>
        Lợi suất tài sản sinh lời (Yield đầu ra) bị ép giảm đồng loạt trên toàn hệ thống. <strong class="text-[#E67300]">Do đó, Yield không phải là nhân tố tạo ra sự phân hóa hiệu quả sinh lời (NIM) trong giai đoạn này, vì tất cả đều chịu chung áp lực pháp lý.</strong>
      </div>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-8) -->
  <div class="col-span-8 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[360px]">
      <img src="./public/new_slide_6_1_macro.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần VI: Giai đoạn 1 (2020-2021) | Slide 6.1 – Cú sốc Vĩ mô</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 6.2: Giai đoạn 1 - CASA vs CoF -->
<ImpressiveHeader>
<template #title>Chương 6: Giai đoạn 1 (2020-2021) — "Ai có vốn rẻ, người đó sống"</template>
<template #subtitle>2. Nhánh nhân quả chính: Lá chắn CASA quyết định CoF và NIM</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10px] leading-[1.25] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <strong class="text-[#003366] text-[10.5px] uppercase border-b border-slate-300 pb-0.5 mb-1 block">1. Kiểm định thực nghiệm (Mô hình hồi quy)</strong>
        Dữ liệu thực chứng xác nhận sự phân hóa NIM khổng lồ (từ 1.22% đến 8.34%) thực chất được định đoạt ở đầu vào. Tỷ lệ CASA giải thích tới <span class="font-bold text-[#003366]">75%</span> sự biến động của Chi phí vốn (R² ≈ 0.75). Tương quan nghịch cực mạnh (r = -0.864) khẳng định CASA là lá chắn phòng thủ tối thượng giúp các ngân hàng neo giữ giá vốn.
      </p>
      <p class="mt-2.5">
        <strong class="text-[#00897B] text-[10.5px] uppercase border-b border-slate-300 pb-0.5 mb-1 block">2. Phân hóa thực tế khốc liệt</strong>
        <span class="text-[#00897B] font-bold block mb-0.5">■ Nhóm dẫn đầu (Vùng dưới cùng bên phải):</span>
        Sở hữu hệ sinh thái số mạnh, điển hình là NH7 (CASA 45.6%) và NH6 (40.8%), đã kéo tụt CoF xuống vùng rất thấp (< 3%), đẩy NIM lên đỉnh 5.5% và ROA dẫn đầu ngành 3.4%.
      </p>
      <p class="mt-2">
        <span class="text-[#CC3333] font-bold block mb-0.5">■ Nhóm tụt hậu (Vùng trên cùng bên trái):</span>
        Thiếu hụt CASA (NH20: 2.4%, NH24: 4.2%), phải phụ thuộc vào dòng vốn bán buôn đắt đỏ khiến CoF đội lên tới > 7%. Hệ quả là NIM bị bóp nghẹt xuống 1.2% - 2.0%, đẩy ROA tiệm cận mức 0%.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_6_2_casa_cof.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần VI: Giai đoạn 1 (2020-2021) | Slide 6.2 – Phân tích Nhân quả CASA & CoF</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 6.3: Giai đoạn 1 - Nghịch lý Đòn bẩy -->
<ImpressiveHeader>
<template #title>Chương 6: Giai đoạn 1 (2020-2021) — "Ai có vốn rẻ, người đó sống"</template>
<template #subtitle>3. Nhánh phụ 1: Nghịch lý đòn bẩy tài chính trong khủng hoảng</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="text-justify text-[10px] leading-[1.25] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <strong class="text-[#003366] text-[10.5px] uppercase border-b border-slate-300 pb-0.5 mb-1 block">1. Sự phá vỡ lý thuyết truyền thống</strong>
        Lý thuyết tài chính doanh nghiệp truyền thống cho rằng trong điều kiện bình thường, việc tăng cường sử dụng đòn bẩy tài chính (hệ số nhân vốn chủ sở hữu cao) sẽ giúp khuếch đại tỷ suất sinh lời trên vốn chủ sở hữu (ROE). Tuy nhiên, dữ liệu thực tế của hệ thống ngân hàng Việt Nam trong khủng hoảng 2020-2021 lại chứng minh một nghịch lý hoàn toàn trái ngược.
      </p>
      <p class="mt-2.5">
        <strong class="text-[#00897B] text-[10.5px] uppercase border-b border-slate-300 pb-0.5 mb-1 block">2. Cơ chế tác động của khủng hoảng</strong>
        Khi nền kinh tế đối mặt với cú sốc hệ thống và chất lượng tài sản đi xuống, đòn bẩy tài chính cao không đóng vai trò khuếch đại lợi nhuận mà ngược lại, phóng đại tổn thất thực tế. 
      </p>
      <div class="bg-red-50 border-l-2 border-[#CC3333] p-1.5 mt-2 rounded text-[9.5px] leading-[1.2]">
        <strong class="text-[#CC3333]">Hệ lụy của việc thiếu "đệm vốn":</strong><br/>
        Các ngân hàng có đệm vốn mỏng (Equity Ratio thấp) thường bị thị trường đánh giá rủi ro cao hơn, dẫn đến việc bị "phạt" bằng mức chi phí huy động vốn đắt đỏ trên thị trường liên ngân hàng và dân cư, trực tiếp làm xói mòn hiệu quả sinh lời tổng thể.
      </div>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_6_3_leverage.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần VI: Giai đoạn 1 (2020-2021) | Slide 6.3 – Nghịch lý Đòn bẩy</template>
</ImpressiveHeader>

---
transition: slide-left
---

<!-- SLIDE 6.4: Giai đoạn 1 - Nợ ẩn & VAMC -->
<ImpressiveHeader>
<template #title>Chương 6: Giai đoạn 1 (2020-2021) — "Ai có vốn rẻ, người đó sống"</template>
<template #subtitle>4. Nhánh phụ 2: Nợ ẩn — Sự bình yên tạm thời và quả bom nợ VAMC</template>

<div class="grid grid-cols-12 gap-x-4 mt--4 text-slate-700">
  <!-- CỘT TRÁI (col-span-5) -->
  <div class="col-span-5 flex flex-col justify-center h-[390px] pr-2">
    <div class="space-y-2 mb-2 text-justify text-[10px] leading-[1.25] text-slate-600 font-medium animate-fade-in-left">
      <p>
        <span class="text-slate-400 font-bold mr-1">♦</span>
        <strong class="text-slate-800 text-[10.5px]">Sự phẳng lặng của tỷ lệ nợ xấu báo cáo:</strong><br />
        Trong giai đoạn 2020-2021, chất lượng tài sản toàn ngành duy trì sự ổn định tạm thời. Tỷ lệ nợ xấu báo cáo toàn ngành (<span class="font-bold text-slate-500">NPL</span>) chỉ tăng nhẹ từ <span class="font-bold text-slate-500">1.74%</span> (2020) lên <span class="font-bold text-slate-500">1.78%</span> (2021), trung bình giai đoạn đạt <span class="font-bold text-slate-500">1.76%</span>, phản ánh khả năng chống chịu tốt của hệ thống trước đại dịch.
      </p>
      <p>
        <span class="text-[#CC3333] font-bold mr-1">♦</span>
        <strong class="text-[#CC3333] text-[10.5px]">Rủi ro nợ ẩn gia tăng dưới bảng cân đối kế toán:</strong><br />
        Tuy nhiên, rủi ro tín dụng thực tế đang tích tụ qua hai kênh nợ ẩn:
      </p>
      <div class="pl-3 border-l-2 border-[#CC3333] space-y-1.5 text-[9.5px]">
        <div>
          <strong class="text-slate-800">1. Nợ Nhóm 2 vọt tăng mạnh:</strong> 
          Tỷ lệ nợ cần chú ý tăng từ <span class="font-bold text-[#CC3333]">1.25% lên 1.67% (+0.42 pp)</span>, tương đương tốc độ tăng gấp hơn 10 lần nợ xấu báo cáo. Nhờ cơ chế hoãn hoãn nợ của Thông tư 01/2020 và 02/2021, các khoản nợ suy giảm chất lượng thực tế được giữ nguyên nhóm, biến Nhóm 2 thành nơi trú ẩn tạm thời.
        </div>
        <div>
          <strong class="text-slate-800">2. Trái phiếu đặc biệt VAMC tồn đọng:</strong> 
          Còn <span class="font-bold text-[#003366]">10/27 ngân hàng</span> gánh lượng trái phiếu VAMC lớn chưa tất toán. Đây là rủi ro nợ ẩn có độ trễ lớn, sẵn sàng phát nổ và ảnh hưởng mạnh đến lợi nhuận khi chính sách hỗ trợ hết hiệu lực.
        </div>
      </div>
    </div>
    
    <div class="bg-blue-50/50 p-1.5 rounded border border-blue-100/50 text-[9.5px] leading-[1.2] mt-1">
      <p class="text-slate-600">
        <strong class="text-[#004C99]">Chuyển tiếp:</strong> Lá chắn CASA và kỷ luật đòn bẩy hỗ trợ duy trì sự bình ổn tạm thời trong năm 2020-2021. Nhưng bước sang giai đoạn 2022-2023, khi chính sách tiền tệ đảo chiều và quả bom nợ ẩn hết thời gian ân hạn, cục diện chất lượng tài sản lập tức xoay chuyển.
      </p>
    </div>
  </div>

  <!-- CỘT PHẢI (col-span-7) - Biểu đồ -->
  <div class="col-span-7 flex flex-col justify-center h-[390px] pl-3 border-l border-slate-200/60">
    <div class="w-full h-[370px]">
      <img src="./public/new_slide_6_4_no_an_vamc.png" class="h-full w-full object-contain" />
    </div>
  </div>
</div>

<template #footer-left>Phần VI: Giai đoạn 1 (2020-2021) | Slide 6.4 – Rủi ro Nợ ẩn & VAMC</template>
</ImpressiveHeader>

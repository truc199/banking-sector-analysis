---
description: use to generate a slide
---

Bạn hãy tạo slide theo yêu cầu của user, sử dụng slidev:
- Từ yêu cầu của user, hãy tính toán lại các số liệu liên quan, sử dụng các trường dữ liệu từ file mapping.csv và các file data csv tương ứng.
- Trình bày lại ý hiểu của bạn về mong muốn của user: thông tin gì sẽ được đưa vào slide, thông tin gì bạn tính ra nhưng sẽ không đưa vào, bố cục của slide nhìn như thế nào, 
- Đợi user xác nhận các thông tin
- Nếu user đồng ý, viết slide ngay dưới cùng của slidev/slides.md 
- Khi viết slide, tuân thủ các yêu cầu sau: 
 + quy định chart dải màu xanh navy, dotted line với ipolate trọng số thấp để smoothing. 
 + khi vừa có bar vừa có line thì chọn cặp màu tương phản cao (bar thì nên đậm hơn line)
 + toàn bộ chart vẽ bằng matplotlib, với phông chữ của chart giống với của text
 + Chart layout phải giống nhau: trục tọa độ rõ ràng có chia vạch, có legend, title chart, axis title.
 + phần text: viết ngắn gọn, line spacing 1.15pt, không ví von ngoặc kép, văn phong báo cáo chuyên nghiệp, công sở, mang tính tài chính kinh tế.
 + Các số liệu quan trọng thì bôi đậm chữ với màu tương ứng với legend trong chart.
- Tất cả mọi slide đều phải sử dụng bố cục của ImpressiveHeader.vue

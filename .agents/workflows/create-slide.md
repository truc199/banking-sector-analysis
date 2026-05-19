---
description: use to generate a slide
---

Bạn hãy tạo slide theo yêu cầu của user, sử dụng slidev:
- Từ yêu cầu của user, hãy tính toán lại các số liệu liên quan, sử dụng các trường dữ liệu từ file mapping.csv và các file data csv tương ứng.
- Trình bày lại ý hiểu của bạn về mong muốn của user: thông tin gì sẽ được đưa vào slide, thông tin gì bạn tính ra nhưng sẽ không đưa vào, bố cục của slide nhìn như thế nào trước khi làm slide.
- Đợi user xác nhận các thông tin
- Nếu user đồng ý, viết slide ngay dưới cùng của slidev/slides.md 
- Khi viết slide, tuân thủ các yêu cầu sau: 
 + quy định chart tuân theo dải màu chủ đạo là màu xanh navy (#003366 Dark Midnight Blue -> #004C99 US Air Force Academy Blue -> #0066CC Bright Navy Blue -> #007FFF Azure -> #3399FF Dodger blue -> #66B2FF French Sky Blue -> #99CCFF Baby Blue Eyes), ngoài ra sử dụng màu đỏ gạch, cam đất, xanh ngọc làm màu phụ để highlight và làm rõ chữ tốt hơn với những chart có nhiều loại figure (VD: bar + line chart),  dotted line với ipolate trọng số thấp để smoothing. 
 + khi vừa có bar vừa có line thì chọn cặp màu tương phản cao (bar thì nên đậm hơn line).
 + toàn bộ chart vẽ bằng matplotlib, với phông chữ, cỡ chữ của chart giống với của text. Tỉ lệ text và kích cỡ line/bar/... trong chart hợp lí, hài hòa.
 + Chart layout phải giống nhau: trục tọa độ rõ ràng có chia vạch, có legend, title chart, axis title.
 + Legend để ở dưới chart.
 + phần text: line spacing 1pt, không ví von ngoặc kép, văn phong báo cáo chuyên nghiệp, công sở, mang tính tài chính kinh tế. 
 + Cố gắng không để thừa khoảng trắng nào trong slide. 
 + Các số liệu quan trọng thì bôi đậm chữ với màu tương ứng với legend trong chart.
 + Tăng kích cỡ chart sao cho không có chữ nào bị đè nhau, và đè lên biểu đồ
- Tất cả mọi slide đều phải sử dụng bố cục của ImpressiveHeader.vue
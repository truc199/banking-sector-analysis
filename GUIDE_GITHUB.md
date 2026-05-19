# Hướng dẫn đẩy dự án lên GitHub

Dưới đây là các bước chi tiết để bạn đưa thư mục dự án `d:\uni\gcontest` lên GitHub một cách an toàn và sạch sẽ nhất.

---

### Bước 1: Cấu hình Git (Chỉ cần làm lần đầu tiên)
Nếu đây là lần đầu bạn dùng Git trên máy tính, chạy 2 lệnh sau trên terminal để cấu hình thông tin cá nhân:
```bash
git config --global user.name "truc199"
git config --global user.email "quangtruc1909@gmail.com"
```

---

### Bước 2: Khởi tạo Git
Mở terminal/cmd tại thư mục `d:\uni\gcontest` và chạy:
```bash
git init
```

---

### Bước 3: Thêm và Commit các file
Thêm toàn bộ các file vào bộ nhớ đệm (Git sẽ tự động bỏ qua `.venv` nhờ file `.gitignore` đã có sẵn):
```bash
git add .
```

Commit các file đã thêm với một lời nhắn:
```bash
git commit -m "Initial commit"
```

---

### Bước 4: Tạo Repository trên GitHub
1. Truy cập [github.com](https://github.com/) và bấm nút **New** để tạo Repository mới.
2. Nhập tên Repository (ví dụ: `gcontest`).
3. **Lưu ý:** Không tích vào bất kỳ ô nào như *Add a README*, *Add .gitignore*, hay *Choose a license*.
4. Bấm **Create repository**.

---

### Bước 5: Đẩy dự án lên GitHub (Push)
Sao chép các lệnh được GitHub cung cấp và chạy trên terminal của bạn:

1. Đặt tên nhánh chính là `main`:
   ```bash
   git branch -M main
   ```

2. Liên kết local repository với GitHub repository (thay URL bằng URL thực tế của bạn):
   ```bash
   git remote add origin https://github.com/TÊN_GITHUB_CỦA_BẠN/TÊN_REPO.git
   ```

3. Đẩy code lên:
   ```bash
   git push -u origin main
   ```

*Khi được hỏi đăng nhập, bạn chọn đăng nhập bằng trình duyệt web (**Sign in with your browser**) để xác thực nhanh nhất.*

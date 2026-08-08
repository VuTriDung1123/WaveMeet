# Hướng dẫn chạy dự án WaveMeet

Đây là hướng dẫn dành riêng cho môi trường phát triển (Local Development) trên máy tính của bạn. Mỗi khi bạn tắt máy và bật lại, hãy thực hiện lần lượt các bước sau:

## 1. Khởi động Docker (Bắt buộc)
WaveMeet sử dụng **Redis** để làm kênh truyền tín hiệu WebSockets (Channel Layer). Do đó, bạn cần có Redis đang chạy.
- Mở phần mềm **Docker Desktop** trên Windows và đợi nó khởi động xong (hiện nút màu xanh lá).
- Mở Terminal (PowerShell) mới và gõ lệnh sau để chạy Redis:
  ```powershell
  docker run -d -p 6379:6379 redis
  ```
*(Nếu Redis đã chạy rồi, lệnh này có thể báo lỗi cổng đã được sử dụng. Không sao cả, bạn cứ bỏ qua bước này)*.

## 2. Kích hoạt môi trường ảo (Virtual Environment)
Đảm bảo bạn đang đứng ở thư mục gốc của dự án (`d:\Personal\WaveMeet`). Gõ lệnh sau vào Terminal để kích hoạt môi trường Python:
```powershell
.\venv\Scripts\activate
```
*(Nếu thành công, bạn sẽ thấy chữ `(venv)` màu xanh ở đầu dòng lệnh)*.

## 3. Chạy Server Django
Sau khi đã kích hoạt `venv` và có Redis, bạn chạy server bằng lệnh:
```powershell
python manage.py runserver
```

## 4. Truy cập trang Web
Mở trình duyệt (Chrome/Edge) và truy cập vào địa chỉ:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---
### Xử lý sự cố (Troubleshooting)
- **Lỗi `port is already allocated` khi chạy Docker**: Tức là máy tính của bạn đã có sẵn Redis đang chạy ngầm rồi. Rất tuyệt, bạn cứ bỏ qua bước 1 và đi tiếp!
- **Lỗi `cannot be loaded because running scripts is disabled on this system`**: Đây là cơ chế bảo mật mặc định của Windows (PowerShell) chặn chạy script. Để sửa lỗi này vĩnh viễn, bạn hãy gõ lệnh sau vào Terminal (chỉ cần làm 1 lần duy nhất):
  ```powershell
  Set-ExecutionPolicy Unrestricted -Scope CurrentUser
  ```
  Sau khi ấn Enter (nếu nó hỏi thì gõ `Y` hoặc `A`), bạn gõ lại lệnh kích hoạt `.\venv\Scripts\activate` là sẽ thành công.
- **Lỗi `Error 111 connecting to 127.0.0.1:6379`**: Tức là Redis chưa chạy. Hãy kiểm tra lại xem Docker Desktop đã bật chưa và chạy lại lệnh ở bước 1.
- **Lỗi `ModuleNotFoundError`**: Tức là bạn chưa kích hoạt môi trường ảo. Hãy chạy lệnh ở bước 2 trước khi chạy `runserver`.
- **Muốn test tính năng Mời ra khỏi phòng / Khóa phòng**: Hãy mở thêm một cửa sổ ẩn danh (Ctrl + Shift + N) để đóng vai trò là một người dùng khác (Guest) rồi copy link phòng sang đó.

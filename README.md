<div align="center">
  <img src="https://img.icons8.com/color/96/000000/video-call--v1.png" alt="WaveMeet Logo"/>
  <h1>🌸 WaveMeet</h1>
  <p><b>Nền tảng Họp trực tuyến P2P (WebRTC & Django Channels)</b></p>
  
  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/Django-5.0+-green.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
  [![WebRTC](https://img.shields.io/badge/WebRTC-P2P-red.svg?logo=webrtc&logoColor=white)](https://webrtc.org/)
  [![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
  [![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
</div>

<br>

> ⚠️ **Lưu ý**: Đây là một Đồ án Cá nhân (Personal Project). Quá trình phát triển tập trung vào tính năng và nghiên cứu công nghệ (WebRTC, WebSockets) thay vì mở rộng quy mô (scalability). Mã nguồn có thể chứa một vài sai sót hoặc chưa được tối ưu hóa tối đa cho môi trường thực tế (production) quy mô lớn. 

---

## 🌟 Tính Năng Nổi Bật (Features)

WaveMeet không chỉ là một ứng dụng gọi video thông thường, mà còn tích hợp các tính năng cao cấp:

- 🎥 **Gọi Video/Audio P2P (WebRTC)**: Truyền tải media độ trễ thấp thông qua kiến trúc Mesh (không tốn tài nguyên máy chủ).
- 🎨 **Giao diện Sakura Glassmorphism**: Thiết kế kính mờ trong suốt (Backdrop Blur), responsive mượt mà từ PC đến Mobile.
- 🪄 **Làm mờ nền bằng AI (Virtual Background)**: Tích hợp thư viện *MediaPipe Selfie Segmentation* xử lý trực tiếp trên trình duyệt.
- 💬 **Trò chuyện & Thả Cảm Xúc (Live Emojis)**: Đồng bộ tin nhắn văn bản và bắn các icon Emojis bay lơ lửng trên màn hình theo thời gian thực (WebSockets).
- 🔤 **Phụ đề trực tiếp (Live Captions)**: Ứng dụng Web Speech API để chuyển đổi giọng nói thành văn bản (Hỗ trợ Tiếng Việt & Tiếng Anh).
- 📁 **Truyền File ngang hàng (P2P File Sharing)**: Chia sẻ file trực tiếp (Dưới 10MB) thông qua RTCDataChannel, hỗ trợ kéo thả tiện lợi.
- 👑 **Quyền Quản Trị (Host Controls)**: Người tạo phòng có quyền Khóa phòng (Lock), Tắt mic toàn bộ (Mute All), hoặc Mời người lạ ra khỏi phòng (Kick).
- 🟢 **Trạng thái Trực tuyến (Presence)**: Danh bạ hiển thị chấm xanh realtime báo hiệu ai đang online trong hệ thống.

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

- **Backend**: Python, Django, Django Channels (WebSockets).
- **Frontend**: HTML5/CSS3, Vanilla JavaScript, Tailwind CSS, FontAwesome.
- **Realtime & Media**: WebRTC (Mesh Topology), MediaRecorder API, SpeechRecognition API, MediaPipe.
- **Database & Broker**: SQLite (Mặc định), Redis (Dùng làm Channel Layer cho WebSockets).
- **Deployment**: Docker, Docker Compose, Daphne (ASGI Server).

---

## 🚀 Hướng Dẫn Cài Đặt (Local Development)

Nếu bạn muốn chạy thử dự án này trên máy tính cá nhân, hãy làm theo các bước sau:

### 1. Yêu cầu hệ thống (Prerequisites)
- Đã cài đặt [Python 3.11+](https://www.python.org/downloads/).
- Đã cài đặt [Docker Desktop](https://www.docker.com/products/docker-desktop/) (cần thiết để chạy Redis).

### 2. Khởi động Redis
WaveMeet sử dụng Redis để quản lý luồng tin nhắn WebSockets. Mở Terminal / PowerShell và chạy:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

### 3. Cài đặt Môi trường (Virtual Environment)
Mở Terminal tại thư mục gốc của dự án (`WaveMeet/`):
```powershell
# 1. Tạo môi trường ảo
python -m venv venv

# 2. Kích hoạt môi trường ảo (Windows PowerShell)
.\venv\Scripts\activate

# (Lưu ý: Nếu bị lỗi Execution Policy, hãy chạy lệnh sau với quyền Admin: 
# Set-ExecutionPolicy Unrestricted -Scope CurrentUser )

# 3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt
```

### 4. Cấu hình Biến Môi Trường (Environment Variables)
- Copy file `.env.example` thành file mới có tên là `.env`.
- (Tùy chọn) Chỉnh sửa lại `SECRET_KEY` hoặc `TURN_URL` nếu bạn có máy chủ TURN riêng.

### 5. Cập nhật Database & Khởi chạy Server
```powershell
# Tạo database SQLite và bảng dữ liệu
python manage.py migrate

# (Tùy chọn) Tạo tài khoản quản trị Admin
python manage.py createsuperuser

# Chạy server ứng dụng
python manage.py runserver
```

Truy cập 👉 **http://127.0.0.1:8000** để bắt đầu sử dụng. Mở 2 tab ẩn danh (Incognito) hoặc 2 trình duyệt khác nhau để test tính năng gọi Video và đồng bộ WebSockets!

---

## 🚢 Hướng Dẫn Triển Khai (Production Deployment)

Dự án đã được thiết lập sẵn `Dockerfile` và `docker-compose.yml`. Để đưa hệ thống lên Server/VPS thực tế:

1. Đảm bảo file `.env` đã tắt chế độ Debug: `DEBUG=False` và chỉnh sửa `ALLOWED_HOSTS=yourdomain.com`.
2. Khởi chạy thông qua Docker Compose:
```bash
docker-compose up -d --build
```
Hệ thống ASGI Server (Daphne) cùng với Redis sẽ tự động chạy ngầm qua cổng `8000`. Bạn chỉ việc cấu hình Nginx Reverse Proxy trỏ vào cổng này.

---

<div align="center">
  <b>Được phát triển với 🌸 và đam mê lập trình.</b>
</div>

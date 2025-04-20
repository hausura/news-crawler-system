#  News Crawler System

## 📌 Giới thiệu

**News Crawler System** là một hệ thống thu thập dữ liệu tin tức tự động, sử dụng Python và MongoDB. Dự án cho phép crawl các đường dẫn bài viết từ nhiều trang tin khác nhau, lưu trữ và quản lý chúng trong MongoDB để phục vụ các tác vụ phân tích dữ liệu như hồi quy,NLP, phân loại, tóm tắt tin tức, v.v.
Nhiệm vụ chính của project này là thu thập --> Trích xuất đặc trưng --> Phân tích, lựa chọn đặc trưng --> Xây dựng mô hình dự đoán.

---

## ⚙️ Các thành phần chính

- **MongoDB**: Lưu trữ thông tin các URL đã được crawl.
- **Python Script (`recursive_crawler.py`)**: Crawler chạy đệ quy từ một URL gốc.
- **Docker**: Dùng để khởi chạy MongoDB container nhanh chóng.
- **requirements.txt**: Danh sách các thư viện Python cần thiết.

---

## 🛠 Hướng dẫn cài đặt và chạy hệ thống

### 1. 🔧 Build Docker Image (nếu có thêm dịch vụ cần chạy)

```bash
docker build -t mongodb-news-main .
```

---

### 2. 🚀 Khởi chạy MongoDB bằng Docker

```bash
docker run -d --name mongodb-news-main \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=admin \
    mongo:latest
```

---

### 3. 🗂 Tạo Database và Collection

Sau khi MongoDB khởi động thành công, thực hiện:

```js
use crawler
db.createCollection("url_crawled")
```

> Hoặc dùng MongoDB Compass để thao tác trực quan.

---

### 4. 📦 Cài đặt thư viện Python

```bash
pip install -r requirements.txt
```

---

### 5. 🕷 Chạy trình thu thập dữ liệu

```bash
python downloader/html/recursive_crawler.py
```

## Hoặc ở đây có thể đổi sang dùng playwright cho 1 số trang SPA nếu muốn!

---

## ✅ Kết quả đầu ra

- Các URL được thu thập sẽ lưu vào collection: `crawler.url_crawled` trong MongoDB.
- Crawler có thể mở rộng thêm để lưu nội dung bài viết, tiêu đề, thời gian đăng, phân tích, v.v.

---

## ⚠️ Ghi chú

- Đảm bảo crawler tuân thủ `robots.txt` và các quy định của trang web.
- Nên đặt thời gian chờ (`sleep`) giữa các request để tránh bị chặn IP.
- Hạn chế độ sâu crawl để tối ưu hiệu suất và tránh vòng lặp.

---

## 📬 Liên hệ

- Mọi ý kiến đóng góp, báo lỗi hoặc đề xuất cải tiến xin vui lòng tạo issue hoặc gửi pull request.
- Hoặc liên hệ với thành viên phụ trách chính Repo Nguyễn Hà Nam.
- Email: hanampy@gmail.com
- Github: hausura

---

> Happy Crawling 🕸️!

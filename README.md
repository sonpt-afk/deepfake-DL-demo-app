# Hướng dẫn cài đặt và sử dụng ứng dụng

## Giới thiệu
Đây là một ứng dụng web để phát hiện khuôn mặt trong ảnh và cung cấp phản hồi về độ chính xác của việc phát hiện. Ứng dụng này sử dụng các thư viện và công cụ như Flask, Chart.js.
Link dataset để test chức năng detect trên web: https://www.kaggle.com/datasets/hamzaboulahia/hardfakevsrealfaces

## Cài đặt

### Yêu cầu hệ thống
- Python 3.x
- pip (Python package installer)

### Các bước cài đặt

1. **Clone repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Tạo và kích hoạt môi trường ảo:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3. **Cài đặt các gói phụ thuộc:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Chạy ứng dụng:**
    ```sh
    python app.py
    ```

## Sử dụng

### Tải lên ảnh
1. Mở trình duyệt và truy cập `http://127.0.0.1:5000`.
2. Tải lên ảnh bằng cách sử dụng giao diện người dùng.

### Phản hồi
1. Sau khi ảnh được tải lên và xử lý, kết quả sẽ được hiển thị.
2. Bạn có thể cung cấp phản hồi về độ chính xác của việc phát hiện khuôn mặt.

### Xem thống kê phản hồi
1. Truy cập `http://127.0.0.1:5000/feedback_summary` để xem tỷ lệ chính xác và tổng số phản hồi.

## Cấu trúc thư mục

- `app.py`: Tập tin chính của ứng dụng.
- `assets/`: Thư mục chứa các tệp CSS, JS và hình ảnh.
- `templates/`: Thư mục chứa các tệp HTML.
- `uploads/`: Thư mục chứa các tệp ảnh đã tải lên.
- `requirements.txt`: Tập tin liệt kê các gói phụ thuộc cần thiết.

## Lỗi thường gặp

- **413 Request Entity Too Large**: Kích thước file quá lớn, vui lòng upload file < 5MB.
- **415 Unsupported Media Type**: Định dạng file không được hỗ trợ, vui lòng upload file jpg/png/jpeg.
- **422 Unprocessable Entity**: Không có khuôn mặt nào trong ảnh, hãy thử ảnh khác nhé.

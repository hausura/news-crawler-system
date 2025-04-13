# Sử dụng MongoDB image chính thức từ Docker Hub
FROM mongo:latest

# Đặt tên người dùng và mật khẩu cho MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=MyStr0ngP@ss

# Mở cổng 27017 để truy cập vào MongoDB từ ngoài container
EXPOSE 27017

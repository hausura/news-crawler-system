# Sử dụng image MongoDB chính thức
FROM mongo:latest

# Cài đặt biến môi trường để khởi tạo MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=MyStr0ngP@ss

# Mở cổng 27017 cho MongoDB
EXPOSE 27017

# Khởi chạy MongoDB
CMD ["mongod"]

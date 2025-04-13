# Base image
FROM python:3.11-slim

# Cài đặt MongoDB client cho Python
RUN pip install --no-cache-dir requests beautifulsoup4 pymongo

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Mở cổng cho MongoDB
EXPOSE 27017

# Thêm script khởi tạo MongoDB nếu cần
RUN mkdir -p /docker-entrypoint-initdb.d && \
    echo 'if (!db.getSiblingDB("crawler").getCollection("url_crawled")) {' > /docker-entrypoint-initdb.d/init-check.js && \
    echo '  db = db.getSiblingDB("crawler");' >> /docker-entrypoint-initdb.d/init-check.js && \
    echo '  db.createCollection("url_crawled");' >> /docker-entrypoint-initdb.d/init-check.js && \
    echo '}' >> /docker-entrypoint-initdb.d/init-check.js

# Command để chạy crawler
CMD ["python", "recursive_crawler.py"]

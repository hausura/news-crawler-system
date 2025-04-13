import re
from pymongo import MongoClient

# Kết nối MongoDB
mongo_uri = "mongodb://admin:admin@localhost:27017/"
client = MongoClient(mongo_uri)
db = client["crawler"]
source_collection = db["url_crawled"]
target_collection = db["article_url"]

# Regex cho bài báo thực sự
article_patterns = [
    r"^https://vnexpress\.net/.+-\d+\.html$",
    r"^https://dantri\.com\.vn/.+-\d+\.htm$",
]

# Tùy chọn: Xóa dữ liệu cũ trong article_url nếu muốn
# target_collection.delete_many({})

# Truy vấn toàn bộ URL đã crawl
all_urls = source_collection.find()

inserted_count = 0

for doc in all_urls:
    url = doc.get("url", "")
    
    for pattern in article_patterns:
        if re.match(pattern, url):
            # Chỉ thêm nếu chưa tồn tại trong target collection
            if not target_collection.find_one({"url": url}):
                target_collection.insert_one({"url": url})
                inserted_count += 1
            break  # Dừng kiểm tra nếu đã match một pattern

print(f"[✓] Đã lọc và thêm {inserted_count} bài báo mới vào collection 'article_url'.")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from pymongo import MongoClient
import time


# Cấu hình MongoDB
mongo_uri = "mongodb://admin:admin@mongodb-news:27017/"
client = MongoClient(mongo_uri)
db = client["crawler"]
collection = db["url_crawled"]

# Hàm cào đệ quy
def crawl_url(url, domain, max_depth=3, current_depth=0, visited=set()):
    if current_depth > max_depth:
        return

    if url in visited:
        return
    visited.add(url)

    # Nếu đã trong DB thì bỏ qua
    if collection.count_documents({"url": url}, limit=1) > 0:
        return

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Lỗi khi tải URL {url}: {e}")
        return

    # Lưu vào DB
    collection.insert_one({
        "url": url,
        "depth": current_depth
    })
    print(f"[+] Lưu URL ({current_depth}): {url}")

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)

        # Cùng domain và không phải chính nó
        if parsed.netloc == domain:
            crawl_url(full_url, domain, max_depth, current_depth + 1, visited)

# Gọi hàm chính
if __name__ == "__main__":
    seed_url = "https://vnexpress.net/"
    parsed = urlparse(seed_url)
    domain = parsed.netloc

    crawl_url(seed_url, domain, max_depth=3)

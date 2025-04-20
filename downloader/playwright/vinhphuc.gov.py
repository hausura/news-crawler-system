import asyncio
from playwright.async_api import async_playwright
from pymongo import MongoClient

# Cấu hình MongoDB
mongo_uri = "mongodb://admin:admin@localhost:27017/"
client = MongoClient(mongo_uri)
db = client["crawler"]
collection = db["url_crawled"]

found_url = set()

async def process_page(page):
    # Scroll để load thêm nội dung
    for _ in range(6):
        await page.evaluate("window.scrollBy(0, window.innerHeight);")
        await asyncio.sleep(4)

    related_links = await page.query_selector_all('a')
    for link in related_links:
        href = await link.get_attribute('href')
        text = await link.inner_text()

        if href and '/ct/cms' in href and text.strip():
            if not collection.find_one({"url": "https://vinhphuc.gov.vn"+href}):
                collection.insert_one({"url": "https://vinhphuc.gov.vn"+href})
                found_url.add(href)
                print("✅ Tìm thấy URL:", href)

async def crawl_paginated_pages(playwright, start_url, max_pages=1473):
    browser = await playwright.chromium.launch(
        headless=False,
        proxy={"server": "http://192.168.104.52:8136"}
    )
    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        extra_http_headers={
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    )
    page = await context.new_page()

    try:
        print(f"🔗 Đang truy cập trang: {start_url}")
        await page.goto(start_url, timeout=6000)
        await asyncio.sleep(3)
        await process_page(page)

        for page_num in range(2, max_pages + 1):
            print(f"🔄 Đang xử lý trang số: {page_num}")

            try:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

                clicked = await page.evaluate(f'''
                    (() => {{
                        const links = Array.from(document.querySelectorAll('a'));
                        const target = links.find(el => el.textContent.trim() === "{page_num}");
                        if (target) {{
                            target.scrollIntoView();
                            target.click();
                            return true;
                        }}
                        return false;
                    }})()
                ''')

                if not clicked:
                    print(f"⚠️ Không tìm thấy nút trang {page_num}")
                    continue

                await asyncio.sleep(3)
                await page.wait_for_load_state("networkidle")
                await process_page(page)

            except Exception as e:
                print(f"⚠️ Lỗi khi xử lý trang {page_num}: {e}")


    except Exception as e:
        print(f"❌ Lỗi khi mở trang chính: {e}")

    finally:
        await browser.close()

async def main():
    start_url = "https://vinhphuc.gov.vn/ct/cms/tintuc/Lists/ThoiSuChinhTri/View_Detail.aspx?ItemID=13820"
    if not collection.find_one({"url": start_url}):
        collection.insert_one({"url": start_url})
    found_url.add(start_url)

    async with async_playwright() as playwright:
        await crawl_paginated_pages(playwright, start_url)

if __name__ == "__main__":
    asyncio.run(main())

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Chỉ định đường dẫn tĩnh cho thư mục assets
app.mount("/assets", StaticFiles(directory="../front-end/assets"), name="assets")

# MongoDB setup
client = MongoClient("mongodb://admin:admin@localhost:27017/")
db = client["crawler"]
collection = db["article_url"]

class ArticleModel(BaseModel):
    url: str

class ArticleUpdateModel(BaseModel):
    old_url: str
    new_url: str

@app.get("/articles")
def get_articles():
    articles = collection.find({}, {"_id": 0, "url": 1})
    return list(articles)

@app.post("/articles")
def add_article(article: ArticleModel):
    if collection.find_one({"url": article.url}):
        raise HTTPException(status_code=400, detail="URL đã tồn tại.")
    collection.insert_one({"url": article.url})
    return {"message": "Đã thêm bài báo."}

@app.put("/articles")
def update_article(article: ArticleUpdateModel):
    result = collection.update_one({"url": article.old_url}, {"$set": {"url": article.new_url}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy URL để cập nhật.")
    return {"message": "Đã cập nhật URL."}

@app.delete("/articles")
def delete_article(article: ArticleModel):
    result = collection.delete_one({"url": article.url})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy URL để xoá.")
    return {"message": "Đã xoá bài báo."}

@app.get("/show")
def serve_frontend():
    return FileResponse(Path("../front-end/articles.html"))
@app.get("/")
def serve_frontend():
    return FileResponse(Path("../front-end/home.html"))

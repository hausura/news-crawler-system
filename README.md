﻿# News Crawler System

### Build Docker Image

---

```bash
docker build -t mongodb-news-main .
```

### Run MongoDB Container

---

```bash
docker run -d --name mongodb-news-main -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo:latest


```

### Create Databases and Collections

---

1. Create a database named `crawler`.
2. Inside `crawler`, create a collection named `url_crawled`.

### Install Required Libraries

---

```bash
pip install -r requirements.txt
```

### Run the Python Crawler Script

---

```bash
python recursive_crawler.py
```

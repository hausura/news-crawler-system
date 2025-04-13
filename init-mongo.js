// init-mongo.js
db = db.getSiblingDB("crawler");
if (!db.getCollectionNames().includes("url_crawled")) {
  db.createCollection("url_crawled");
}

#!/usr/bin/env python3
"""
    script that provides some stats about Nginx logs stored in MongoDB:
    Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the
method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
one line with the number of documents with:
method=GET
path=/status
"""

import pymongo
from pymongo import MongoClient


def log_nginx_stats(mongo_collection):
    """"overview of stats about nginx logs"""
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    numb_gets = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{numb_gets} status check")


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_nginx_stats(mongo_collection)

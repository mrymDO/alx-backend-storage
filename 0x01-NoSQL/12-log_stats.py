#!/usr/bin/env python3
"""provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient



def nginx_logs_stats():
    """stats about Nginx logs"""
    client = MongoClient('mongodb://localhost:27017')
    db = client.logs
    nginx_collection = db.nginx

    total_logs = nginx_collection.count_documents({})

    print(f"{total_logs} logs")


    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")



    count_status_requests = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"\t{count_status_requests} status check")

    client.close()

if __name__ == "__main__":
    nginx_logs_stats()

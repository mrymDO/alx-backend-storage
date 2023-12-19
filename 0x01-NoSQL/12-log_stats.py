#!/usr/bin/env python3
"""provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient



def nginx_logs_stats(mongo_collection):
    """stats about Nginx logs"""

    total_logs = mongo_collection.count_documents({})

    print(f"{total_logs} logs")


    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")



    count_status_requests = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{count_status_requests} status check")



if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx
    nginx_logs_stats(collection)

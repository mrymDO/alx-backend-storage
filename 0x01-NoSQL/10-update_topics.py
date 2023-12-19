#!/usr/bin/env python3
"""update function"""


def update_topics(mongo_collection, name, topics):
    """ changes topic of document based on the name"""
    return mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}});

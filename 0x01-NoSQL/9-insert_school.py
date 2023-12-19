#!/usr/bin/env python3
""" Inserts new document"""


def insert_school(mongo_collection, **kwargs):
    """insert new document in a collection based on kwargs"""
    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id

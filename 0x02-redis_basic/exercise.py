#!/usr/bin/env python3
"""write strings"""

import redis
import uuid


class Cache:
    """store instance od Redis"""
    def __init__(self):
        """Initialize the Cache Creates Redis client and clears the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: any) -> str:
        """store data in the cache and return a unique key"""
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key
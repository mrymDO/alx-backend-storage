#!/usr/bin/env python3
"""write strings"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps



def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""
    counts = {}

    @wraps(method)
    def counting_method(self, *args, **kwargs):
        """counting method"""
        key = method.__qualname__
        self._redis.incr(key)
        result = method(self, *args, **kwargs)
        return result

    return counting_method



class Cache:
    """store instance od Redis"""
    def __init__(self):
        """Initialize the Cache Creates Redis client and clears the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in the cache and return a unique key"""
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """retrieve data from the cache based on a key"""
        data = self._redis.get(key)

        if data and fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> int:
        """retrieve data as a string from the cache"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """retrieve data as an integer from the cache"""
        return self.get(key, int)

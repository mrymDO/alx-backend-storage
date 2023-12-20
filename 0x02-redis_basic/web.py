#!/usr/bin/env python3
"""web cache and tracker"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def track_and_cache(expiration_time: int = 10) -> Callable:
    """track and cache"""
    def decorator(func: Callable) -> Callable:
        """decorator"""
        @wraps(func)
        def wrapper(url: str) -> str:
            """track num of access to a particular URL"""
            access_count_key = f"count:{url}"
            redis_client.incr(access_count_key)

            cache_key = f"cache:{url}"
            cached_result = redis_client.get(cache_key)

            if cached_result:
                return cached_result.decode('utf-8')

            result = func(url)
            redis_client.setex(cache_key, expiration_time, result)

            return result

        return wrapper
    return decorator


def get_page(url: str) -> str:
    """get a page"""
    response = requests.get(url)
    return response.text

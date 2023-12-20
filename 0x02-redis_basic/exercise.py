#!/usr/bin/env python3
"""write strings"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps



def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""

    @wraps(method)
    def counting_method(self, *args, **kwargs):
        """counting method"""
        key = method.__qualname__
        self._redis.incr(key)
        result = method(self, *args, **kwargs)
        return result

    return counting_method


def call_history(method: Callable) -> Callable:
    """Decorator to store history of inputs and outputs of a function"""
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_list_key = f"{method.__qualname__}:inputs"
        output_list_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_list_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_list_key, str(result))

        return result

    return wrapper


def replay(method: Callable, cache):
    """Display the history of calls for a particular function"""
    method_name = method.__qualname__
    input_list_key = f"{method_name}:inputs"
    output_list_key = f"{method_name}:outputs"

    input_history = cache._redis.lrange(input_list_key, 0,  -1)
    output_history = cache._redis.lrange(output_list_key, 0, -1)

    print(f"{method_name} was called {len(input_history)} times:")

    for inputs, output in zip(input_history, output_history):
        print(f"{method_name}(*{inputs.decode('utf-8')} -> {output.decode('utf-8')}")



class Cache:
    """store instance od Redis"""
    def __init__(self):
        """Initialize the Cache Creates Redis client and clears the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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





# Example Usage:
cache = Cache()

# Perform some store operations to generate history
cache.store("foo")
cache.store("bar")
cache.store(42)

# Call the replay function for the store method
replay(cache.store, cache)

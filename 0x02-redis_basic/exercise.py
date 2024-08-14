#!/usr/bin/env python3
"""
    module Cache class. In the __init__ method
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """returns a Callable"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """class cache"""
    def __init__(self):
        """intialize the cache class with redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in redis with a random key

        Args:
            data (Union[str, bytes, int, float])

        Returns:
            str: the key under which the data is stored
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """convert data back to desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get with correct
            conversion function
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get with correct
            conversion function
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value

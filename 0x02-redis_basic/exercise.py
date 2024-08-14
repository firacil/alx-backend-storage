#!/usr/bin/env python3
"""
    module Cache class. In the __init__ method
"""

import redis
import uuid
from typing import Union


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

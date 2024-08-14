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

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper of decorated function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """display the history of calls"""
    r = redis.Redis()
    fname = fn.__qualname__
    value = r.get(fname)
    try:
        value = int(value.decode("utd-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(fname, value))
    inputs = r.lrange("{}:inputs".format(fname), 0, -1)

    outputs = r.lrange("{}:outputs".format(fname), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print("{}(*{}) -> {}".format(fname, input, output))


class Cache:
    """class cache"""
    def __init__(self):
        """intialize the cache class with redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

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

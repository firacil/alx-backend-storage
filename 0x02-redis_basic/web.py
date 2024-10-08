#!/usr/bin/env python3
"""
    In this tasks, we will implement a get_page function
    (prototype: def get_page(url: str) -> str:)
    The core of the function is very simple.
    It uses the requests module to obtain the HTML content
    of a particular URL and returns it.
    Start in a new file named web.py and do not reuse
    the code written in exercise.py

    Inside get_page track how many times a particular URL
    was accessed in the key "count:{url}" and cache the
    result with an expiration time of 10 seconds.

    Tip: Use http://slowwly.robertomurray.co.uk to
    simulate a slow response and test your caching.

    Bonus: implement this use case with decorators.
"""

import redis
import requests
from functools import wraps
from typing import Callable

r = redis.Redis()


def url_access_count(method: Callable) -> Callable:
    """decorator for get_page"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """wrapper function"""
        # increment access count
        count_key = f"count:{url}"
        r.incr(count_key)

        # checking if the page is cached
        cached_val = r.get(url)
        if cached_val:
            return cached_val.decode("utf-8")

        # if not cached, fetch the page
        page_content = method(url)

        # cache the result with an expiration time of 10s
        r.setex(url, 10, page_content)

        return page_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """ get html content of particular"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')

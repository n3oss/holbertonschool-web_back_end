#!/usr/bin/env python3
"""FIFO caching """

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """cach with LIFO last in first out"""

    def __init__(self):
        """starts the LIFO with the lifo policy"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """add the itam in a chace"""
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = self.order.pop()
            del self.cache_data[last_key]
            print("DISCARD: {}".format(last_key))
        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """return the key"""
        if key is None:
            return None
        return self.cache_data.get(key)

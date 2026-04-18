#!/usr/bin/env python3
"""FIFO caching """

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """caching with FIFO in python"""

    def __init__(self):
        """starts the FIFO cache with FIFO policy"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """add an item to the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            return

        self.cache_data[key] = item
        self.order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = self.order.pop(0)
            del self.cache_data[first_key]
            print("DISCARD: {}".format(first_key))

    def get(self, key):
        """return the key"""
        if key is None:
            return None
        return self.cache_data.get(key)

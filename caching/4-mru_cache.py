#!/usr/bin/env python3
"""MRU caching in python"""

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """MRU caching in python"""
    def __init__(self):
        """starts the MRU cache with its policy"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add or update an item in the cache using MRU policy."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.order.remove(key)
            self.order.append(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            used_key = self.order.pop()
            del self.cache_data[used_key]
            print("DISCARD: {}".format(used_key))

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """Return the value linked to key and update recent usage."""
        if key is None or key not in self.cache_data:
            return None

        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]

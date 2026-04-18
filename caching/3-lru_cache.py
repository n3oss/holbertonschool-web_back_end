#!/usr/bin/env python3
"""LRU caching in python"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """LRU caching in python"""
    def __init__(self):
        """starts the LRU cache with its policy"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add or update an item in the cache using LRU policy."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.order.remove(key)
            self.order.append(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            notused_key = self.order.pop(0)
            del self.cache_data[notused_key]
            print("DISCARD: {}".format(notused_key))

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """Return the value linked to key and update recent usage."""
        if key is None or key not in self.cache_data:
            return None

        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]

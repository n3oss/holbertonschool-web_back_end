#!/usr/bin/env python3

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):

    def put(self, key, item):
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):

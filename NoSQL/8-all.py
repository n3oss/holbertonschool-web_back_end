#!/usr/bin/env python3
"""thsi is dacument"""


def list_all(mongo_collection):
    """this is document"""
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())

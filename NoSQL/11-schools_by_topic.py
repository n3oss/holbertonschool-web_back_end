#!/usr/bin/env python3
"""this is doc"""


def schools_by_topic(mongo_collection, topic):
    """this is doc"""
    return list(mongo_collection.find({"topics": topic}))

#!/usr/bin/env python3
"""
    Python function that lists all documents in a collection
    Prototype: def list_all(mongo_collection):
    Return an empty list if no document in the collection
    mongo_collection will be the pymongo collection object
"""

import pymongo


def list_all(mongo_collection):
    """lists all documents in a collection"""
    if not mongo_collection:
        return []
    lists = mongo_collection.find()
    return [doc for doc in lists]

#!/usr/bin/env python
"""
    functions_cache.engines.mongo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ``mongo`` cache engine
"""
from .base import BaseCache
from .storage.mongodict import MongoDict, MongoPickleDict


class MongoCache(BaseCache):
    """``mongo`` cache engine."""

    def __init__(self, db_name='functions-cache', **options):
        """
        :param db_name: database name (default: ``'functions-cache'``)
        :param connection: (optional) ``pymongo.Connection``
        """
        super().__init__(**options)
        self.responses = MongoPickleDict(db_name, 'responses', options.get('connection'))
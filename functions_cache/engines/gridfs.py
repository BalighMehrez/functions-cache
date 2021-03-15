#!/usr/bin/env python
"""
    functions_cache.engines.gridfs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ``gridfs`` cache engine

    Use MongoDB GridFS to support documents greater than 16MB.

    Usage:
        functions_cache.install_cache(engine='gridfs')

    Or:
        from pymongo import MongoClient
        functions_cache.install_cache(engine='gridfs', connection=MongoClient('another-host.local'))
"""
from .base import BaseCache
from .storage.gridfspickledict import GridFSPickleDict
from .storage.mongodict import MongoDict


class GridFSCache(BaseCache):
    """``gridfs`` cache engine."""

    def __init__(self, db_name, **options):
        """
        :param db_name: database name
        :param connection: (optional) ``pymongo.Connection``
        """
        super().__init__(**options)
        self.responses = GridFSPickleDict(db_name, options.get('connection'))

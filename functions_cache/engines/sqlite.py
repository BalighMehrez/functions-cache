#!/usr/bin/env python
"""
    functions_cache.engines.sqlite
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ``sqlite3`` cache engine
"""
from .base import BaseCache
from .storage.dbdict import DbDict, DbPickleDict


class DbCache(BaseCache):
    """sqlite cache engine.

    Reading is fast, saving is a bit slower. It can store big amount of data
    with low memory usage.
    """

    def __init__(self, location='cache', fast_save=False, extension='.sqlite', **options):
        """
        :param location: database filename prefix (default: ``'cache'``)
        :param fast_save: Speedup cache saving up to 50 times but with possibility of data loss.
                          See :ref:`engines.DbDict <engines_dbdict>` for more info
        :param extension: extension for filename (default: ``'.sqlite'``)
        """
        super().__init__(**options)
        self.responses = DbPickleDict(str(location) + extension, 'responses', fast_save=fast_save)

#!/usr/bin/env python
"""
    functions_cache.engines.redis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ``redis`` cache engine
"""
from .base import BaseCache
from .storage.redisdict import RedisDict


class RedisCache(BaseCache):
    """``redis`` cache engine."""

    def __init__(self, namespace='functions-cache', **options):
        """
        :param namespace: redis namespace (default: ``'functions-cache'``)
        :param connection: (optional) ``redis.StrictRedis``
        """
        super().__init__(**options)
        self.responses = RedisDict(namespace, 'responses', options.get('connection'))

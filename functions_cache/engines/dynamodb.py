#!/usr/bin/env python
"""
    functions_cache.engines.dynamodb
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ``dynamodb`` cache engine
"""
from .base import BaseCache
from .storage.dynamodbdict import DynamoDbDict


class DynamoDbCache(BaseCache):
    """``dynamodb`` cache engine."""

    def __init__(self, table_name='functions-cache', **options):
        """
        :param namespace: dynamodb table name (default: ``'functions-cache'``)
        :param connection: (optional) ``boto3.resource('dynamodb')``
        """
        super().__init__(**options)
        self.responses = DynamoDbDict(
            table_name,
            'responses',
            options.get('connection'),
            options.get('endpont_url'),
            options.get('region_name'),
            options.get('read_capacity_units'),
            options.get('write_capacity_units'),
        )

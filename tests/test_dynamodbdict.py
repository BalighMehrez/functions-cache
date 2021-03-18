#!/usr/bin/env python
import os
import pytest
import unittest

from tests.test_custom_dict import BaseCustomDictTestCase

pytestmark = pytest.mark.skip(reason='Integration test database is not set up')
try:
    from functions_cache.engines.storage.dynamodbdict import DynamoDbDict
except ImportError:
    print("DynamoDb not installed")
else:

    class WrapDynamoDbDict(DynamoDbDict):
        def __init__(self, namespace, collection_name='dynamodb_dict_data', **options):
            options['endpoint_url'] = (
                os.getenv('DYNAMODB_ENDPOINT_URL',"http://localhost:8000")
            )
            super(WrapDynamoDbDict, self).__init__(namespace, collection_name, **options)

    class DynamoDbDictTestCase(BaseCustomDictTestCase, unittest.TestCase):
        dict_class = WrapDynamoDbDict
        pickled_dict_class = WrapDynamoDbDict

    if __name__ == '__main__':
        unittest.main()

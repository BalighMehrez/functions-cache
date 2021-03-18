#!/usr/bin/env python
import unittest

from tests.test_custom_dict import BaseCustomDictTestCase

try:
    from functions_cache.engines.storage.mongodict import MongoDict, MongoPickleDict
except ImportError:
    print("pymongo not installed")
else:

    class MongoDictTestCase(BaseCustomDictTestCase, unittest.TestCase):
        dict_class = MongoDict
        pickled_dict_class = MongoPickleDict

    if __name__ == '__main__':
        unittest.main()

#!/usr/bin/env python
import unittest
from datetime import datetime


from functions_cache import cache_it,config_engine,engines

CACHE_ENGINE = engines.create_engine('memory','test',{}) 



@cache_it(custom_engine=CACHE_ENGINE,is_static=True)
def fab_cached(n):
    if n < 2:
        return n
    else:
        return fab_cached(n-2)+fab_cached(n-1)

def fab(n):
    if n < 2:
        return n
    else:
        return fab(n-2)+fab(n-1)

class CacheTestCase(unittest.TestCase):

    def test_cache_it(self):
        
        t1 = datetime.now()
        res1 = fab(20)
        t2 = datetime.now()
        duration1 = t2-t1
        t3 = datetime.now()
        res2 = fab_cached(20)
        t4 = datetime.now()
        duration2 = t4-t3
        self.assertEqual(res1,res2)
        self.assertGreater(duration1 , duration2)


if __name__ == '__main__':
    unittest.main()

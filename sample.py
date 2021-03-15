
import random
import time
from functions_cache import cache_it
import datetime

my_cache = {}


@cache_it(as_daemon=True)
def sample_func(a, b):
    time.sleep(2)
    result = {"a": a,"b": b, "random": random.random()}
    return result
    
def fab(n):
    if n < 2:
        return n
    else:
        return fab(n-2)+fab(n-1)

@cache_it(as_daemon=True)
def fab_cached(n):
    if n < 2:
        return n
    else:
        return fab_cached(n-2)+fab_cached(n-1)

if __name__ == "__main__":
    t1 = datetime.datetime.now()
    print(fab_cached(25))
    t2 = datetime.datetime.now()
    print(t2-t1)
    t3 = datetime.datetime.now()
    print(fab(25))
    t4 = datetime.datetime.now()
    print(t4-t3)

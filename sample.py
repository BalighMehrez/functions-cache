import functools
import random
import threading
import time
from threading import Thread
from typing import Match

my_cache = {}


def cach_it(_func=None, *, as_daemon=False):

    def decorator_cache_it(func):

        @functools.wraps(func)
        def wrapper_cach_it(*args, **kwargs):
            key = (func.__name__, args, hash(tuple(sorted(kwargs))))
            if key in my_cache:
                result = my_cache[key]

                def threaded_func():
                    my_cache[key] = func(*args, **kwargs)

                t = threading.Thread(target=threaded_func, daemon=as_daemon)
                t.start()

            else:
                result = func(*args, **kwargs)
                my_cache[key] = result
            return result
        return wrapper_cach_it

    if _func is None:
        return decorator_cache_it
    else:
        return decorator_cache_it(_func)


@cach_it(as_daemon=True)
def sample_func(a, b):
    time.sleep(2)
    return (a + b) * random.random()


if __name__ == "__main__":
    for i in range(10):
        print(sample_func(5, 5))

        time.sleep(1)

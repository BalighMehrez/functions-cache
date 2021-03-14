import functools
import threading
from threading import Thread

my_cache = {}

def cache_it(_func=None, *, as_daemon=False):

    def decorator_cache_it(func):

        @functools.wraps(func)
        def wrapper_cache_it(*args, **kwargs):
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
        return wrapper_cache_it

    if _func is None:
        return decorator_cache_it
    else:
        return decorator_cache_it(_func)

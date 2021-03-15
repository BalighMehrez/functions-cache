import functools
import threading
from threading import Thread
import functions_cache.engines as engines
from functions_cache.function_identifier import FunctionIdentifier
global my_cache
my_cache = engines.create_engine('sqlite','functions-cache',{})

# def config_engine():
#     my_cache = engines.create_engine()

def cache_it(_func=None, *, as_daemon=False):

    def decorator_cache_it(func):

        @functools.wraps(func)
        def wrapper_cache_it(*args, **kwargs):
            identifier = FunctionIdentifier(func.__name__,args,kwargs)
            key = my_cache.create_key(identifier)
            if my_cache.has_key(key):
                result = my_cache.get_response_and_time(key)[0]

                def threaded_func():
                    my_cache.save_response(key,func(*args, **kwargs))

                t = threading.Thread(target=threaded_func, daemon=as_daemon)
                t.start()

            else:
                result = func(*args, **kwargs)
                my_cache.save_response(key,result)
            return result
        return wrapper_cache_it

    if _func is None:
        return decorator_cache_it
    else:
        return decorator_cache_it(_func)

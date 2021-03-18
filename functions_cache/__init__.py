import functools
import threading
from threading import Thread
import functions_cache.engines as engines
from functions_cache.function_identifier import FunctionIdentifier
_default_engine = engines.create_engine('sqlite','functions-cache',{})
threadLimiter = threading.BoundedSemaphore(4)

def config_engine(engine):
    global _default_engine
    _default_engine = engine

def cache_it(_func=None, *, as_daemon=True, is_static=False, custom_engine=None):
    global _default_engine
    custom_engine = _default_engine if custom_engine is None else custom_engine

    def decorator_cache_it(func):

        @functools.wraps(func)
        def wrapper_cache_it(*args, **kwargs):
            identifier = FunctionIdentifier(func.__name__,args,kwargs)
            key = custom_engine.create_key(identifier)
            if custom_engine.has_key(key):
                result = custom_engine.get_response_and_time(key)[0]

                if not is_static:

                    def threaded_func():
                        threadLimiter.acquire()
                        try:
                            custom_engine.save_response(key,func(*args, **kwargs))
                        finally:
                            threadLimiter.release()
                        

                    t = threading.Thread(target=threaded_func, daemon=as_daemon)
                    t.start()

            else:
                result = func(*args, **kwargs)
                custom_engine.save_response(key,result)
            return result
        return wrapper_cache_it

    if _func is None:
        return decorator_cache_it
    else:
        return decorator_cache_it(_func)

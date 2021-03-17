# functions cache

This library is inspired by requests-cache <https://github.com/reclosedev/requests-cache> and the whole engines code has been copied and modified from there.

this library provide a decorator that can be used to decorate your functions to be cached.

The main feature that diffentiate this library is that it will auto refresh the cache in a background thread so your cache will be kept fresh.

## Sample code
```python
from functions_cache import cache_it
import datetime



@cache_it
def fab_cached(n):
    if n < 2:
        return n
    else:
        return fab_cached(n-2)+fab_cached(n-1)

if __name__ == "__main__":
    t1 = datetime.datetime.now()
    print(fab_cached(100))
    t2 = datetime.datetime.now()
    print(t2-t1)
    t3 = datetime.datetime.now()
    print(fab_cached(100))
    t4 = datetime.datetime.now()
    print(t4-t3)
    
```
and the output
```
354224848179261915075
0:00:03.366472
354224848179261915075
0:00:00.014370
```

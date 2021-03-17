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

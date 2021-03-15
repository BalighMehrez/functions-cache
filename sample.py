
import random
import time
from functions_cache import cache_it

my_cache = {}


@cache_it(as_daemon=True)
def sample_func(a, b):
    time.sleep(2)
    result = {"a": a,"b": b, "random": random.random()}
    return result


if __name__ == "__main__":
    for i in range(10):
        for j in range(4):
            print(sample_func(i, i))
            time.sleep(1)

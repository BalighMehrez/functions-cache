
import random
import time
from functions_cache import cache_it

my_cache = {}


@cache_it(as_daemon=True)
def sample_func(a, b):
    time.sleep(2)
    return (a + b) * random.random()


if __name__ == "__main__":
    for i in range(10):
        print(sample_func(5, 5))

        time.sleep(1)

from collections import OrderedDict
import json

cache = OrderedDict()


#class lru_cache:
def lru_cache(capacity):
    size = capacity

    def extracting_func(func):
        if (str(func.__name__) == "put"):

            def wrapper(key, value):
                if key not in cache:
                    if len(cache) >= size:
                        cache.popitem(last=False)
                else:
                    cache.move_to_end(key)
                cache[key] = str(value)
                return func(key, value)

            return wrapper

        if (str(func.__name__) == "get"):

            def wrapper(key):
                if key not in cache:
                    return -1
                else:
                    cache.move_to_end(key)
                    return cache[key]
                return func(key)

            return wrapper

        if (str(func.__name__) == "delete"):

            def wrapper(key):
                if key in cache:
                    del cache[key]
                return func(key)

            return wrapper

    return extracting_func

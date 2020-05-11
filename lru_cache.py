from collections import OrderedDict
import json

cache = OrderedDict()
size = int()


#class lru_cache:
def lru_cache(capacity):
    size = capacity

    def extracting_func(func):
        def wrapper(key):
            if key in cache:
                cache.move_to_end(key)
                """print("[cache-hit] " + str(func.__name__) + "(" + str(key) +
                      ") -> " + str(cache[key]))"""
                #print(str(cache[key]))
                return cache[key]
            else:
                item = func(key)
                if len(cache) == size:
                    cache.popitem(last=False)
                """print("[Not-in-cache] " + str(func.__name__) + "(" + str(key) +
                      ") -> " + str(item))"""
                cache[key] = item
                return item

        return wrapper

    return extracting_func

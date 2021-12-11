# SYSTEM
from functools import wraps
from time import perf_counter


def timed(fn):
    
    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        time_length = end - start

        # print('{0} ran for {1:.6f}s'.format(fn.__name__, time_length))

        return fn(*args, **{'timer': time_length}, **kwargs)
    
    return inner
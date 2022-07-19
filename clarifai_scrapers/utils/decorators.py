# SYSTEM IMPORTS
from functools import wraps
from time import perf_counter
from itertools import islice
from typing import Generator

# errors
from clarifai_scrapers.errors import PageSizeLimitExceeded


def timed(fn):
    """
    Decorator that times function 

    Args:
        fn (function): Parent function

    Returns:
        (function): Parent function
    """
    
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start       = perf_counter()
        result      = fn(*args, **kwargs)
        end         = perf_counter()
        time_length = end - start

        print('{0} ran for {1:.6f}s'.format(fn.__name__, time_length))

        return fn(*args, **{'timer': time_length}, **kwargs)
    
    return wrapper



def paginate(page_size: int) -> Generator:
    """
    Chunks a list into multiple tuples

    Args:
        page_size (int): Size of each chunks
    """

    def inner(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            results   = fn(*args, **kwargs)
            i         = iter(results)

            while True:
                page = tuple(islice(i, 0, page_size))
                if len(page):
                    yield page
                else:
                    return
        
        return wrapper
    
    return inner



def add_all_args_to_self(fn):
    """
    All args passed to function are added to self

    Args:
        fn (function)

    Returns:
        (function): Parent function and fed self
    """

    @wraps(fn)
    def inner(self, *args, **kwargs):

        for param in kwargs.items():
            if param[0] != 'self': setattr(self, param[0], param[1])  

        return fn(self, *args, **kwargs)
    
    return inner



def page_size_limitation_if_bytes_requested(fn):

    @wraps(fn)
    def inner(self, *args, **kwargs):

        bool_user_requested_bytes_to_be_returned = self.also_return_bytes
        per_page = kwargs.get('per_page')

        if per_page > 30 and bool_user_requested_bytes_to_be_returned:
            raise PageSizeLimitExceeded('Bytes can only be returned when page size is <= 30')

        return fn(self, *args, **kwargs)
    
    return inner
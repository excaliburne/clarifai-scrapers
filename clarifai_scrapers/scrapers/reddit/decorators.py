# SYSTEM
from functools import wraps
from operator import itemgetter


def reset_last_utc(fn):
    
    @wraps(fn)
    def inner(self, *args, **kwargs):

        page = kwargs.get('page') or 1

        if page == 1: self.last_utc = None

        return fn(self, *args, **kwargs)
    
    return inner
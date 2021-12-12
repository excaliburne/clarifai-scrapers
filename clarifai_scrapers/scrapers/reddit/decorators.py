# SYSTEM
from functools import wraps
from operator import itemgetter


def reset_last_utc(fn):
    
    @wraps(fn)
    def inner(self, *args, **kwargs):

        page_num = itemgetter('page_num')(kwargs)

        if page_num == 1: self.last_utc = None

        return fn(self, *args, **kwargs)
    
    return inner
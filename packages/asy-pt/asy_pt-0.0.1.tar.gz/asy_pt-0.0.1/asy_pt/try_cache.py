# -*- coding: utf-8 -*-
# @Time    : 2024/12/24 14:14
# @Author  : xuwei
# @FileName: try_cache.py
# @Software: PyCharm



from functools import wraps
from .logger import log

def catch_error_log(func):
    @wraps(func)
    def try_catch(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # print("%s: %s" % (func.__name__, e))
            log.exception("%s: %s" % (func.__name__, e))
            return None

    return try_catch
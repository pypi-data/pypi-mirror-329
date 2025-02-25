import inspect
from functools import wraps


def oauthtoken(fn):
    if not inspect.isfunction(fn):
        raise TypeError("The oauthtoken decorator can only be applied to functions.")

    fn.__oauthtoken__ = True
    return wraps(fn)(fn)

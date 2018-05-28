from functools import wraps
from flask import abort, g


def auth_required(f):
    """ Provides a wrapper for views to enforce login requirements """
    @wraps(f)
    def auth_required_decorator(*args, **kwargs):
        if g.user is None:
            abort(401)
        return f(*args, **kwargs)
    return auth_required_decorator

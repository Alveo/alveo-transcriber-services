from functools import wraps
from flask import abort, g


def auth_required(f):
    """ Provides a decorator/wrapper to enforce authentication as a requirement

    Will abort via flask with a 401 error if the user is not authenticated when
    passing through the decorator.

    Args:
        f: Function to wrap

    Returns:
        Decorated function

    """
    @wraps(f)
    def auth_required_decorator(*args, **kwargs):
        if g.user is None:
            abort(401)
        return f(*args, **kwargs)
    return auth_required_decorator

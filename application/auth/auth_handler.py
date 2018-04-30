from functools import wraps
from flask import abort, g

from application import auth_handlers

class register_auth_handler(object):
    def __init__(self, name):
        self.auth_name = name
        self.register();

    def register(self):
        auth_handlers.append(self)

    def __call__(self, function):
        self.authenticate = function

def auth_required(f):
    """ Provides a wrapper for views to enforce login requirements """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


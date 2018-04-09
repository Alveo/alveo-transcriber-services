from functools import wraps
from flask import abort, g, request

from application import app, login_manager
from application.users.model import User

def auth_required(f):
    """ Provides a wrapper for views to enforce login requirements """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

@login_manager.request_loader
def load_user_from_request(request):
    """ Authenticates users via API key from request arguments or request header """

    # Authenticate via arguments first if possible
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # If that didn't work, try headers
    api_key = request.headers.get('Api-Key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # User couldn't be set
    return None

@app.before_request
def before_request():
    """ Attempt to authenticate the user on each request """
    g.user = load_user_from_request(request)

from flask import g, request, abort

from application import app, login_manager
from application.misc.events import get_handler_for, MODULE_PATHS

@login_manager.request_loader
def load_user_from_request(request):
    """ Authenticates users via API key from header """
    api_domain = request.headers.get('X-Api-Domain')
    api_key = request.headers.get('X-Api-Key')
    api_user_id = request.headers.get('X-Api-UserId')

    if api_domain is None or api_key is None:
        return None

    auth = get_handler_for(api_domain, MODULE_PATHS['AUTH'])
    if auth is None:
        return None

    user = auth.handle(api_user_id, api_key)
    if user is not None:
        user.remote_api_key = api_key

    return user

@app.before_request
def before_request():
    """ Attempt to authenticate the user on each request """
    g.user = load_user_from_request(request)

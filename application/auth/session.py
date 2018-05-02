from flask import g, request, abort

from application import app, login_manager
from application.misc.register import get_handler_for

@login_manager.request_loader
def load_user_from_request(request):
    """ Authenticates users via API key from header """
    api_domain = request.headers.get('X-Api-Domain')
    api_key = request.headers.get('X-Api-Key')
    api_user_id = request.headers.get('X-Api-UserId')

    if api_domain is None:
        abort(401, "X-Api-Domain not provided. No idea who to try authenticate with!")

    auth = get_handler_for(api_domain, "auth")
    if auth is None:
        abort(403, "There isn't an registered authentication handler for this domain");

    return auth.handle(api_user_id, api_key), api_key

    # User couldn't be authenticated
    return None, None

@app.before_request
def before_request():
    """ Attempt to authenticate the user on each request """
    g.user, remote_api_key = load_user_from_request(request)

    if g.user is not None:
        g.user.remote_api_key = remote_api_key

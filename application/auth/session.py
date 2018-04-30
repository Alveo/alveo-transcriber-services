from flask import g, request

from application import app, login_manager, auth_handlers

@login_manager.request_loader
def load_user_from_request(request):
    """ Authenticates users via API key from header """
    api_key = request.headers.get('X-Api-Key')
    api_type = request.headers.get('X-Api-Type')
    api_user_id = request.headers.get('X-Api-UserId')

    for handler in auth_handlers:
        if handler.auth_name == api_type:
            return handler.authenticate(api_user_id, api_key), api_key

    # User couldn't be authenticated
    return None, None

@app.before_request
def before_request():
    """ Attempt to authenticate the user on each request """
    g.user, remote_api_key = load_user_from_request(request)
    g.user.remote_api_key = remote_api_key

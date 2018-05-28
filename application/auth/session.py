from flask import g, request, abort

from application import app, login_manager
from application.misc.events import get_handler_for, EVENTS

@login_manager.request_loader
def load_user_from_request(request):
    """ Authenticates users via API key from header

    If the user can't be found or authenticated, NoneType will be returned.

    This function builds on the app's event system in order to authenticate.
    By default, the application has no built-in to handle authentication.
    Further information can be found by looking at another module's authentication
    event handler.

    Args:
        request: Flask request object to retrieve headers
    
    Returns:
        User (application.users) object or NoneType if user cannot be resolved
        
    """
    api_domain = request.headers.get('X-Api-Domain')
    api_key = request.headers.get('X-Api-Key')
    api_user_id = request.headers.get('X-Api-UserId')

    if api_domain is None or api_key is None:
        return None

    auth = get_handler_for(api_domain, EVENTS['AUTH'])
    if auth is None:
        return None

    user = auth.handle(api_user_id, api_key)
    if user is not None:
        user.remote_api_key = api_key

    return user


@app.before_request
def before_request():
    """ Handles tasks before processing a request
    
    Attempts to authenticate the user on each request.

    """
    g.user = load_user_from_request(request)


@app.after_request
def after_request(response):
    """ Processes a ready-to-send response

    This will tell the application what we expect back in terms of valid headers, and
    enable more complicated website applications to  access this web application when
    hosted on a different address/domain. You can configure which origins are allowed
    in the global config file.

    Args:
        Response: Flask response object
    
    """
    response.headers.add('Access-Control-Allow-Origin',
                         app.config['ACCESS_CONTROL_ALLOW_ORIGIN'])
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,X-Api-Domain,X-Api-Key')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response



from functools import wraps
from flask import abort, g, request, jsonify
from pyalveo import *

from application import app, db, login_manager
from application.users.model import User

# TODO more elegant solution
#  Ideally do not persistently store AAS API keys for security reasons
API_STORE = {}

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

def activate_api_access(ats_api_key, aas_api_key):
    API_STORE[ats_api_key] = aas_api_key

def get_api_access(ats_api_key):
    try:
        return API_STORE[ats_api_key]
    except:
        return None

def unregister_api_access(ats_api_key):
    API_STORE[ats_api_key] = None

@app.route('/authorize')
def authorize():
    api_key = request.args.get('api_key')
    if not api_key:
        abort(400, "Alveo API key was not provided")

    client = pyalveo.OAuth2(api_url="https://app.alveo.edu.au/", api_key=api_key)
    user_data = client.get_user_data()

    # PyAlveo doesn't return any meaningful errors, so if nothing is returned we will
    #  have to hope and assume it is just because the API key is not valid.
    if user_data is None:
        abort(400, "Request could not be completed. API key may be invalid.")

    user_id = user_data['user_id']

    if user_id is None:
        abort(400, "Malformed or unexpected data was received from the Alveo application server. Request could not be completed.")

    user_ref = User.query.filter(User.alveo_id == user_id).first()
    new_user = False
    if user_ref is None:
        user_ref = User(user_id)
        db.session.add(user_ref)
        db.session.commit()
        new_user = True

    activate_api_access(user_ref.api_key, api_key)

    print(get_api_access(user_ref.api_key))

    return jsonify({'status': 200, 'new_user': new_user, 'ats-api-key': user_ref.api_key}) 

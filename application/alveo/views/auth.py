from pyalveo import *
from flask import abort

from application import app, db
from application.users.model import User
from application.misc.events import handle_api_event, get_module_metadata, EVENTS

from application.alveo.module import DOMAIN

@handle_api_event(DOMAIN, EVENTS['AUTH'])
def auth_alveo(remote_user_id, remote_api_key):
    if not remote_api_key:
        abort(400, "Alveo API key was not provided")

    alveo_metadata = get_module_metadata(DOMAIN)
    if alveo_metadata is None:
        abort(404, "'alveo' module not found.")
    api_url = alveo_metadata['api_url']

    client = pyalveo.OAuth2(api_url=api_url, api_key=remote_api_key)
    user_data = client.get_user_data()

    if user_data is None:
        abort(400, "Request could not be completed. API key may be invalid.")

    user_id = user_data['user_id']

    if user_id is None:
        abort(400, "Malformed or unexpected data was received from the Alveo application server. Request could not be completed.")

    user_ref = User.query.filter(User.remote_id == user_id).filter(User.domain == DOMAIN).first()
    if user_ref is None:
        user_ref = User(user_id, DOMAIN)
        db.session.add(user_ref)
        db.session.commit()
    
    return user_ref

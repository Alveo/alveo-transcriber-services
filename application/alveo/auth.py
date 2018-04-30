from pyalveo import *
from flask import abort

from application import app, db
from application.users.model import User
from application.auth.auth_handler import register_auth_handler

@register_auth_handler("alveo")
def auth_alveo(remote_user_id, remote_api_key):
    if not remote_api_key:
        abort(400, "Alveo API key was not provided")

    client = pyalveo.OAuth2(api_url=app.config['ALVEO_API_URL'], api_key=remote_api_key)
    user_data = client.get_user_data()

    if user_data is None:
        abort(400, "Request could not be completed. API key may be invalid.")

    user_id = user_data['user_id']

    if user_id is None:
        abort(400, "Malformed or unexpected data was received from the Alveo application server. Request could not be completed.")

    user_ref = User.query.filter(User.remote_user_id == "alveo:" + user_id).first()
    if user_ref is None:
        user_ref = User("alveo:" + user_id)
        db.session.add(user_ref)
        db.session.commit()
    
    return user_ref

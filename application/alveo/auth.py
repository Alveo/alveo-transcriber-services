from pyalveo import *
from flask import abort, request, jsonify
from flask.views import MethodView

from application import db
from application.users.model import User
from application.alveo.api_registrant import activate_api_access

class AlveoAuthentication(MethodView):
    def get(self, identifier=None):
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

        return jsonify({'status': 200, 'new_user': new_user, 'ats-api-key': user_ref.api_key}) 

alveo_auth_api = AlveoAuthentication.as_view('alveo_auth_api')

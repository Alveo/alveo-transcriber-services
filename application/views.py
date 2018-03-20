from flask import jsonify, g
from application import app
import application.users.auth

from application.segmentation.component import segmentor_service
from application.datastore.model import Datastore

def url_error(error_code, description):
    response = jsonify({'error': True, 'code': error_code, 'description': description})
    response.status_code = error_code;
    return response

def bad_request(error):
    return url_error(400, error.description)

def not_authorised(error):
    return url_error(401, "Not authorised")

def not_allowed(error):
    return url_error(403, "Forbidden")

def not_found(error):
    return url_error(404, "Resource not found")

def server_error(error):
    return url_error(500, "Server error")

app.register_error_handler(400, bad_request)
app.register_error_handler(401, not_authorised)
app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

app.add_url_rule('/segment', view_func=segmentor_service, methods=['GET', 'POST'])

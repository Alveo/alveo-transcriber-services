from flask import jsonify
from application import app
import application.session

from application.alveo.auth import alveo_auth_api
from application.alveo.segmentation_view import alveo_auth_segmentor_api

def url_error(error_code, description):
    response = jsonify({'error': True, 'status': error_code, 'description': description})
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

app.add_url_rule('/authorize', view_func=alveo_auth_api, methods=['GET'])
app.add_url_rule('/segment', view_func=alveo_auth_segmentor_api, methods=['GET', 'POST'])

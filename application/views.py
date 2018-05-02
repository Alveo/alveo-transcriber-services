from flask import jsonify
from application import app
import application.auth.session
import application.alveo.auth
import application.alveo.segmenter
from application.segmentation.view import segmenter_api
from application.datastore.view import datastore_api

def url_error(error_code, description):
    response = jsonify({'error': True, 'description': description})
    response.status_code = error_code;
    return response

def bad_request(error):
    return url_error(400, error.description)

def not_authorised(error):
    return url_error(401, "Not authorised")

def not_allowed(error):
    return url_error(403, error.description)

def not_found(error):
    return url_error(404, "Resource not found")

def server_error(error):
    return url_error(500, "Server error")

app.register_error_handler(400, bad_request)
app.register_error_handler(401, not_authorised)
app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

app.add_url_rule('/segment', view_func=segmenter_api, methods=['GET', 'POST'])
app.add_url_rule('/storage', view_func=datastore_api, methods=['GET', 'POST'])

from flask import jsonify

from application import app
from application.segmentation.view import segmenter_api
from application.datastore.view import datastore_api
from application.datastore.userstore import userstore_api 
from application.datastore.userstore_list import userstore_list_api
import application.auth.session

# Module specific
import application.alveo.auth
import application.alveo.segmenter
import application.alveo.datastore
import application.alveo.userstore
import application.alveo.userstore_list

def url_error(error_code, description):
    response = jsonify({'error': True, 'description': description})
    response.status_code = error_code;
    return response

def bad_request(error):
    return url_error(400, error.description)

def not_authorised(error):
    return url_error(401, error.description)

def not_allowed(error):
    return url_error(403, error.description)

def not_found(error):
    return url_error(404, error.description)

def server_error(error):
    return url_error(500, "Internal server error")

app.register_error_handler(400, bad_request)
app.register_error_handler(401, not_authorised)
app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

app.add_url_rule('/userstore/archive', view_func=userstore_api, methods=['GET'])
app.add_url_rule('/userstore', view_func=userstore_list_api, methods=['GET'])
app.add_url_rule('/segment', view_func=segmenter_api, methods=['GET', 'POST'])
app.add_url_rule('/storage', view_func=datastore_api, methods=['GET', 'POST'])

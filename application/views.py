from flask import jsonify, g
from application import app
import application.users.auth

#from application.modules.segmentation.web import segment_url

def url_error(error_code):
    response = jsonify({'error': True, 'code': error_code})
    response.status_code = error_code;
    return response

def not_allowed(error):
    return url_error(403)

def not_found(error):
    return url_error(404)

def server_error(error):
    return url_error(500)

app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

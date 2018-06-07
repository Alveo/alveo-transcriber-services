from flask import jsonify

from application import app
import application.auth.session


def url_error(error_code, description):
    response = jsonify({'error': True, 'description': description})
    response.status_code = error_code
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
    # Error argument is expected even if not used
    return url_error(500, "Internal server error")


app.register_error_handler(400, bad_request)
app.register_error_handler(401, not_authorised)
app.register_error_handler(403, not_allowed)
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)

# Import any modules here
import application.alveo as alveo
app.register_blueprint(alveo.views.blueprint, url_prefix='/alveo')

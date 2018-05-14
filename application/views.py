from flask import jsonify

from application import app
from application.segmentation.view import segmenter_api
from application.auth.required import auth_required
import application.datastore.views as datastore
import application.auth.session

import application.alveo.module

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

app.add_url_rule('/segment', view_func=segmenter_api, methods=['GET', 'POST'])

# User's datastore control
app.add_url_rule(
        '/datastore/',
        view_func=auth_required(datastore.manage),
        methods=['GET', 'POST']
    )

# User's own datastore
app.add_url_rule(
        '/datastore/list/',
        endpoint='ds.list',
        view_func=auth_required(datastore.list),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/list/<key>',
        endpoint='ds.list.key',
        view_func=auth_required(datastore.list_key),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/list/<key>/<revision>',
        endpoint='ds.list.key.rev',
        view_func=auth_required(datastore.list_key),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/export/',
        view_func=auth_required(datastore.export),
        endpoint='ds.export',
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/export/<key>',
        view_func=auth_required(datastore.export_key),
        endpoint='ds.export.key',
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/export/<key>/<revision>',
        view_func=auth_required(datastore.export_key),
        endpoint='ds.export.key.rev',
        methods=['GET']
    )

# User specific datastore
app.add_url_rule(
        '/datastore/user/<user_id>/list/',
        endpoint='ds.user.list',
        view_func=auth_required(datastore.list_by_user),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/user/<user_id>/list/<key>',
        endpoint='ds.user.list.key',
        view_func=auth_required(datastore.list_by_user_key),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/user/<user_id>/list/<key>/<revision>',
        endpoint='ds.user.list.key.rev',
        view_func=auth_required(datastore.list_by_user_key),
        methods=['GET']
    )


app.add_url_rule(
        '/datastore/user/<user_id>/export/',
        endpoint='ds.user.export',
        view_func=auth_required(datastore.export_by_user),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/user/<user_id>/export/<key>',
        endpoint='ds.user.export.key',
        view_func=auth_required(datastore.export_by_user_key),
        methods=['GET']
    )

app.add_url_rule(
        '/datastore/user/<user_id>/export/<key>/<revision>',
        endpoint='ds.user.export.key.rev',
        view_func=auth_required(datastore.export_by_user_key),
        methods=['GET']
    )

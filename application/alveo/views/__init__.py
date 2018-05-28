"""
from .datastore import manage 
"""

from flask import Blueprint
from application.alveo.module import DOMAIN

from . import auth
from .segmentation import segmentation_route

from .datastore.manage import store_route
from .datastore.export import export_route
from .datastore.export_key import export_by_key_route
from .datastore.export_by_user import export_by_user_route
from .datastore.export_by_user_key import export_by_user_key_route
from .datastore.list import list_route
from .datastore.list_key import list_by_key_route
from .datastore.list_by_user import list_by_user_route
from .datastore.list_by_user_key import list_by_user_key_route

blueprint = Blueprint(DOMAIN, __name__)

blueprint.add_url_rule(
        '/segment',
        view_func=segmentation_route,
        methods=['GET', 'POST']
    )

blueprint.add_url_rule(
        '/datastore/',
        view_func=store_route,
        methods=['GET', 'POST']
    )

blueprint.add_url_rule(
        '/datastore/export/',
        view_func=export_route,
    )

blueprint.add_url_rule(
        '/datastore/export/<key>',
        view_func=export_by_key_route,
    )

blueprint.add_url_rule(
        '/datastore/export/<key>/<revision>',
        view_func=export_by_key_route
    )

blueprint.add_url_rule(
        '/datastore/user/<user_id>/export/',
        view_func=export_by_user_route,
    )

blueprint.add_url_rule(
        '/datastore/user/<user_id>/export/<key>',
        view_func=export_by_user_key_route,
    )

blueprint.add_url_rule(
        '/datastore/user/<user_id>/export/<key>/<revision>',
        view_func=export_by_user_key_route,
    )

blueprint.add_url_rule(
        '/datastore/list/',
        view_func=list_route,
    )

blueprint.add_url_rule(
        '/datastore/list/<key>',
        view_func=list_by_key_route,
    )

blueprint.add_url_rule(
        '/datastore/list/<key>/<revision>',
        view_func=list_by_key_route
    )

blueprint.add_url_rule(
        '/datastore/user/<user_id>/list/',
        view_func=list_by_user_route,
    )

blueprint.add_url_rule(
        '/datastore/user/<user_id>/list/<key>',
        view_func=list_by_user_key_route,
    )

blueprint.add_url_rule(
        '/datastore/user/<user_id>/list/<key>/<revision>',
        view_func=list_by_user_key_route,
    )

#from application import app
#app.register_blueprint(blueprint, url_prefix='/%s'%DOMAIN)

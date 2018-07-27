from flask import Blueprint
from application.alveo.module import DOMAIN

from . import auth
from .segmentation import segmentation_route
from .datastore.store import store_route
from .datastore.export_by_user import export_by_user_route
from .datastore.list_by_user import list_by_user_route

blueprint = Blueprint(DOMAIN, __name__)

blueprint.add_url_rule(
    '/segment',
    view_func=segmentation_route,
    methods=['GET', 'POST']
)

blueprint.add_url_rule(
    '/datastore/objects',
    view_func=store_route,
    methods=['POST']
)

blueprint.add_url_rule(
    '/datastore/objects/',
    view_func=store_route,
    methods=['GET']
)

blueprint.add_url_rule(
    '/datastore/export/',
    view_func=export_by_user_route,
)

blueprint.add_url_rule(
    '/datastore/export/<user_id>',
    view_func=export_by_user_route,
)

blueprint.add_url_rule(
    '/datastore/list/',
    view_func=list_by_user_route,
)

blueprint.add_url_rule(
    '/datastore/list/<user_id>',
    view_func=list_by_user_route,
)

from flask import Blueprint
from application.alveo.module import DOMAIN

from . import auth
from .asr.add_job import add_job_route
from .asr.cancel_job import cancel_job_route 
from .asr.retrieve_job import retrieve_job_route 
from .asr.list_jobs import list_jobs_route
from .segmentation import segmentation_route
from .datastore.store import store_route
from .datastore.export_by_user import export_by_user_route
from .datastore.list_by_user import list_by_user_route
from .datastore.list_by_key import list_by_key_route

blueprint = Blueprint(DOMAIN, __name__)

blueprint.add_url_rule(
    '/segment',
    view_func=segmentation_route,
    methods=['GET', 'POST']
)

blueprint.add_url_rule(
    '/asr/jobs/add',
    view_func=add_job_route,
    methods=['GET', 'POST']
)

blueprint.add_url_rule(
    '/asr/jobs/cancel',
    view_func=cancel_job_route,
    methods=['GET', 'POST']
)

blueprint.add_url_rule(
    '/asr/jobs/retrieve',
    view_func=retrieve_job_route,
    methods=['GET', 'POST']
)

blueprint.add_url_rule(
    '/asr/jobs',
    view_func=list_jobs_route,
    methods=['GET', 'POST']
)

blueprint.add_url_rule(
    '/datastore/objects',
    view_func=store_route,
    methods=['POST']
)

blueprint.add_url_rule(
    '/datastore/objects/<object_id>',
    view_func=store_route
)

blueprint.add_url_rule(
    '/datastore/objects/<object_id>/<version>',
    view_func=store_route
)

blueprint.add_url_rule(
    '/datastore/export/',
    view_func=export_by_user_route,
)

blueprint.add_url_rule(
    '/datastore/export/<user_id>',
    view_func=export_by_user_route,
)

# Lists everything attached to the requesting user
#  Optional: can provide user_id to view another user
blueprint.add_url_rule(
    '/datastore/list/',
    view_func=list_by_key_route,
)

# Lists everything matching the object_key attached to the requesting user
#  Optional: can provide user_id to view another user
blueprint.add_url_rule(
    '/datastore/list/<object_key>',
    view_func=list_by_key_route,
)

# Lists everything by user_id
blueprint.add_url_rule(
    '/datastore/listall/<user_id>',
    view_func=list_by_user_route,
)

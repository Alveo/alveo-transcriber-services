from application.misc.events import handle_api_event, MODULE_PATHS
from .helper_exports import datastore_export

from application.alveo.module import DOMAIN

@handle_api_event(DOMAIN, MODULE_PATHS['DATASTORE']['EXPORT']['SELF'])
def alveo_datastore_export(user_id, revision):
    return datastore_export(user_id=user_id, revision=revision)

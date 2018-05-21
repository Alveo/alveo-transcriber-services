from application.misc.events import handle_api_event, MODULE_PATHS
from .helper_exports import datastore_export

from application.alveo.module import DOMAIN

@handle_api_event(DOMAIN, MODULE_PATHS['DATASTORE']['EXPORT']['USER+KEY'])
def alveo_datastore_export_by_user_key(user_id, key, revision):
    return datastore_export(user_id=user_id, key=key, revision=revision)

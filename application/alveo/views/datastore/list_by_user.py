from application.misc.events import handle_api_event, MODULE_PATHS
from .helper_lists import datastore_list

from application.alveo.module import DOMAIN

@handle_api_event(DOMAIN, MODULE_PATHS['DATASTORE']['LIST']['USER'])
def alveo_datastore_list_by_user(user_id, revision):
    return datastore_list(user_id=user_id, revision=revision)

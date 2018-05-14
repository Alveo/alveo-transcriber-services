from application.misc.events import handle_api_event
from .helper_lists import datastore_list

@handle_api_event('alveo', 'datastore:list_key')
def alveo_datastore_list_key(user_id, key, revision):
    return datastore_list(user_id=user_id, key=key, revision=revision)

from application.misc.events import handle_api_event
from .helper_exports import datastore_export

@handle_api_event('alveo', 'datastore:export_by_user_key')
def alveo_datastore_export_by_user_key(user_id, key, revision):
    return datastore_export(user_id=user_id, key=key, revision=revision)

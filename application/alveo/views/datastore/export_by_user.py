from application.misc.events import handle_api_event
from .helper_exports import datastore_export

@handle_api_event('alveo', 'datastore:export_by_user')
def alveo_datastore_export_by_user(user_id, revision):
    return datastore_export(user_id=user_id, revision=revision)

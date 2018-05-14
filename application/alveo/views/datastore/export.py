from application.misc.events import handle_api_event
from .helper_exports import datastore_export

@handle_api_event('alveo', 'datastore:export')
def alveo_datastore_export(user_id, revision):
    return datastore_export(user_id=user_id, revision=revision)

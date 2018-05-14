from flask import abort, request
from application.misc.event_router import EventRouter

from application.auth.required import auth_required

class DatastoreAPI(EventRouter):
    def get(self):
        storage_id = request.args.get('storage_id')

        return self.event("datastore:get").handle(
                storage_id=storage_id
            )

    def post(self):
        data = request.get_json()
        storage_key = None
        storage_value = None

        try:
            storage_key = data['storage_key']
            storage_value = data['storage_value']
        except:
            if storage_key is None:
                abort(400, "storage_key not provided")

            if storage_value is None:
                abort(400, "storage_value not provided")

        return self.event("datastore:post").handle(storage_key, storage_value)

datastore_api = auth_required(DatastoreAPI.as_view('datastore_api'))

from flask import abort, request
from application.misc.event_router import EventRouter

from application.auth.required import auth_required

class DatastoreAPI(EventRouter):
    def get(self):
        storage_key = request.args.get('storage_key')
        revision = request.args.get('revision')
        user_id = request.args.get('user_id')
        download_type = request.args.get('download_type')

        if download_type is None:
            download_type = "json"

        return self.event("datastore:get").handle(
                storage_key=storage_key,
                revision=revision,
                user_id=user_id,
                download_type=download_type
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

from flask import abort, request, jsonify

from application.auth.required import auth_required
from application.misc.event_router import EventRouter

class UserstoreAllListAPI(EventRouter):
    def get(self):
        storage_key = request.args.get('storage_key')
        if storage_key is None:
            abort(400, "No storage key provided")

        return self.event("userstore_list_all").handle(storage_key)

userstore_all_list_api = auth_required(UserstoreAllListAPI.as_view('userstore_all_list_api'))

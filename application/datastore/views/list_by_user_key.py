from flask import abort, jsonify

from application.misc.event_router import EventRouter

class APIListByUserKey(EventRouter):
    def get(self, user_id=None, key=None, revision=None):
        if user_id is None:
            abort(400, "User not specified")

        if key is None:
            abort(400, "Key not specified")

        response = self.event("datastore:list_by_user_key").handle(
                storage_key=key,
                user_id=user_id,
                revision=revision
            )

        return jsonify(response)

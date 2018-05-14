from flask import abort, jsonify, g

from application.misc.event_router import EventRouter

class APIListKey(EventRouter):
    def get(self, key=None, revision=None):
        if key is None:
            abort(400, "Key not specified")

        response = self.event("datastore:list_key").handle(
                storage_key=key,
                user_id=g.user.id,
                revision=revision
            )

        return jsonify(response)

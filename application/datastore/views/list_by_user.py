from flask import abort, jsonify

from application.misc.event_router import EventRouter

class APIListByUser(EventRouter):
    def get(self, user_id, revision=None):
        if user_id is None:
            abort(400, "User not specified")

        response = self.event("datastore:list_by_user").handle(
                user_id=user_id,
                revision=revision
            )

        return jsonify(response)

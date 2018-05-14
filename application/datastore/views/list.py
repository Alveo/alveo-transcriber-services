from flask import abort, jsonify, g

from application.misc.event_router import EventRouter

class APIList(EventRouter):
    def get(self, revision=None):
        response = self.event("datastore:list").handle(
                user_id=g.user.id,
                revision=revision
            )

        return jsonify(response)

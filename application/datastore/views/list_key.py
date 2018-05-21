from flask import abort, jsonify, g

from application.misc.events import MODULE_PATHS
from application.misc.event_router import EventRouter

class APIListKey(EventRouter):
    def get(self, key=None, revision=None):
        if key is None:
            abort(400, "Key not specified")

        response = self.event(MODULE_PATHS['DATASTORE']['LIST']['KEY']).handle(
                key=key,
                user_id=g.user.id,
                revision=revision
            )

        return jsonify(response)

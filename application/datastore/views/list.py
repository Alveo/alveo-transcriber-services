from flask import abort, jsonify, g

from application.misc.events import MODULE_PATHS
from application.misc.event_router import EventRouter

class APIList(EventRouter):
    def get(self, revision=None):
        response = self.event(MODULE_PATHS['DATASTORE']['LIST']['SELF']).handle(
                user_id=g.user.id,
                revision=revision
            )

        return jsonify(response)

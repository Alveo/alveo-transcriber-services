from flask import abort, jsonify, g

from application.misc.events import MODULE_PATHS
from application.misc.event_router import EventRouter

class APIList(EventRouter):
    def get(self, revision=None):
        user_id = None
        if g.user != None:
            user_id = g.user.id

        response = self.event(MODULE_PATHS['DATASTORE']['LIST']['SELF']).handle(
                user_id=user_id,
                revision=revision
            )

        return jsonify(response)

from flask import abort, jsonify, g

from application.misc.event_router import EventRouter

class APIList(EventRouter):
    def get(self):
        return self.event("datastore:list").handle(
                user_id=g.user.remote_user_id,
                revision=revision
            )

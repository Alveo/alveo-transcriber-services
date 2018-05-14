from flask import abort, jsonify, g

from application.misc.event_router import EventRouter

class APIExportKey(EventRouter):
    def get(self, key=None, revision=None):
        if key is None:
            abort(400, "Key not specified")

        return self.event("datastore:export_key").handle(
                storage_key=key,
                user_id=g.user.remote_user_id,
                revision=revision
            )

from flask import abort, send_file

from application.misc.events import MODULE_PATHS
from application.misc.event_router import EventRouter

class APIExportByUser(EventRouter):
    def get(self, user_id=None, revision=None):
        if user_id is None:
            abort(400, "User not specified")

        response = self.event(MODULE_PATHS['DATASTORE']['EXPORT']['USER']).handle(
                user_id=user_id,
                revision=revision
            )

        return send_file(
            response['data'],
            response['mimetype'],
            as_attachment=True,
            attachment_filename=response['filename']
        )

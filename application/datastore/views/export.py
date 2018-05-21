from flask import abort, send_file, g

from application.misc.events import MODULE_PATHS
from application.misc.event_router import EventRouter

class APIExport(EventRouter):
    def get(self, revision=None):
        response = self.event(MODULE_PATHS['DATASTORE']['EXPORT']['SELF']).handle(
                user_id=g.user.id,
                revision=revision
            )

        return send_file(
            response['data'],
            response['mimetype'],
            as_attachment=True,
            attachment_filename=response['filename']
        )

from flask import abort, send_file, g

from application.misc.event_router import EventRouter

class APIExportKey(EventRouter):
    def get(self, key=None, revision=None):
        if key is None:
            abort(400, "Key not specified")

        response = self.event("datastore:export_key").handle(
                key=key,
                user_id=g.user.id,
                revision=revision
            )

        return send_file(
            response['data'],
            response['mimetype'],
            as_attachment=True,
            attachment_filename=response['filename']
        )

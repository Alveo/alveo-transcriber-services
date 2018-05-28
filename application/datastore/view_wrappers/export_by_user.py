from flask import abort, send_file

from application.misc.query_wrapper import QueryWrapper


class ExportByUserWrapper(QueryWrapper):
    def get(self, user_id=None, revision=None):
        if user_id is None:
            abort(400, "User not specified")

        response = self._process_get(
            user_id=user_id,
            revision=revision
        )

        return send_file(
            response['data'],
            response['mimetype'],
            as_attachment=True,
            attachment_filename=response['filename']
        )

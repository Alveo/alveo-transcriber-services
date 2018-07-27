from flask import abort, send_file

from application.misc.query_wrapper import QueryWrapper


class ExportByUserKeyWrapper(QueryWrapper):
    def get(self, user_id=None, key=None):
        if user_id is None:
            abort(400, "User not specified")

        if key is None:
            abort(400, "Key not specified")

        response = self._process_get(
            key=key,
            user_id=user_id
        )

        return send_file(
            response['data'],
            response['mimetype'],
            as_attachment=True,
            attachment_filename=response['filename']
        )

from flask import send_file, g

from application.misc.query_wrapper import QueryWrapper

class ExportWrapper(QueryWrapper):
    def get(self, revision=None):
        response = self._processor_get(user_id=g.user.id, revision=revision)

        return send_file(
            response['data'],
            response['mimetype'],
            as_attachment=True,
            attachment_filename=response['filename']
        )

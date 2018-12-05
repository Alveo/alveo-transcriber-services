from flask import jsonify, abort, request, g

from application import app
from application.misc.query_wrapper import QueryWrapper
from application.auth.required import auth_required


class AddJobWrapper(QueryWrapper):
    decorators = [auth_required]

    def get(self):
        remote_url = request.args.get('remote_url')

        if remote_url is None:
            abort(400, 'Request did not include a document to transcribe')

        results = self._processor_get(
            user_id=g.user.id,
            remote_path=remote_url
        )

        return jsonify({
            "results": results
        })

    def post(self):
        if not app.config['ALLOW_POST_TRANSCRIPTION']:
            abort(405)

        if 'file' not in request.files:
            abort(400, 'No file attached to query')

        audiofile = request.files['file']
        if audiofile.filename is '':
            abort(400, 'No file selected in query')

        results = self._processor_post(
            user_id=g.user.id,
            audiofile=audiofile
        )

        return jsonify({
            "results": results
        })

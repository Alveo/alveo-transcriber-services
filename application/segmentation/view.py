from urllib.parse import urlparse

from flask import jsonify, abort, g, request

from application import app
from application.misc.event_router import EventRouter
from application.auth.required import auth_required
from application.segmentation.audio_segmentor import segment_audio_data

class SegmenterAPI(EventRouter):
    def get(self):
        remote_url = request.args.get('remote_url')

        if remote_url is None:
            abort(400, "Request did not include a document to segment");

        results = self.event("segmenter").handle(remote_url)

        return jsonify({
                "results": results
            })

    def post(self):
        if not app.config['ALLOW_POST_SEGMENTATION']:
            abort(405)

        if 'file' not in request.files:
            abort(400, 'No file attached to query')

        audiofile = request.files['file']
        if audiofile.filename is '':
            abort(400, 'No file selected in query')

        result = segment_audio_data(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return jsonify(result)

segmenter_api = auth_required(SegmenterAPI.as_view('segmentor_api'))

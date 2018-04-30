from urllib.parse import urlparse

from flask import jsonify, abort, g, request
from flask.views import MethodView

from application import app, segment_handlers
from application.auth.auth_handler import auth_required
from application.segmentation.audio_segmentor import segment_audio_data

class SegmenterAPI(MethodView):
    @auth_required
    def get(self):
        remote_url = request.args.get('remote_url')

        domain = str(urlparse(remote_url).netloc)

        handler = None
        for handler in app.config['DOMAIN_HANDLERS']:
            if domain in handler['domains']:
                handler = handler['module']
                break

        if handler is None:
            abort(400, "There are no handlers available for the requested URL.")

        for handler_ref in segment_handlers:
            if handler_ref.name == handler:
                return jsonify(handler_ref.segment(remote_url, g.user))

        abort(400, "There are no modules available matching the requested handler for this URL. This is likely a missing optional dependency.")


    @auth_required
    def post(self):
        if 'file' not in request.files:
            abort(400, 'No file attached to query')

        audiofile = request.files['file']
        if audiofile.filename is '':
            abort(400, 'No file selected in query')

        result = segment_audio_data(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return jsonify(result)

segmenter_api = SegmenterAPI.as_view('segmenter_api')

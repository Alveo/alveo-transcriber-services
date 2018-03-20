from flask import jsonify
from flask.views import MethodView

from application import app, db
from application.segmentation.audio_segmentor import AudioSegmentor
from application.users.auth import auth_required

class SegmentorService(MethodView):
    @auth_required
    def get(self, identifier=None):
        if identifier is None:
            return "401"

        return jsonify({})

    @auth_required
    def post(self):
        return "Not Implemented"

segmentor_service = SegmentorService.as_view('segmentor_service')

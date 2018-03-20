from flask import jsonify, abort
from flask.views import MethodView

from application import app, db
from application.segmentation.audio_segmentor import AudioSegmentor
from application.users.auth import auth_required

class SegmentorService(MethodView):
    @auth_required
    def get(self, identifier=None):
        if identifier is None:
            abort(400, "This GET request did not receive an Alveo identifier to segment.")

        # If cached
        #  Check if user can access document
        #  Return result if permissable, else 403

        # Else
        #  Request document with user's API key: will this work with constantly changing keys?
        #  Segment it, cache result 

        return jsonify({})

    @auth_required
    def post(self):
        return "Not Implemented"

segmentor_service = SegmentorService.as_view('segmentor_service')

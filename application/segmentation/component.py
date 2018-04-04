from flask import jsonify, abort, g, request
from flask.views import MethodView

import uuid

import pyalveo

from application import app, db
from application.segmentation.audio_segmentor import AudioSegmentor
from application.segmentation.model import CachedSegmentationResult
from application.users.auth import auth_required, get_api_access

class SegmentorService(MethodView):
    @auth_required
    def get(self, identifier=None):
        document_id = request.args.get('document_id')
        if not document_id:
            abort(400, "Request did not receive an Alveo document identifier to segment.")

        aas_key = get_api_access(g.user.api_key)
        print(aas_key)
        if aas_key is None:
            abort(400, "You're not authorised to access the Alveo API, register your API key at /authorize first.")

        client = pyalveo.Client(api_url="https://app.alveo.edu.au/", api_key=aas_key, use_cache=False, cache_dir=None)

        # TODO cache reading, check if user has permission to access file somehow
        audio_result = None
        try:
            audio_result = client.get_document(document_id)
        except:
            pass

        if audio_result is None:
            abort(400, "Could not access requested document.")


        
        # TODO - Cleanup
        file_path = '/tmp/alveo/'+str(uuid.uuid4());
        with open(file_path, 'wb') as f:
            f.write(audio_result)

        testseg = AudioSegmentor(file_path)
        result = testseg.segment()

        # TODO cache writing

        return jsonify(result)

    @auth_required
    def post(self):
        return "Not Implemented" # TODO

segmentor_service = SegmentorService.as_view('segmentor_service')

from urllib.parse import urlparse

from flask import jsonify, abort, g, request
from flask.views import MethodView

from application import app
from application.session import auth_required
from application.segmentation.cache.model import cache_result, get_cached_result
from application.alveo.document_segmentation import segment_document
from application.segmentation.audio_segmentor import segment_audio_data

def shorten_id(document_id):
    url = urlparse(document_id)
    url = url.path.split('/catalog/')[1]
    return url

class AlveoAuthSegmentor(MethodView):
    @auth_required
    def get(self, identifier=None):
        document_id = request.args.get('document_id')

        if '/' not in str(urlparse(document_id).path):
            abort(400, 'Request did not receive an Alveo document identifier to segment.')

        aas_key = g.user.remote_api_key
        if aas_key is None:
            abort(400, 'You\'re not authorised to access the Alveo API, register your API key at /authorize first.')

        # TODO check Alveo permissions before accessing cache
        #   Note: request submitted to PyAlveo repository for permission checking
        result = get_cached_result(shorten_id(document_id))
        if result is None:
            result = segment_document(document_id, aas_key) 
            if result is None:
                abort(400, 'Could not access requested document.')
            else:
                cache_result(shorten_id(document_id), result)

        response = {'status': 200, 'result': result}
        
        return jsonify(response)

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

alveo_auth_segmentor_api = AlveoAuthSegmentor.as_view('alveo_auth_segmentor_api')

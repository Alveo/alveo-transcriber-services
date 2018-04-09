import os
import uuid
from urllib.parse import urlparse

import pyalveo
from flask import jsonify, abort, g, request
from flask.views import MethodView

from application import app, db
from application.segmentation.audio_segmentor import AudioSegmentor
from application.segmentation.model import CachedSegmentationResult
from application.users.auth import auth_required, get_api_access

def shorten_id(document_id):
    url = urlparse(document_id)
    url = url.path.split('/catalog/')[1]
    return url

def cache_result(document_id, result):
    document_id = shorten_id(document_id)
    if len(document_id) is 0:
        raise Exception("Attempting to store something to the cache without a valid document identifier")
    cached_result = CachedSegmentationResult(document_id, str(result))
    db.session.add(cached_result)
    db.session.commit()

def get_cached_result(document_id):
    document_id = shorten_id(document_id)
    result = CachedSegmentationResult.query.filter(CachedSegmentationResult.alveo_id == document_id).first()
    if result is None:
        return None

    return jsonify(result.data)

def remote_segment(document_id, aas_key):
    client = pyalveo.Client(api_url='https://app.alveo.edu.au/', api_key=aas_key, use_cache=False, update_cache=False, cache_dir=None)

    audio_result = None
    try:
        audio_result = client.get_document(document_id)
    except:
        pass

    if audio_result is None:
        return None

    file_path = '/tmp/alveo/'+str(uuid.uuid4());
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(audio_result)

    result = AudioSegmentor(file_path).segment()

    cache_result(document_id, result)

    try:
        os.remove(tmp_path)
    except:
        pass

    return result

class SegmentorService(MethodView):
    @auth_required
    def get(self, identifier=None):
        document_id = request.args.get('document_id')

        if "/" not in str(urlparse(document_id).path):
            abort(400, 'Request did not receive an Alveo document identifier to segment.')

        aas_key = get_api_access(g.user.api_key)
        if aas_key is None:
            abort(400, 'You\'re not authorised to access the Alveo API, register your API key at /authorize first.')

        # TODO check Alveo permissions before accessing cache
        #   Note: request submitted to PyAlveo repository for permission checking
        result = get_cached_result(document_id)
        if result is None:
            result = remote_segment(document_id, aas_key) 
            if result is None:
                abort(400, 'Could not access requested document.')

        response = {'status': 200, 'result': result}

        return jsonify(response)

    @auth_required
    def post(self):
        return 'Not Implemented' # TODO

segmentor_service = SegmentorService.as_view('segmentor_service')

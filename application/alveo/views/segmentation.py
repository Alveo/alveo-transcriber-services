from urllib.parse import urlparse

from pyalveo import *
from flask import abort, g

from application.auth.required import auth_required
from application.segmentation.cache.model import cache_result, get_cached_result
from application.alveo.document_segmentation import segment_document
from application.misc.events import handle_api_event

def shorten_path(path):
    return urlparse(path).path.split('/catalog/')[1]

@handle_api_event("alveo", "segmenter")
def alveo_segmenter(path):
    api_path = str(urlparse(path).path)
    if '/' not in api_path or api_path == "/":
        abort(400, 'Request did not include an Alveo document identifier to segment')

    api_key = g.user.remote_api_key

    # TODO check Alveo permissions before accessing cache
    #   Note: request submitted to PyAlveo repository for permission checking
    result = get_cached_result(shorten_path(path))
    if result is None:
        result = segment_document(path, api_key) 
        if result is None:
            abort(400, 'Could not access requested document')
        else:
            cache_result(shorten_path(path), result)

    return result

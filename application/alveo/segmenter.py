from urllib.parse import urlparse

from pyalveo import *
from flask import abort, g

from application.session import auth_required
from application.segmentation.segment_handlers import register_segmenter
from application.segmentation.cache.model import cache_result, get_cached_result
from application.alveo.document_segmentation import segment_document

def shorten_path(path):
    url = urlparse(path)
    url = url.path.split('/catalog/')[1]
    return url

@auth_required
@register_segmenter("alveo")
def alveo_segmenter(path, user_ref):
    if '/' not in str(urlparse(path).path):
        abort(400, 'Request did not receive an Alveo document identifier to segment.')

    api_key = g.user.remote_api_key

    # TODO check Alveo permissions before accessing cache
    #   Note: request submitted to PyAlveo repository for permission checking
    result = get_cached_result(shorten_path(path))
    if result is None:
        result = segment_document(path, api_key) 
        if result is None:
            abort(400, 'Could not access requested document.')
        else:
            cache_result(shorten_id(path), result)

    return result

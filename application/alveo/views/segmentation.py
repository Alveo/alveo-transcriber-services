from urllib.parse import urlparse

from pyalveo import *
from flask import abort, g

from application.auth.required import auth_required
from application.segmentation.cache.model import cache_result, get_cached_result
from application.alveo.document_segmentation import segment_document
from application.misc.events import get_module_metadata
from application.misc.query_wrapper import QueryWrapper
from application.segmentation.view import UniformSegmenterWrapper

from application.alveo.module import DOMAIN

def shorten_path(path):
    return urlparse(path).path.split('/catalog/')[1]

class AlveoSegmentationRoute(UniformSegmenterWrapper):
    decorators = [auth_required]

    def _processor_get(self, path):
        api_path = str(urlparse(path).path)
        if '/' not in api_path or api_path == "/":
            abort(400, 'Request did not include an Alveo document identifier to segment')

        api_key = g.user.remote_api_key

        alveo_metadata = get_module_metadata("alveo")
        api_url = alveo_metadata['api_url']
        client = pyalveo.Client(api_url=api_url, api_key=api_key, use_cache=False, update_cache=False, cache_dir=None)

        # Check if we can access the list first.
        # Would be good if we could just check Alveo permissions instead of retrieving the item directly. 
        # https://github.com/Alveo/pyalveo/issues/11
        try:
            itemlist_path = path.split('/document/')[0]
            itemlist = client.get_item(itemlist_path)
        except APIError as e:
            abort(400, "Response from remote host: \n"+str(e))

        result = get_cached_result(shorten_path(path))
        if result is None:
            result = segment_document(path, api_key) 
            if result is None:
                abort(400, 'Could not access requested document')
            else:
                cache_result(shorten_path(path), result)

        return result

segmentation_route = AlveoSegmentationRoute.as_view('/alveo/segment')

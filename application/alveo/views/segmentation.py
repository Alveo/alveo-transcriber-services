from urllib.parse import urlparse

from pyalveo import *
from flask import abort, g

from application import limiter
from application.alveo.module import DOMAIN
from application.auth.required import auth_required
from application.segmentation.cache.model import cache_result, get_cached_result
from application.alveo.document_segmentation import segment_document
from application.misc.modules import get_module_metadata
from application.segmentation.view_wrapper import SegmenterWrapper
from application.segmentation.audio_segmenter import segment_audio_data


def shorten_path(path):
    return urlparse(path).path.split('/catalog/')[1]


class AlveoSegmentationRoute(SegmenterWrapper):
    decorators = [
        auth_required,
        limiter.limit("15 per minute"),
        limiter.limit("150 per day")
    ]

    def _processor_get(self, user_id, remote_path):
        api_path = str(urlparse(remote_path).path)
        if '/' not in api_path or api_path == "/":
            abort(
                400,
                'Request did not include an Alveo document identifier to segment')

        # We care more about the user itself than the user_id, another option
        # is to query the database for something that matches the key but that
        # would be slower
        api_key = g.user.remote_api_key

        alveo_metadata = get_module_metadata("alveo")
        api_url = alveo_metadata['api_url']
        client = pyalveo.Client(
            api_url=api_url,
            api_key=api_key,
            use_cache=False,
            update_cache=False,
            cache_dir=None)

        # Check if we can access the list first.
        # Would be good if we could just check Alveo permissions instead of retrieving the item directly.
        # https://github.com/Alveo/pyalveo/issues/11
        try:
            itemlist_path = remote_path.split('/document/')[0]
            itemlist = client.get_item(itemlist_path)
        except APIError as e:
            abort(400, "Response from remote host: \n" + str(e))

        result = get_cached_result(shorten_path(remote_path))
        if result is None:
            result = segment_document(remote_path, api_key)
            if result is None:
                abort(400, 'Could not access requested document')
            else:
                cache_result(shorten_path(remote_path), result)

        return result

    def _processor_post(self, user_id, audiofile):
        result = segment_audio_data(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return result


segmentation_route = AlveoSegmentationRoute.as_view('/alveo/segment')

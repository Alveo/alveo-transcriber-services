from flask import abort, g

from application import limiter
from application.alveo.module import shorten_path
from application.alveo.views.access import verify_access
from application.auth.required import auth_required
from application.alveo.services import segment_document
from application.datastore.binary import create_binary_object, get_binary_object
from application.segmentation.view_wrapper import SegmenterWrapper
from application.segmentation.audio_segmenter import segment_audio_data

class AlveoSegmentationRoute(SegmenterWrapper):
    decorators = [
        auth_required,
        limiter.limit("15 per minute"),
        limiter.limit("150 per day")
    ]

    def _processor_get(self, user_id, remote_path):
        api_key = g.user.remote_api_key
        verify_access(remote_path, api_key)

        short_path = shorten_path(remote_path)

        result = get_binary_object(short_path)
        if result is None:
            result = segment_document(remote_path, api_key)
            if result is None:
                abort(400, 'Could not access requested document')
            else:
                create_binary_object(short_path, result)

        return result

    def _processor_post(self, user_id, audiofile):
        result = segment_audio_data(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return result


segmentation_route = AlveoSegmentationRoute.as_view('/alveo/segment')

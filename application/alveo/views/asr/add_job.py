from flask import abort, g

from application import limiter
from application.alveo.module import shorten_path
from application.alveo.views.access import verify_access
from application.auth.required import auth_required
from application.alveo.services import transcribe_document
from application.datastore.binary import create_binary_object, get_binary_object
from application.asr.view_wrappers.add_job import AddJobWrapper
from application.asr.engines.gcloud.speech import transcribe

class AlveoASRAddJobRoute(AddJobWrapper):
    decorators = [
        auth_required,
        limiter.limit("5 per minute"),
        limiter.limit("50 per day")
    ]

    def _processor_get(self, user_id, remote_path):
        api_key = g.user.remote_api_key
        verify_access(remote_path, api_key)

        short_path = shorten_path(remote_path)

        result = get_binary_object(short_path)
        if result is None:
            result = transcribe_document(remote_path, api_key)
            if result is None:
                abort(400, 'Could not access requested document')
            else:
                create_binary_object(short_path, result)

        return result

    def _processor_post(self, user_id, audiofile):
        result = transcribe(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return result


add_job_route = AlveoASRAddJobRoute.as_view('/alveo/asr/jobs/add')
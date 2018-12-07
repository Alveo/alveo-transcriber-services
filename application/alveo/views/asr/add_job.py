from flask import abort, g
from rq import get_current_job
from uuid import uuid4

from application import limiter, redis_queue, db
from application.datastore.model import Datastore
from application.users.model import User
from application.jobs.model import Job
from application.jobs.types import JobTypes

from application.alveo.module import shorten_path, DOMAIN
from application.alveo.views.access import verify_access
from application.alveo.views.asr.helper_exporter import export_asrdata
from application.auth.required import auth_required
from application.alveo.services import transcribe_document
from application.datastore.binary import create_binary_object, get_binary_object
from application.asr.view_wrappers.add_job import AddJobWrapper
from application.asr.engines.gcloud.speech import transcribe

ENGINE = "asr-engine-gcloud"

def test():
    active_job = get_current_job()
    job = Job.query.filter(Job.external_id == active_job.id).first()
    if job is None:
        print("Error: Job %s doesn't exist in application database" % active_job.id)
        return

    job.status = JobTypes.FINISHED
    job.datastore.set_value("{'success': true}")
    db.session.commit()
    print(job.datastore.get_value())
    print(job.status)
    print("Done")
    #    create_binary_object(short_path, result)

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

        # Check cache first
        cached_asr = Datastore.query.filter(
            Datastore.key == '%s:%s:%s' % (DOMAIN, ENGINE, short_path)).first()
        if cached_asr is not None:
            return {
                "status": "cached",
                "result": export_asrdata(cached_asr)
            }

        worker = redis_queue.enqueue(transcribe_document, (remote_path, api_key))
        ds = Datastore(
            key="%s:%s:%s" % (DOMAIN, ENGINE, short_path),
            value="{}",
            storage_spec="asr-engine-gcloud/json/1.0",
            user=g.user,
            alias="init"
        )
        job = Job(
            external_id=worker.id,
            user=g.user,
            datastore=ds,
            description="ASR via engine 'gcloud' for item: %s" % short_path
        )
        db.session.add(ds)
        db.session.add(job)
        db.session.commit()

        return {"status": "queued", "job_id": job.id}


    def _processor_post(self, user_id, audiofile):
        result = transcribe(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return result


add_job_route = AlveoASRAddJobRoute.as_view('/alveo/asr/jobs/add')
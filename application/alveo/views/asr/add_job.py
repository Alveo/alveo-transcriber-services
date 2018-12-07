from flask import abort, g
from rq import get_current_job
from uuid import uuid4

from application import limiter, redis_queue, db
from application.datastore.model import Datastore
from application.users.model import User
from application.jobs.model import Job
from application.jobs.types import JobTypes

from application.alveo.module import shorten_path
from application.alveo.views.access import verify_access
from application.auth.required import auth_required
from application.alveo.services import transcribe_document
from application.datastore.binary import create_binary_object, get_binary_object
from application.asr.view_wrappers.add_job import AddJobWrapper
from application.asr.engines.gcloud.speech import transcribe

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

class AlveoASRAddJobRoute(AddJobWrapper):
    decorators = [
        auth_required,
        limiter.limit("5 per minute"),
        limiter.limit("50 per day")
    ]

    def _processor_get(self, user_id, remote_path):
        api_key = g.user.remote_api_key
        verify_access(remote_path, api_key)

        # Enqueued the function
        worker = redis_queue.enqueue(test)
        ds = Datastore("justatest-%s" % uuid4(), "{}", "", g.user, "Noalias")
        job = Job(
            external_id=worker.id,
            user=g.user,
            datastore=ds,
            description="This is just a test job"
        )
        db.session.add(ds)
        db.session.add(job)
        db.session.commit()

        # Create the job
        return {"status": "queued", "job_id": job.id}

        #short_path = shorten_path(remote_path)

        #result = get_binary_object(short_path)
        #if result is None:
        #result = transcribe_document(remote_path, api_key)
        #if result is None:
        #    abort(400, 'Could not access requested document')
        #else:
        #    create_binary_object(short_path, result)

        #return result

    def _processor_post(self, user_id, audiofile):
        result = transcribe(audiofile.read())
        if result is None:
            abort(400, "Uploaded file is not a valid .wav audio file.")

        return result


add_job_route = AlveoASRAddJobRoute.as_view('/alveo/asr/jobs/add')
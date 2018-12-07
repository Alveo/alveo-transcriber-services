from flask import abort

from application.alveo.views.asr.helper_job_query import job_query
from application.asr.view_wrappers.cancel_job import CancelJobWrapper
from application.auth.required import auth_required
from application.jobs.types import JobTypes

from application import limiter, redis_queue, db


class AlveoASRCancelJobRoute(CancelJobWrapper):
    decorators = [
        auth_required,
        limiter.limit("50 per minute"),
        limiter.limit("1000 per hour"),
        limiter.limit("5000 per day")
    ]

    def _processor_get(self, user_id, job_id):
        jobs = job_query(user_id=user_id, job_id=job_id)

        if len(jobs) < 1:
            abort(404, "You have no job matching that job_id")

        job_model = jobs[0]
        status = job_model.status

        if status is not JobTypes.QUEUED:
            abort(401, "Job ID `%s` is not queued" % job_id)

        job_object = redis_queue.fetch_job(job_model.external_id)

        if job_object is None:
            job_model.status = JobTypes.FAILED
            abort(401, "Job ID `%s` couldn't be found. Moving to 'failed' pool" % job_id)

        job_object.cancel()
        job_model.status = JobTypes.CANCELLED
        db.session.commit()

        return {"status": "cancelled", "job_id": job_id}


cancel_job_route = AlveoASRCancelJobRoute.as_view('/alveo/asr/jobs/cancel')
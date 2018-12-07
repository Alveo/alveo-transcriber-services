from flask import abort

from application.alveo.views.asr.helper_job_query import job_query
from application.asr.view_wrappers.retrieve_job import RetrieveJobWrapper
from application.auth.required import auth_required
from application.jobs.types import JobTypes

from application import limiter


class AlveoASRRetrieveJobRoute(RetrieveJobWrapper):
    decorators = [
        auth_required,
        limiter.limit("25 per minute"),
        limiter.limit("1000 per day")
    ]

    def _processor_get(self, user_id, job_id):
        jobs = job_query(user_id=user_id, job_id=job_id)

        if len(jobs) < 1:
            abort(404, "You have no job matching that job_id")

        job_model = jobs[0]
        status = job_model.status
        data = {
            "job_id": job_id,
            "status": status
        }

        if status is JobTypes.FINISHED:
            data["result"] = job_model.result

        return data


retrieve_job_route = AlveoASRRetrieveJobRoute.as_view('/alveo/asr/jobs/get')
import json

from flask import abort

from application.alveo.views.asr.helper_exporter import export_asrdata
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

        job = jobs[0]
        status = job.status
        ds_object = job.datastore
        data = {
            "job_id": job_id,
            "status": JobTypes(status).name,
            "description": job.description
        }

        if status is JobTypes.FINISHED.value:
            data["result"] = export_asrdata(ds_object)

        return data


retrieve_job_route = AlveoASRRetrieveJobRoute.as_view('/alveo/asr/jobs/get')
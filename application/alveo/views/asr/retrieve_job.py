from .helper_jobs import retrieve_job

from application.auth.required import auth_required
from application.asr.view_wrappers.retrieve_job import RetrieveJobWrapper

from application import limiter


class AlveoASRRetrieveJobRoute(RetrieveJobWrapper):
    decorators = [
        auth_required,
        limiter.limit("25 per minute"),
        limiter.limit("1000 per day")
    ]

    def _processor_get(self, user_id, job_id):
        # Find the job matching the user_id and job_id
        # If it is finished, return the data from it
        # If it is not finished, return the status of the job
        pass # TODO


retrieve_job_route = AlveoASRRetrieveJobRoute.as_view('/alveo/asr/jobs/get')
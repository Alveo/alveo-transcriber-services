from .helper_jobs import cancel_job

from application.auth.required import auth_required
from application.asr.view_wrappers.cancel_job import CancelJobWrapper

from application import limiter


class AlveoASRCancelJobRoute(CancelJobWrapper):
    decorators = [
        auth_required,
        limiter.limit("50 per minute"),
        limiter.limit("1000 per hour"),
        limiter.limit("5000 per day")
    ]

    def _processor_get(self, user_id, job_id):
        # Find the job matching the user_id and job_id
        # Switch it to cancelled status, cancel it on redis
        pass # TODO


cancel_job_route = AlveoASRCancelJobRoute.as_view('/alveo/asr/jobs/cancel')
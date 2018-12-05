from .helper_jobs import list_jobs

from application.auth.required import auth_required
from application.asr.view_wrappers.list_jobs import ListJobsWrapper

from application import limiter


class AlveoASRListJobsRoute(ListJobsWrapper):
    decorators = [
        auth_required,
        limiter.limit("50 per minute"),
        limiter.limit("1000 per hour"),
        limiter.limit("5000 per day")
    ]

    def _processor_get(self, user_id):
        # Return all jobs matching the user_id
        pass # TODO


list_jobs_route = AlveoASRListJobsRoute.as_view('/alveo/asr/jobs')
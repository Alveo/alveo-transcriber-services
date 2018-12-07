from application.alveo.views.asr.helper_job_query import job_query
from application.asr.view_wrappers.list_jobs import ListJobsWrapper
from application.auth.required import auth_required
from application.jobs.types import JobTypes

from application import limiter


class AlveoASRListJobsRoute(ListJobsWrapper):
    decorators = [
        auth_required,
        limiter.limit("50 per minute"),
        limiter.limit("1000 per hour"),
        limiter.limit("5000 per day")
    ]

    def _processor_get(self, user_id):
        query_jobs = job_query(user_id=user_id)
        job_data = []

        for job in query_jobs:
            job_data.append({
                'id': job.id,
                'status': JobTypes(job.status).name,
                'description': job.description
            })

        data = {
            'jobs': job_data
        }

        return data


list_jobs_route = AlveoASRListJobsRoute.as_view('/alveo/asr/jobs')
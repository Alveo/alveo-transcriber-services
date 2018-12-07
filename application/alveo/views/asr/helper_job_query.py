from flask import abort

from application.jobs.model import Job
from application.users.model import User

from application.alveo.module import DOMAIN


def job_query(user_id=None, job_id=None):
    query = None

    if user_id is None:
        abort(401, "You must log in to do that")

    if job_id is None:
        query = Job.query
    else:
        query = Job.query.filter(
            Job.external_id == '%s:%s' % (DOMAIN, job_id)
        )

    query = query.filter(Job.user_id == user_id)

    jobs = query.all()

    return jobs

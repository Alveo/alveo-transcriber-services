from flask import abort, jsonify, request, g

from application.misc.query_wrapper import QueryWrapper
from application.auth.required import auth_required


class JobTargetTemplate(QueryWrapper):
    decorators = [auth_required] # Jobs are bound to a user, so we must authenticate

    def get(self):
        job_id = request.args.get('job_id')
        if job_id is None:
            abort(400, "Job ID not specified")

        user_id = g.user.id

        response = self._processor_get(
            job_id=job_id,
            user_id=user_id
        )

        return jsonify(response)

from flask import abort, jsonify, request, g

from application.misc.query_wrapper import QueryWrapper
from application.auth.required import auth_required


class ListJobsWrapper(QueryWrapper):
    decorators = [auth_required] # Jobs are bound to a user, so we must authenticate

    def get(self):
        response = self._processor_get(
            user_id=g.user.id
        )

        return jsonify(response)

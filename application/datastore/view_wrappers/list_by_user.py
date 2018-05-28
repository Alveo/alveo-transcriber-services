from flask import abort, jsonify

from application.misc.query_wrapper import QueryWrapper


class ListByUserWrapper(QueryWrapper):
    def get(self, user_id, revision=None):
        if user_id is None:
            abort(400, "User not specified")

        response = self._processor_get(
            user_id=user_id,
            revision=revision
        )

        return jsonify(response)

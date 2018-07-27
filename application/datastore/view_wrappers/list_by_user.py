from flask import abort, g, jsonify

from application.misc.query_wrapper import QueryWrapper


class ListByUserWrapper(QueryWrapper):
    def get(self, user_id=None):
        if user_id is None:
            if g.user is not None:
                user_id = g.user.id
            else:
                abort(403, "You must log in to do that")

        response = self._processor_get(
            user_id=user_id
        )

        return jsonify(response)

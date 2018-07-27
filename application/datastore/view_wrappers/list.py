from flask import jsonify, g

from application.misc.query_wrapper import QueryWrapper


class ListWrapper(QueryWrapper):
    def get(self):
        user_id = None
        if g.user is not None:
            user_id = g.user.id

            response = self._processor_get(
                user_id=user_id
            )

        return jsonify(response)

from flask import jsonify, g

from application.misc.query_wrapper import QueryWrapper

class ListWrapper(QueryWrapper):
    def get(self, revision=None):
        user_id = None
        if g.user != None:
            user_id = g.user.id

            response = self._processor_get(
                user_id=user_id,
                revision=revision
            )

        return jsonify(response)

from flask import abort, jsonify, g

from application.misc.query_wrapper import QueryWrapper


class ListByKeyWrapper(QueryWrapper):
    def get(self, object_key=None):
        if object_key is None:
            abort(400, "Key not specified")

        response = self._processor_get(
            object_key=object_key,
            user_id=g.user.id
        )

        return jsonify(response)

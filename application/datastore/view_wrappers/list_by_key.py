from flask import abort, jsonify, g

from application.misc.query_wrapper import QueryWrapper


class ListByKeyWrapper(QueryWrapper):
    def get(self, key=None, revision=None):
        if key is None:
            abort(400, "Key not specified")

        response = self._processor_get(
            key=key,
            user_id=g.user.id,
            revision=revision
        )

        return jsonify(response)

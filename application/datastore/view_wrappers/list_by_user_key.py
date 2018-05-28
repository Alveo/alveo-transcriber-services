from flask import abort, jsonify

from application.misc.query_wrapper import QueryWrapper

class ListByUserKeyWrapper(QueryWrapper):
    def get(self, user_id=None, key=None, revision=None):
        if user_id is None:
            abort(400, "User not specified")

        if key is None:
            abort(400, "Key not specified")

        response = self._processor_get(
                key=key,
                user_id=user_id,
                revision=revision
            )

        return jsonify(response)

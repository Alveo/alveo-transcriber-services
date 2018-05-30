from flask import abort, g, jsonify, request

from application.misc.query_wrapper import QueryWrapper


class RevisionsWrapper(QueryWrapper):
    def get(self, store_id):
        if store_id is None:
            abort(400, "store_id not provided or invalid")

        response = self._processor_get(
            store_id=store_id,
            user_id=g.user.id
        )
        return jsonify(response)

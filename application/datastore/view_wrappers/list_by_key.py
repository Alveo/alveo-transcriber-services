from flask import abort, jsonify, request, g

from application.misc.query_wrapper import QueryWrapper


class ListByKeyWrapper(QueryWrapper):
    def get(self, object_key=None):
        user_id = request.args.get('user_id')

        #if object_key is None:
        #    abort(400, "Key not specified")

        if user_id is None:
            if g.user is not None:
                user_id = g.user.id
            else:
                abort(401, "You must log in to do that")

        response = self._processor_get(
            object_key=object_key,
            user_id=user_id
        )

        return jsonify(response)
